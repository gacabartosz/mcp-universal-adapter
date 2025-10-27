"""Command-line interface for MCP Universal Adapter."""

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(
    name="mcp-adapt",
    help="Transform any API into a fully functional MCP server",
    add_completion=False,
)
console = Console()


@app.command()
def version():
    """Show version information."""
    from mcp_adapter import __author__, __version__

    console.print(f"[bold green]MCP Universal Adapter[/bold green] v{__version__}")
    console.print(f"Author: {__author__}")
    console.print("\n[dim]Transform any API into MCP server in seconds[/dim]")


@app.command()
def generate(
    source: str,
    output: str = typer.Option(  # noqa: B008
        "./generated_server", "--output", "-o", help="Output directory"
    ),
    language: str = typer.Option(  # noqa: B008
        "python", "--language", "-l", help="Target language (python/typescript)"
    ),
    preset: str = typer.Option(
        None, "--preset", "-p", help="Use preset configuration"
    ),  # noqa: B008
):
    """Generate MCP server from API specification.

    Args:
        source: API specification URL or file path

    Examples:
        mcp-adapt generate https://api.example.com/openapi.json
        mcp-adapt generate ./api-spec.yaml --output my-server
        mcp-adapt generate https://jsonplaceholder.typicode.com/openapi.json
    """
    output_path = Path(output)
    import asyncio

    from mcp_adapter.generators import PythonGenerator
    from mcp_adapter.parsers import OpenAPIParser

    console.print("\n[bold cyan]🔧 MCP Universal Adapter[/bold cyan]")
    console.print(f"Source: {source}")
    console.print(f"Output: {output}")
    console.print(f"Language: {language}\n")

    try:
        # Step 1: Parse API specification
        console.print("[bold]Step 1:[/bold] Parsing API specification...")
        parser = OpenAPIParser(source)
        api_spec = asyncio.run(parser.parse())

        console.print(f"✅ Parsed: {api_spec.name} v{api_spec.version}")
        console.print(f"   Endpoints: {len(api_spec.endpoints)}")
        console.print(f"   Auth: {api_spec.auth.type if api_spec.auth else 'None'}\n")

        # Step 2: Generate MCP server
        console.print("[bold]Step 2:[/bold] Generating MCP server...")

        if language.lower() == "python":
            generator = PythonGenerator(api_spec)
        else:
            console.print(f"[red]Error:[/red] Unsupported language: {language}")
            console.print("Currently supported: python")
            return

        generator.generate(output_path)

        # Step 3: Success!
        console.print("\n[bold green]✨ Success![/bold green]")
        console.print(f"\nGenerated MCP server in: [cyan]{output}[/cyan]")
        console.print("\n[bold]Next steps:[/bold]")
        console.print(f"  1. cd {output}")
        console.print("  2. pip install -e .")
        if api_spec.auth:
            console.print("  3. Copy .env.example to .env and add your credentials")
            console.print("  4. python server.py")
        else:
            console.print("  3. python server.py")

    except Exception as e:
        console.print(f"\n[red]❌ Error:[/red] {str(e)}")
        import traceback

        console.print(f"\n[dim]{traceback.format_exc()}[/dim]")
        raise typer.Exit(code=1) from e


@app.command()
def presets():
    """List available API presets."""
    console.print("\n[bold]Available Presets:[/bold]\n")

    presets_list = [
        ("stripe", "Stripe Payments API", "🔄 Planned"),
        ("github", "GitHub REST & GraphQL API", "🔄 Planned"),
        ("openai", "OpenAI API", "🔄 Planned"),
        ("slack", "Slack API", "🔄 Planned"),
        ("sendgrid", "SendGrid Email API", "🔄 Planned"),
    ]

    for name, description, status in presets_list:
        console.print(f"  • [bold cyan]{name}[/bold cyan] - {description} [{status}]")

    console.print("\n[dim]More presets coming soon! Contributions welcome.[/dim]\n")


@app.command()
def discover(
    base_url: str,
    output: str = typer.Option(  # noqa: B008
        "./api_spec.yaml", "--output", "-o", help="Output file for discovered spec"
    ),
):
    """Discover API endpoints from base URL.

    Args:
        base_url: Base URL of the API to discover

    Example:
        mcp-adapt discover https://api.example.com
    """
    output_path = Path(output)  # noqa: F841 - will be used when discovery implemented
    console.print(
        Panel.fit(
            "[bold yellow]⚠️  Feature in Development[/bold yellow]\n\n"
            "REST endpoint discovery is currently being implemented.\n"
            f"Base URL: {base_url}\n"
            f"Output: {output}",
            title="API Discovery",
        )
    )

    # TODO: Implement discovery logic
    # 1. Probe common endpoints
    # 2. Analyze responses
    # 3. Generate OpenAPI specification


def main():
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
