# MCP Universal Adapter - Quickstart Guide

Get started with MCP Universal Adapter in 5 minutes.

---

## Prerequisites

- Python 3.10 or higher
- Poetry (recommended) or pip

---

## Installation

### Option 1: Using Poetry (Recommended)

```bash
# Clone repository
git clone https://github.com/gacabartosz/mcp-universal-adapter.git
cd mcp-universal-adapter

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Option 2: Using pip

```bash
# Clone repository
git clone https://github.com/gacabartosz/mcp-universal-adapter.git
cd mcp-universal-adapter

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

---

## Quick Demo: Pet Store API

### 1. Generate MCP Server

```bash
# Generate from included example
mcp-adapt generate examples/demo_petstore/petstore-openapi.yaml \
    --output ./my-petstore-mcp

# Or generate from URL
# mcp-adapt generate https://petstore.swagger.io/v2/swagger.json \
#     --output ./swagger-petstore-mcp
```

### 2. Install Generated Server

```bash
cd my-petstore-mcp

# Install dependencies
pip install -e .
```

### 3. Configure (if auth required)

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your credentials
# For Pet Store example with Bearer auth:
# BEARER_TOKEN=your_token_here
```

### 4. Run MCP Server

```bash
python server.py
```

You should see:
```
🚀 Starting Pet Store API MCP Server
   Base URL: https://petstore.example.com/api/v1
   Tools: 5
```

### 5. Use in Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "petstore": {
      "command": "python",
      "args": ["/absolute/path/to/my-petstore-mcp/server.py"],
      "env": {
        "BEARER_TOKEN": "your_token_here"
      }
    }
  }
}
```

Restart Claude Desktop, then try:
- "List all pets in the pet store"
- "Create a new pet named Fluffy"
- "Get details for pet ID 1"

---

## Generate from Different Sources

### From Local File

```bash
# YAML
mcp-adapt generate ./api-spec.yaml --output ./my-mcp

# JSON
mcp-adapt generate ./openapi.json --output ./my-mcp
```

### From URL

```bash
# OpenAPI from URL
mcp-adapt generate https://api.example.com/openapi.json \
    --output ./example-mcp
```

### From Public APIs

```bash
# JSONPlaceholder (no auth)
mcp-adapt generate https://jsonplaceholder.typicode.com/openapi.json \
    --output ./jsonplaceholder-mcp

# GitHub API (requires auth)
mcp-adapt generate https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.yaml \
    --output ./github-mcp
```

---

## Testing Generated Server

### Option 1: Manual Test

```python
# test_server.py
import asyncio
from mcp import ClientSession, StdioServerParameters

async def test():
    # Connect to server
    server = StdioServerParameters(
        command="python",
        args=["server.py"]
    )

    async with ClientSession(server) as session:
        # List available tools
        tools = await session.list_tools()
        print(f"Available tools: {[t.name for t in tools]}")

        # Call a tool (example: list_pets)
        result = await session.call_tool("list_pets", {"limit": 5})
        print(f"Result: {result}")

asyncio.run(test())
```

### Option 2: Using MCP Inspector

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Inspect your server
mcp-inspector python server.py
```

---

## Common Use Cases

### 1. Internal Company API

```bash
# Generate MCP for your company's API
mcp-adapt generate https://api.mycompany.com/openapi.json \
    --output ./company-api-mcp

cd company-api-mcp
pip install -e .

# Configure auth
cp .env.example .env
# Edit .env: Add API_KEY=your_internal_api_key

python server.py
```

### 2. Third-Party Service Integration

```bash
# Example: Weather API
mcp-adapt generate https://api.weather.com/openapi.json \
    --output ./weather-mcp

# Example: Payment Gateway
mcp-adapt generate https://api.stripe.com/openapi.json \
    --output ./stripe-mcp
```

### 3. Microservices Orchestration

```bash
# Generate MCP for each microservice
mcp-adapt generate http://users-service/openapi.json --output ./users-mcp
mcp-adapt generate http://orders-service/openapi.json --output ./orders-mcp
mcp-adapt generate http://inventory-service/openapi.json --output ./inventory-mcp

# Use Claude to orchestrate across services
# "Create a user, place an order, and check inventory"
```

---

## Troubleshooting

### Issue: Import Errors

```bash
# Make sure dependencies are installed
pip install -e .

# Or with Poetry
poetry install
```

### Issue: Server Won't Start

```bash
# Check if required environment variables are set
cat .env

# Verify server.py syntax
python -m py_compile server.py
```

### Issue: Authentication Errors

```bash
# Verify credentials in .env
cat .env

# Test API credentials directly
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.example.com/endpoint
```

### Issue: Can't Find OpenAPI Spec

```bash
# Some APIs expose OpenAPI at different paths:
# /openapi.json
# /swagger.json
# /api-docs
# /docs/openapi.json

# Try listing available endpoints
curl https://api.example.com/ | jq
```

---

## CLI Reference

### Commands

```bash
# Generate MCP server
mcp-adapt generate <source> [options]

# List available presets
mcp-adapt presets

# Show version
mcp-adapt version

# Get help
mcp-adapt --help
```

### Options

```
--output, -o PATH        Output directory (default: ./generated_server)
--language, -l LANG      Target language: python, typescript (default: python)
--preset, -p NAME        Use preset configuration
```

---

## Next Steps

1. **Read the Full Documentation**
   - [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md) - Roadmap and vision
   - [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute

2. **Try Advanced Features** (Coming Soon)
   - API Discovery Mode (without OpenAPI spec)
   - AI-Enhanced Generation
   - Custom Presets

3. **Join the Community**
   - Star the repo: https://github.com/gacabartosz/mcp-universal-adapter
   - Report issues
   - Share your generated MCPs
   - Contribute presets

---

## Examples

Check the `examples/` directory for complete examples:
- `demo_petstore/` - Pet Store API demo
- `stripe_payments/` - Stripe integration (coming soon)
- `github_automation/` - GitHub API (coming soon)

---

## Getting Help

- **Documentation**: https://github.com/gacabartosz/mcp-universal-adapter/docs
- **Issues**: https://github.com/gacabartosz/mcp-universal-adapter/issues
- **Email**: gaca.bartosz@gmail.com

---

**Happy MCP Building!** 🚀
