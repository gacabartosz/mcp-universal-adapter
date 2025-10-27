"""Unit tests for OpenAPI parser."""

import pytest
from pathlib import Path
from mcp_adapter.parsers import OpenAPIParser, ParserValidationError
from mcp_adapter.models import HTTPMethod, AuthType, ParameterLocation


@pytest.mark.asyncio
async def test_parse_petstore_yaml():
    """Test parsing Pet Store OpenAPI YAML file."""
    # Get path to test file
    test_file = Path(__file__).parent.parent.parent / "examples" / "demo_petstore" / "petstore-openapi.yaml"

    # Parse
    parser = OpenAPIParser(str(test_file))
    spec = await parser.parse()

    # Verify basic info
    assert spec.name == "Pet Store API"
    assert spec.version == "1.0.0"
    assert spec.description == "A simple pet store API for demonstration"

    # Verify endpoints
    assert len(spec.endpoints) == 5  # GET, POST /pets, GET, PUT, DELETE /pets/{id}

    # Verify endpoint names
    tool_names = [e.tool_name for e in spec.endpoints]
    assert "list_pets" in tool_names or "listPets" in tool_names
    assert "create_pet" in tool_names or "createPet" in tool_names
    assert "get_pet" in tool_names or "getPet" in tool_names

    # Verify auth
    assert spec.auth is not None
    assert spec.auth.type == AuthType.BEARER


@pytest.mark.asyncio
async def test_parser_validates_spec():
    """Test that parser validates OpenAPI specification."""
    test_file = Path(__file__).parent.parent.parent / "examples" / "demo_petstore" / "petstore-openapi.yaml"
    parser = OpenAPIParser(str(test_file))

    await parser.parse()
    assert parser.validate() is True


@pytest.mark.asyncio
async def test_endpoint_tool_name_generation():
    """Test that endpoint tool names are generated correctly."""
    test_file = Path(__file__).parent.parent.parent / "examples" / "demo_petstore" / "petstore-openapi.yaml"
    parser = OpenAPIParser(str(test_file))
    spec = await parser.parse()

    # Find list_pets endpoint
    list_endpoint = spec.get_endpoint_by_name("listPets")
    if not list_endpoint:
        # Try alternative naming
        list_endpoint = next((e for e in spec.endpoints if e.path == "/pets" and e.method == HTTPMethod.GET), None)

    assert list_endpoint is not None
    assert list_endpoint.method == HTTPMethod.GET
    assert list_endpoint.path == "/pets"


@pytest.mark.asyncio
async def test_endpoint_parameters():
    """Test that endpoint parameters are parsed correctly."""
    test_file = Path(__file__).parent.parent.parent / "examples" / "demo_petstore" / "petstore-openapi.yaml"
    parser = OpenAPIParser(str(test_file))
    spec = await parser.parse()

    # Find list_pets endpoint
    list_endpoint = next((e for e in spec.endpoints if e.path == "/pets" and e.method == HTTPMethod.GET), None)
    assert list_endpoint is not None

    # Check query parameters
    query_params = list_endpoint.query_parameters
    assert len(query_params) >= 1

    # Check limit parameter
    limit_param = next((p for p in query_params if p.name == "limit"), None)
    assert limit_param is not None
    assert limit_param.location == ParameterLocation.QUERY
    assert limit_param.type == "int"


@pytest.mark.asyncio
async def test_path_parameters():
    """Test that path parameters are parsed correctly."""
    test_file = Path(__file__).parent.parent.parent / "examples" / "demo_petstore" / "petstore-openapi.yaml"
    parser = OpenAPIParser(str(test_file))
    spec = await parser.parse()

    # Find get_pet endpoint (GET /pets/{petId})
    get_endpoint = next((e for e in spec.endpoints if e.path == "/pets/{petId}" and e.method == HTTPMethod.GET), None)
    assert get_endpoint is not None

    # Check path parameters
    path_params = get_endpoint.path_parameters
    assert len(path_params) == 1
    assert path_params[0].name == "petId"
    assert path_params[0].location == ParameterLocation.PATH
    assert path_params[0].required is True


@pytest.mark.asyncio
async def test_request_body():
    """Test that request body is parsed correctly."""
    test_file = Path(__file__).parent.parent.parent / "examples" / "demo_petstore" / "petstore-openapi.yaml"
    parser = OpenAPIParser(str(test_file))
    spec = await parser.parse()

    # Find create_pet endpoint (POST /pets)
    create_endpoint = next((e for e in spec.endpoints if e.path == "/pets" and e.method == HTTPMethod.POST), None)
    assert create_endpoint is not None

    # Check request body
    assert create_endpoint.request_body is not None
    assert "name" in create_endpoint.request_body.properties
    assert "species" in create_endpoint.request_body.properties


def test_parser_is_url():
    """Test URL detection."""
    parser = OpenAPIParser("https://api.example.com/openapi.json")
    assert parser.is_url("https://api.example.com/openapi.json") is True
    assert parser.is_url("http://api.example.com/openapi.json") is True
    assert parser.is_url("/path/to/file.yaml") is False
    assert parser.is_url("file.yaml") is False


def test_parser_is_file():
    """Test file detection."""
    test_file = Path(__file__).parent.parent.parent / "examples" / "demo_petstore" / "petstore-openapi.yaml"
    parser = OpenAPIParser(str(test_file))
    assert parser.is_file(str(test_file)) is True
    assert parser.is_file("nonexistent.yaml") is False
