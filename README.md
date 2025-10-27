# MCP Universal Adapter

> **⚠️ PROJECT STATUS: Work in Progress**
> This project is in early development. Core functionality is being implemented. Contributions welcome!

**Transform any API into a fully functional MCP server in seconds, not days.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-alpha-orange.svg)](https://github.com/gacabartosz/mcp-universal-adapter)

---

## The Problem

Building MCP (Model Context Protocol) servers manually is slow and repetitive:
- 73.6k+ stars on `awesome-mcp-servers` shows massive demand
- Each MCP server currently takes **2-5 days** to code
- There are **15,000+ public APIs**, but only ~100 have MCP adapters
- Developers write the same boilerplate over and over

## The Solution

**MCP Universal Adapter** automatically generates production-ready MCP servers from any API specification:

```bash
# Transform Stripe API into MCP server
mcp-adapt --preset stripe --api-key sk_test_xxx

# Done! Now use in Claude/Cursor:
# "Create a Stripe customer for john@example.com and charge $99"
```

**Time reduction:** 5 days → 5 minutes ⚡

---

## 🎯 Vision

Make **every API in the world accessible to AI** by eliminating the manual adapter-writing bottleneck.

One universal tool that unlocks thousands of APIs for the AI ecosystem.

---

## ✨ Features (Planned)

### Core Capabilities
- ✅ **OpenAPI 3.x Support** - Parse any OpenAPI specification
- ✅ **GraphQL Support** - Handle GraphQL schemas
- ✅ **REST Discovery** - Auto-detect endpoints from base URL
- ✅ **Multiple Languages** - Generate Python or TypeScript servers
- ✅ **Authentication** - Support for API Key, Bearer, OAuth2

### Pre-configured Presets
- 🔄 **Stripe** - Complete payments integration
- 🔄 **GitHub** - Repository and issue management
- 🔄 **OpenAI** - AI model composition
- 🔄 **Slack** - Team communication automation
- 🔄 **SendGrid** - Email automation

### Advanced Features
- 🔄 **HAR Import** - Import from browser DevTools
- 🔄 **Postman Collections** - Convert Postman to MCP
- 🔄 **Auto-generated Tests** - Pytest/Jest test suites
- 🔄 **Live Reload** - Hot reload during development
- 🔄 **VS Code Extension** - IDE integration

**Legend:**
- ✅ In Progress
- 🔄 Planned

---

## 🚀 Quick Start

> **Note:** Installation instructions will be available when v0.1.0 is released.

### Installation (Coming Soon)

```bash
pip install mcp-universal-adapter
```

### Basic Usage

```bash
# Generate from OpenAPI URL
mcp-adapt https://api.example.com/openapi.json \
  --output my-mcp-server

# Use preset for popular APIs
mcp-adapt --preset stripe --api-key sk_test_xxx

# Discover REST endpoints
mcp-adapt https://api.example.com \
  --discover \
  --output example-mcp
```

### Example: Stripe Payments

```bash
mcp-adapt --preset stripe --api-key sk_test_YOUR_KEY
```

Now in Claude/Cursor:
```
User: "Create a customer for john@example.com and charge $99 for Premium Plan"
AI: [Uses generated MCP server to]
    1. Create Stripe customer
    2. Create payment intent
    3. Process charge
    4. Return confirmation
```

---

## 🏗️ Architecture

```
API Input (OpenAPI/GraphQL/REST)
         ↓
    Parser Layer
         ↓
  Schema Normalizer
         ↓
   MCP Generator
         ↓
  Code Templates (Jinja2)
         ↓
MCP Server Output (Python/TS)
         ↓
  Validation & Testing
```

### Components

1. **Parsers** - Extract API structure from various formats
2. **Normalizer** - Unified API representation
3. **Generator** - Creates MCP server code
4. **Templates** - Language-specific code templates
5. **Validator** - Tests generated servers

---

## 📚 Documentation

> Documentation is being written. Check back soon!

- [Quickstart Guide](docs/quickstart.md) - Coming soon
- [API Reference](docs/api_reference.md) - Coming soon
- [Presets Guide](docs/presets.md) - Coming soon
- [Cookbook](docs/cookbook/) - Example recipes

---

## 🛣️ Roadmap

### Sprint 1 (Days 1-5): Foundation
- [ ] Project setup & repository structure
- [ ] OpenAPI 3.x parser
- [ ] Python MCP generator
- [ ] CLI interface (Typer)
- [ ] First working demo with Stripe

### Sprint 2 (Days 6-10): Polish & Presets
- [ ] Error handling & validation
- [ ] 5 API presets (Stripe, GitHub, OpenAI, Slack, SendGrid)
- [ ] Comprehensive documentation
- [ ] v0.1.0 release

### Sprint 3 (Days 11-14): Advanced Features
- [ ] GraphQL support
- [ ] REST endpoint discovery
- [ ] HAR file import
- [ ] VS Code extension

### Future
- TypeScript generator
- Web playground (Streamlit)
- GitHub Action
- Docker images
- Community presets marketplace

---

## 💡 Use Cases

### 1. Payments (Stripe)
```bash
mcp-adapt --preset stripe
# Enable: "Process $99 payment for customer@email.com"
```

### 2. GitHub Automation
```bash
mcp-adapt --preset github --token ghp_xxx
# Enable: "Create urgent bug issue in myapp repo"
```

### 3. Team Communication (Slack)
```bash
mcp-adapt --preset slack --workspace myteam
# Enable: "Post 'Deployment done' to #engineering"
```

### 4. Custom Internal APIs
```bash
mcp-adapt https://api.mycompany.com/swagger.json
# Enable your company's API for AI agents!
```

---

## 🤝 Contributing

**We're in early development and would love your help!**

### Priority Contributions Needed:
1. **API Presets** - Add support for popular APIs
2. **TypeScript Generator** - Implement TS template
3. **GraphQL Parser** - Complete GraphQL support
4. **Documentation** - Write guides and examples
5. **Testing** - Improve test coverage

### How to Contribute:

```bash
# 1. Fork the repository
# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/mcp-universal-adapter.git
cd mcp-universal-adapter

# 3. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 4. Install dependencies
pip install -e ".[dev]"

# 5. Create feature branch
git checkout -b feature/amazing-feature

# 6. Make changes and test
pytest tests/

# 7. Commit and push
git commit -m "feat: add amazing feature"
git push origin feature/amazing-feature

# 8. Open Pull Request
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 🎯 Success Metrics

**Launch Goals (First 30 days):**
- 5,000+ GitHub stars
- 100+ generated MCP servers
- 20+ API presets
- Listed in `awesome-mcp-servers`

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=gacabartosz/mcp-universal-adapter&type=Date)](https://star-history.com/#gacabartosz/mcp-universal-adapter&Date)

---

## 📧 Contact

**Bartosz Gaca** - AI & Automation Strategist
- Email: gaca.bartosz@gmail.com
- Website: [bartoszgaca.pl](https://bartoszgaca.pl)
- GitHub: [@gacabartosz](https://github.com/gacabartosz)

---

## 🙏 Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io) - The protocol that makes this possible
- [Anthropic](https://anthropic.com) - For Claude and MCP specification
- [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) - Inspiration and community

---

**Built with ❤️ to democratize AI-API integration**

*Stop writing adapters. Start building.*
