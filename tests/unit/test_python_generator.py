"""Unit tests for Python MCP server generator."""

import pytest
from pathlib import Path
import tempfile
import shutil
from mcp_adapter.parsers import OpenAPIParser
from mcp_adapter.generators import PythonGenerator


@pytest.mark.asyncio
async def test_generator_creates_files():
    """Test that generator creates all required files."""
    # Parse Pet Store
    test_file = Path(__file__).parent.parent.parent / "examples" / "demo_petstore" / "petstore-openapi.yaml"
    parser = OpenAPIParser(str(test_file))
    spec = await parser.parse()

    # Generate in temp directory
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)

        generator = PythonGenerator(spec)
        generator.generate(output_dir)

        # Check files exist
        assert (output_dir / "server.py").exists()
        assert (output_dir / "pyproject.toml").exists()
        assert (output_dir / "README.md").exists()
        assert (output_dir / ".env.example").exists()


@pytest.mark.asyncio
async def test_generated_server_syntax():
    """Test that generated server.py has valid Python syntax."""
    # Parse Pet Store
    test_file = Path(__file__).parent.parent.parent / "examples" / "demo_petstore" / "petstore-openapi.yaml"
    parser = OpenAPIParser(str(test_file))
    spec = await parser.parse()

    # Generate
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        generator = PythonGenerator(spec)
        generator.generate(output_dir)

        # Try to compile the generated server.py
        server_code = (output_dir / "server.py").read_text()
        try:
            compile(server_code, "server.py", "exec")
        except SyntaxError as e:
            pytest.fail(f"Generated server.py has syntax error: {e}")


@pytest.mark.asyncio
async def test_generated_server_contains_tools():
    """Test that generated server contains all tools."""
    # Parse Pet Store
    test_file = Path(__file__).parent.parent.parent / "examples" / "demo_petstore" / "petstore-openapi.yaml"
    parser = OpenAPIParser(str(test_file))
    spec = await parser.parse()

    # Generate
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        generator = PythonGenerator(spec)
        generator.generate(output_dir)

        server_code = (output_dir / "server.py").read_text()

        # Check that all endpoints have corresponding functions
        for endpoint in spec.endpoints:
            tool_name = endpoint.tool_name
            assert f"async def {tool_name}(" in server_code, f"Function {tool_name} not found in generated server"


@pytest.mark.asyncio
async def test_generated_server_has_auth():
    """Test that generated server includes authentication handling."""
    test_file = Path(__file__).parent.parent.parent / "examples" / "demo_petstore" / "petstore-openapi.yaml"
    parser = OpenAPIParser(str(test_file))
    spec = await parser.parse()

    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        generator = PythonGenerator(spec)
        generator.generate(output_dir)

        server_code = (output_dir / "server.py").read_text()

        # Check for auth-related code
        assert "load_dotenv()" in server_code
        assert "get_headers()" in server_code

        # Check for Bearer auth (from Pet Store)
        if spec.auth and spec.auth.type.value == "bearer":
            assert "BEARER_TOKEN" in server_code
            assert "Authorization" in server_code


@pytest.mark.asyncio
async def test_generated_pyproject_valid():
    """Test that generated pyproject.toml is valid."""
    test_file = Path(__file__).parent.parent.parent / "examples" / "demo_petstore" / "petstore-openapi.yaml"
    parser = OpenAPIParser(str(test_file))
    spec = await parser.parse()

    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        generator = PythonGenerator(spec)
        generator.generate(output_dir)

        pyproject_content = (output_dir / "pyproject.toml").read_text()

        # Check required fields
        assert "[project]" in pyproject_content
        assert "name =" in pyproject_content
        assert "version =" in pyproject_content
        assert "mcp>=" in pyproject_content
        assert "httpx>=" in pyproject_content
        assert "python-dotenv>=" in pyproject_content


@pytest.mark.asyncio
async def test_generated_readme_complete():
    """Test that generated README has all sections."""
    test_file = Path(__file__).parent.parent.parent / "examples" / "demo_petstore" / "petstore-openapi.yaml"
    parser = OpenAPIParser(str(test_file))
    spec = await parser.parse()

    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        generator = PythonGenerator(spec)
        generator.generate(output_dir)

        readme_content = (output_dir / "README.md").read_text()

        # Check sections
        assert "# " in readme_content  # Title
        assert "## Overview" in readme_content
        assert "## Installation" in readme_content
        assert "## Configuration" in readme_content
        assert "## Usage" in readme_content
        assert "## Available Tools" in readme_content


@pytest.mark.asyncio
async def test_generated_env_example():
    """Test that .env.example contains correct variables."""
    test_file = Path(__file__).parent.parent.parent / "examples" / "demo_petstore" / "petstore-openapi.yaml"
    parser = OpenAPIParser(str(test_file))
    spec = await parser.parse()

    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        generator = PythonGenerator(spec)
        generator.generate(output_dir)

        env_content = (output_dir / ".env.example").read_text()

        # Check base variables
        assert "API_BASE_URL" in env_content

        # Check auth variables
        if spec.auth:
            if spec.auth.type.value == "bearer":
                assert "BEARER_TOKEN" in env_content
            elif spec.auth.type.value == "api_key":
                assert spec.auth.name.upper() in env_content


def test_generator_validates_spec():
    """Test that generator validates spec before generation."""
    from mcp_adapter.models import NormalizedAPISpec

    # Create minimal spec (no endpoints - should fail validation)
    spec = NormalizedAPISpec(
        name="Test API",
        version="1.0.0",
        endpoints=[],  # Empty - should fail
    )

    generator = PythonGenerator(spec)
    assert generator.validate_spec() is False
