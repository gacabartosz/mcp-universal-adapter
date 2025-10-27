"""OpenAPI 3.x parser implementation."""

import json
from pathlib import Path
from typing import Any

import httpx
import yaml

from mcp_adapter.models import (
    AuthConfig,
    AuthType,
    Endpoint,
    HTTPMethod,
    NormalizedAPISpec,
    Parameter,
    ParameterLocation,
    PropertySchema,
    SchemaModel,
    ServerConfig,
)
from mcp_adapter.parsers.base import (
    BaseParser,
    ParserError,
    ParserNetworkError,
    ParserValidationError,
)


class OpenAPIParser(BaseParser):
    """Parser for OpenAPI 3.x specifications.

    Supports:
    - OpenAPI 3.0.x
    - OpenAPI 3.1.x
    - JSON and YAML formats
    - URL or file path sources
    """

    def __init__(self, source: str | Path):
        super().__init__(source)
        self.spec: dict[str, Any] | None = None

    async def parse(self) -> NormalizedAPISpec:
        """Parse OpenAPI specification."""
        # 1. Load spec
        await self._load_spec()

        # 2. Validate it's OpenAPI
        if not self.validate():
            raise ParserValidationError(f"Invalid OpenAPI specification: {self.source}")

        # Type assertion: validate() ensures self.spec is not None
        assert self.spec is not None

        # 3. Extract components
        info = self.spec.get("info", {})
        servers = self._extract_servers()
        endpoints = self._extract_endpoints()
        auth = self._extract_auth()
        schemas = self._extract_schemas()

        # 4. Build normalized spec
        return NormalizedAPISpec(
            name=info.get("title", "Unknown API"),
            version=info.get("version", "1.0.0"),
            description=info.get("description"),
            servers=servers,
            endpoints=endpoints,
            auth=auth,
            schemas=schemas,
            contact=info.get("contact"),
            license=info.get("license"),
            external_docs=self.spec.get("externalDocs", {}).get("url"),
            tags=[
                {"name": t.get("name", ""), "description": t.get("description", "")}
                for t in self.spec.get("tags", [])
            ],
            source_format="openapi",
            source_url=self.source if self.is_url(self.source) else None,
            base_url=servers[0].url if servers else None,
        )

    async def _load_spec(self) -> None:
        """Load OpenAPI spec from URL or file."""
        if self.is_url(self.source):
            # Fetch from URL
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(self.source, timeout=30.0)
                    response.raise_for_status()

                    # Try JSON first
                    try:
                        self.spec = response.json()
                    except json.JSONDecodeError:
                        # Try YAML
                        self.spec = yaml.safe_load(response.text)

            except httpx.HTTPError as e:
                raise ParserNetworkError(f"Failed to fetch OpenAPI spec: {e}") from e

        elif self.is_file(self.source):
            # Load from file
            path = Path(self.source)
            content = path.read_text()

            try:
                if path.suffix in [".json"]:
                    self.spec = json.loads(content)
                elif path.suffix in [".yaml", ".yml"]:
                    self.spec = yaml.safe_load(content)
                else:
                    # Try JSON first, then YAML
                    try:
                        self.spec = json.loads(content)
                    except json.JSONDecodeError:
                        self.spec = yaml.safe_load(content)
            except Exception as e:
                raise ParserError(f"Failed to parse file: {e}") from e
        else:
            raise ParserError(f"Source not found: {self.source}")

    def validate(self) -> bool:
        """Validate OpenAPI specification."""
        if not self.spec:
            return False

        # Check for OpenAPI version
        openapi_version = self.spec.get("openapi", "")
        if not openapi_version.startswith("3."):
            return False

        # Check for required fields
        if "info" not in self.spec:
            return False

        if "paths" not in self.spec:
            return False

        return True

    def _extract_servers(self) -> list[ServerConfig]:
        """Extract server configurations."""
        assert self.spec is not None
        servers = []
        for server in self.spec.get("servers", []):
            servers.append(
                ServerConfig(
                    url=server.get("url", ""),
                    description=server.get("description"),
                    variables=server.get("variables", {}),
                )
            )
        return servers

    def _extract_endpoints(self) -> list[Endpoint]:
        """Extract all API endpoints from paths."""
        assert self.spec is not None
        endpoints = []
        paths = self.spec.get("paths", {})

        for path, path_item in paths.items():
            # Skip non-operation keys
            for method in ["get", "post", "put", "patch", "delete", "head", "options"]:
                if method not in path_item:
                    continue

                operation = path_item[method]
                endpoint = self._build_endpoint(path, method.upper(), operation)
                endpoints.append(endpoint)

        return endpoints

    def _build_endpoint(self, path: str, method: str, operation: dict[str, Any]) -> Endpoint:
        """Build Endpoint model from OpenAPI operation."""
        # Extract parameters
        parameters = []
        for param in operation.get("parameters", []):
            parameters.append(self._build_parameter(param))

        # Extract request body
        request_body = None
        if "requestBody" in operation:
            request_body = self._build_request_body(operation["requestBody"])

        # Extract response
        response_schema = None
        responses = operation.get("responses", {})
        if "200" in responses:
            response_schema = self._build_response_schema(responses["200"])
        elif "201" in responses:
            response_schema = self._build_response_schema(responses["201"])

        return Endpoint(
            path=path,
            method=HTTPMethod(method),
            operation_id=operation.get("operationId"),
            summary=operation.get("summary"),
            description=operation.get("description"),
            tags=operation.get("tags", []),
            parameters=parameters,
            request_body=request_body,
            response_schema=response_schema,
            deprecated=operation.get("deprecated", False),
            external_docs=operation.get("externalDocs", {}).get("url"),
        )

    def _build_parameter(self, param: dict[str, Any]) -> Parameter:
        """Build Parameter model from OpenAPI parameter."""
        location_map = {
            "query": ParameterLocation.QUERY,
            "header": ParameterLocation.HEADER,
            "path": ParameterLocation.PATH,
            "cookie": ParameterLocation.COOKIE,
        }

        schema = param.get("schema", {})
        param_type = self._openapi_type_to_python(schema.get("type", "string"))

        return Parameter(
            name=param.get("name", ""),
            location=location_map.get(param.get("in", "query"), ParameterLocation.QUERY),
            type=param_type,
            description=param.get("description"),
            required=param.get("required", False),
            default=schema.get("default"),
            param_schema=self._build_property_schema(param.get("name", ""), schema),  # type: ignore[call-arg]
            example=param.get("example") or schema.get("example"),
        )

    def _build_request_body(self, request_body: dict[str, Any]) -> SchemaModel | None:
        """Build SchemaModel from OpenAPI requestBody."""
        content = request_body.get("content", {})
        # Try application/json first
        media_type = content.get("application/json") or content.get(
            "application/x-www-form-urlencoded"
        )

        if not media_type:
            return None

        schema = media_type.get("schema", {})
        return self._build_schema_model("RequestBody", schema)

    def _build_response_schema(self, response: dict[str, Any]) -> SchemaModel | None:
        """Build SchemaModel from OpenAPI response."""
        content = response.get("content", {})
        media_type = content.get("application/json")

        if not media_type:
            return None

        schema = media_type.get("schema", {})
        return self._build_schema_model("Response", schema)

    def _build_schema_model(self, name: str, schema: dict[str, Any]) -> SchemaModel:
        """Build SchemaModel from OpenAPI schema."""
        properties = {}
        for prop_name, prop_schema in schema.get("properties", {}).items():
            properties[prop_name] = self._build_property_schema(prop_name, prop_schema)

        return SchemaModel(
            name=name,
            description=schema.get("description"),
            properties=properties,
            required=schema.get("required", []),
            example=schema.get("example"),
        )

    def _build_property_schema(self, name: str, schema: dict[str, Any]) -> PropertySchema:
        """Build PropertySchema from OpenAPI schema."""
        prop_type = schema.get("type", "string")

        # Handle array items
        items = None
        if prop_type == "array" and "items" in schema:
            items = self._build_property_schema("item", schema["items"])

        # Handle object properties
        properties = None
        if prop_type == "object" and "properties" in schema:
            properties = {
                key: self._build_property_schema(key, val)
                for key, val in schema.get("properties", {}).items()
            }

        return PropertySchema(
            name=name,
            type=prop_type,
            description=schema.get("description"),
            required=schema.get("required", False),
            default=schema.get("default"),
            enum=schema.get("enum"),
            format=schema.get("format"),
            pattern=schema.get("pattern"),
            min_length=schema.get("minLength"),
            max_length=schema.get("maxLength"),
            minimum=schema.get("minimum"),
            maximum=schema.get("maximum"),
            items=items,
            properties=properties,
            example=schema.get("example"),
        )

    def _extract_auth(self) -> AuthConfig | None:
        """Extract authentication configuration."""
        assert self.spec is not None
        security_schemes = self.spec.get("components", {}).get("securitySchemes", {})

        if not security_schemes:
            return None

        # Get first security scheme (simplified)
        scheme_name, scheme = next(iter(security_schemes.items()))
        scheme_type = scheme.get("type", "").lower()

        if scheme_type == "apikey":
            return AuthConfig(
                type=AuthType.API_KEY,
                name=scheme.get("name", "api_key"),
                location=ParameterLocation(scheme.get("in", "header")),
                description=scheme.get("description"),
            )
        elif scheme_type == "http":
            http_scheme = scheme.get("scheme", "").lower()
            if http_scheme == "bearer":
                return AuthConfig(
                    type=AuthType.BEARER,
                    scheme="Bearer",
                    description=scheme.get("description"),
                )
            elif http_scheme == "basic":
                return AuthConfig(
                    type=AuthType.BASIC,
                    scheme="Basic",
                    description=scheme.get("description"),
                )
        elif scheme_type == "oauth2":
            flows = scheme.get("flows", {})
            # Simplified OAuth2 handling
            flow = flows.get("authorizationCode") or flows.get("implicit") or flows.get("password")
            if flow:
                return AuthConfig(
                    type=AuthType.OAUTH2,
                    authorization_url=flow.get("authorizationUrl"),
                    token_url=flow.get("tokenUrl"),
                    scopes=flow.get("scopes", {}),
                    description=scheme.get("description"),
                )

        return None

    def _extract_schemas(self) -> dict[str, SchemaModel]:
        """Extract data schemas from components."""
        assert self.spec is not None
        schemas = {}
        components = self.spec.get("components", {}).get("schemas", {})

        for name, schema in components.items():
            schemas[name] = self._build_schema_model(name, schema)

        return schemas

    def _openapi_type_to_python(self, openapi_type: str) -> str:
        """Convert OpenAPI type to Python type hint."""
        type_map = {
            "string": "str",
            "integer": "int",
            "number": "float",
            "boolean": "bool",
            "array": "list",
            "object": "dict",
        }
        return type_map.get(openapi_type, "Any")
