"""Python MCP server generator."""

import os
from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader, select_autoescape

from mcp_adapter.models import (
    NormalizedAPISpec,
    AuthType,
    ParameterLocation,
    HTTPMethod,
)
from mcp_adapter.generators.base import BaseGenerator, GeneratorError


class PythonGenerator(BaseGenerator):
    """Generate Python MCP server from API specification."""

    def __init__(self, api_spec: NormalizedAPISpec):
        super().__init__(api_spec)
        # Setup Jinja2 environment
        template_dir = Path(__file__).parent.parent / "templates" / "python"
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        # Add custom filters
        self.env.filters["to_python_name"] = self._to_python_name

    def validate_spec(self) -> bool:
        """Validate API spec has required information."""
        if not self.api_spec.endpoints:
            return False
        if not self.api_spec.primary_server:
            return False
        return True

    def generate(self, output_dir: Path) -> None:
        """Generate complete Python MCP server.

        Creates:
        - server.py: Main MCP server with tools
        - pyproject.toml: Dependencies and metadata
        - README.md: Usage instructions
        - .env.example: Environment variables template
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        if not self.validate_spec():
            raise GeneratorError("Invalid API specification for generation")

        # Generate files
        self._generate_server(output_path)
        self._generate_pyproject(output_path)
        self._generate_readme(output_path)
        self._generate_env_example(output_path)

        print(f"✅ Generated Python MCP server in: {output_path}")
        print(f"   Endpoints: {len(self.api_spec.endpoints)}")
        print(f"   Tools: {len(self.api_spec.endpoints)}")

    def _generate_server(self, output_dir: Path) -> None:
        """Generate main server.py file."""
        template = self.env.get_template("server.py.jinja2")

        # Prepare context
        context = {
            "api_spec": self.api_spec,
            "endpoints": self.api_spec.endpoints,
            "has_auth": self.api_spec.auth is not None,
            "auth_type": self.api_spec.auth.type if self.api_spec.auth else None,
            "auth_name": self.api_spec.auth.name if self.api_spec.auth else "API_KEY",
            "base_url": self.api_spec.primary_server,
        }

        # Render and write
        output = template.render(**context)
        (output_dir / "server.py").write_text(output)

    def _generate_pyproject(self, output_dir: Path) -> None:
        """Generate pyproject.toml file."""
        template = self.env.get_template("pyproject.toml.jinja2")

        # Prepare context
        package_name = self._to_python_name(self.api_spec.name).replace("_", "-")
        context = {
            "package_name": package_name,
            "api_name": self.api_spec.name,
            "description": self.api_spec.description or f"MCP server for {self.api_spec.name}",
            "version": self.api_spec.version,
        }

        # Render and write
        output = template.render(**context)
        (output_dir / "pyproject.toml").write_text(output)

    def _generate_readme(self, output_dir: Path) -> None:
        """Generate README.md file."""
        template = self.env.get_template("README.md.jinja2")

        # Group endpoints by tag
        endpoints_by_tag: Dict[str, list] = {}
        for endpoint in self.api_spec.endpoints:
            tag = endpoint.tags[0] if endpoint.tags else "General"
            if tag not in endpoints_by_tag:
                endpoints_by_tag[tag] = []
            endpoints_by_tag[tag].append(endpoint)

        context = {
            "api_spec": self.api_spec,
            "endpoints_by_tag": endpoints_by_tag,
            "has_auth": self.api_spec.auth is not None,
            "auth_type": self.api_spec.auth.type if self.api_spec.auth else None,
            "total_endpoints": len(self.api_spec.endpoints),
        }

        output = template.render(**context)
        (output_dir / "README.md").write_text(output)

    def _generate_env_example(self, output_dir: Path) -> None:
        """Generate .env.example file."""
        lines = [
            "# Environment variables for MCP server",
            f"# Generated for: {self.api_spec.name}\n",
        ]

        # Add auth variables
        if self.api_spec.auth:
            if self.api_spec.auth.type == AuthType.API_KEY:
                var_name = self.api_spec.auth.name.upper()
                lines.append(f"# {self.api_spec.auth.description or 'API authentication key'}")
                lines.append(f"{var_name}=your_api_key_here\n")
            elif self.api_spec.auth.type == AuthType.BEARER:
                lines.append("# Bearer token for authentication")
                lines.append("BEARER_TOKEN=your_bearer_token_here\n")
            elif self.api_spec.auth.type == AuthType.BASIC:
                lines.append("# Basic authentication credentials")
                lines.append("API_USERNAME=your_username")
                lines.append("API_PASSWORD=your_password\n")

        # Add base URL (if configurable)
        lines.append("# API Base URL (optional, override default)")
        lines.append(f"API_BASE_URL={self.api_spec.primary_server}\n")

        (output_dir / ".env.example").write_text("\n".join(lines))

    def _to_python_name(self, name: str) -> str:
        """Convert API name to valid Python identifier."""
        # Remove special chars, replace spaces with underscores
        name = "".join(c if c.isalnum() or c == "_" else "_" for c in name)
        # Remove leading/trailing underscores
        name = name.strip("_").lower()
        # Ensure doesn't start with number
        if name and name[0].isdigit():
            name = "api_" + name
        return name or "api"
