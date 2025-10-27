"""Unified API specification models.

All parsers (OpenAPI, GraphQL, REST discovery) convert to these models.
This provides a consistent interface for generators regardless of source format.
"""

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class HTTPMethod(str, Enum):
    """HTTP methods."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class ParameterLocation(str, Enum):
    """Location of parameter in HTTP request."""

    QUERY = "query"
    HEADER = "header"
    PATH = "path"
    BODY = "body"
    COOKIE = "cookie"


class AuthType(str, Enum):
    """Authentication types."""

    NONE = "none"
    API_KEY = "api_key"
    BEARER = "bearer"
    BASIC = "basic"
    OAUTH2 = "oauth2"
    CUSTOM = "custom"


class PropertySchema(BaseModel):
    """Schema for a property in request/response."""

    name: str
    type: str  # string, number, integer, boolean, array, object
    description: str | None = None
    required: bool = False
    default: Any | None = None
    enum: list[Any] | None = None
    format: str | None = None  # email, date-time, uri, etc.
    pattern: str | None = None
    min_length: int | None = None
    max_length: int | None = None
    minimum: float | None = None
    maximum: float | None = None
    items: Optional["PropertySchema"] = None  # For arrays
    properties: dict[str, "PropertySchema"] | None = None  # For objects
    example: Any | None = None


class SchemaModel(BaseModel):
    """Request or response schema."""

    name: str
    description: str | None = None
    properties: dict[str, PropertySchema] = Field(default_factory=dict)
    required: list[str] = Field(default_factory=list)
    example: dict[str, Any] | None = None


class Parameter(BaseModel):
    """API parameter (query, path, header, or body)."""

    model_config = ConfigDict(populate_by_name=True)

    name: str
    location: ParameterLocation
    type: str  # Python type hint string
    description: str | None = None
    required: bool = False
    default: Any | None = None
    param_schema: PropertySchema | None = Field(default=None, alias="schema")  # Detailed schema
    example: Any | None = None


class Endpoint(BaseModel):
    """API endpoint definition."""

    # Basic info
    path: str  # /api/users/{id}
    method: HTTPMethod
    operation_id: str | None = None  # Unique identifier
    summary: str | None = None  # Short description
    description: str | None = None  # Long description
    tags: list[str] = Field(default_factory=list)  # Categories/groups

    # Parameters
    parameters: list[Parameter] = Field(default_factory=list)
    request_body: SchemaModel | None = None

    # Response
    response_schema: SchemaModel | None = None
    response_examples: dict[str, Any] = Field(default_factory=dict)

    # Additional metadata
    deprecated: bool = False
    external_docs: str | None = None

    @property
    def tool_name(self) -> str:
        """Generate MCP tool name from endpoint.

        Examples:
            GET /users -> list_users
            GET /users/{id} -> get_user
            POST /users -> create_user
            PUT /users/{id} -> update_user
            DELETE /users/{id} -> delete_user
        """
        if self.operation_id:
            # Use OpenAPI operationId if available
            return self.operation_id.lower().replace(" ", "_")

        # Generate from method + path
        path_parts = [p for p in self.path.split("/") if p and not p.startswith("{")]
        resource = path_parts[-1] if path_parts else "resource"

        method_map = {
            HTTPMethod.GET: "get" if "{" in self.path else "list",
            HTTPMethod.POST: "create",
            HTTPMethod.PUT: "update",
            HTTPMethod.PATCH: "update",
            HTTPMethod.DELETE: "delete",
        }

        prefix = method_map.get(self.method, self.method.value.lower())
        return f"{prefix}_{resource}".lower()

    @property
    def path_parameters(self) -> list[Parameter]:
        """Get only path parameters."""
        return [p for p in self.parameters if p.location == ParameterLocation.PATH]

    @property
    def query_parameters(self) -> list[Parameter]:
        """Get only query parameters."""
        return [p for p in self.parameters if p.location == ParameterLocation.QUERY]

    @property
    def header_parameters(self) -> list[Parameter]:
        """Get only header parameters."""
        return [p for p in self.parameters if p.location == ParameterLocation.HEADER]


class AuthConfig(BaseModel):
    """Authentication configuration."""

    type: AuthType
    name: str = "auth"  # Parameter name for API key
    location: ParameterLocation = ParameterLocation.HEADER  # For API key
    scheme: str | None = None  # For HTTP auth (Bearer, Basic)
    description: str | None = None

    # OAuth2 specific
    authorization_url: str | None = None
    token_url: str | None = None
    scopes: dict[str, str] = Field(default_factory=dict)


class ServerConfig(BaseModel):
    """API server configuration."""

    url: str
    description: str | None = None
    variables: dict[str, str] = Field(default_factory=dict)


class NormalizedAPISpec(BaseModel):
    """Unified API specification.

    This is the normalized format that all parsers convert to.
    Generators work with this format to produce MCP servers.
    """

    # Metadata
    name: str
    version: str = "1.0.0"
    description: str | None = None
    base_url: str | None = None

    # Servers
    servers: list[ServerConfig] = Field(default_factory=list)

    # Endpoints
    endpoints: list[Endpoint] = Field(default_factory=list)

    # Authentication
    auth: AuthConfig | None = None

    # Data models
    schemas: dict[str, SchemaModel] = Field(default_factory=dict)

    # Additional metadata
    contact: dict[str, str] | None = None
    license: dict[str, str] | None = None
    external_docs: str | None = None
    tags: list[dict[str, str]] = Field(default_factory=list)

    # Source info
    source_format: str = "unknown"  # openapi, graphql, rest, har
    source_url: str | None = None

    def get_endpoint_by_name(self, name: str) -> Endpoint | None:
        """Find endpoint by tool name."""
        for endpoint in self.endpoints:
            if endpoint.tool_name == name:
                return endpoint
        return None

    def get_endpoints_by_tag(self, tag: str) -> list[Endpoint]:
        """Get all endpoints with specific tag."""
        return [e for e in self.endpoints if tag in e.tags]

    @property
    def primary_server(self) -> str | None:
        """Get primary server URL."""
        if self.base_url:
            return self.base_url
        if self.servers:
            return self.servers[0].url
        return None

    def summary(self) -> str:
        """Generate summary of API."""
        return (
            f"{self.name} v{self.version}\n"
            f"Endpoints: {len(self.endpoints)}\n"
            f"Auth: {self.auth.type if self.auth else 'None'}\n"
            f"Base URL: {self.primary_server or 'Not specified'}"
        )


# Update forward references
PropertySchema.model_rebuild()
