# MCP Universal Adapter - Development Plan

**Status:** Pre-Alpha (v0.0.1)
**Target:** v0.1.0 MVP
**Timeline:** 3 Sprints (~14 days)

---

## 🎯 Vision & Innovation

### Core Idea
Transform any API into MCP server **automatically** by:
1. **Traditional approach:** Parse OpenAPI/GraphQL specs → Generate code
2. **🚀 INNOVATIVE approach:** AI learns API by exploration → Generate intelligent adapters

### Key Innovation: AI-Powered API Learning

Instead of just parsing static specs, the system will:

```
┌─────────────────────────────────────────┐
│  1. User provides: API base URL         │
│     + optional auth                     │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│  2. AI Exploration Agent:               │
│     • Probes common endpoints           │
│     • Analyzes response patterns        │
│     • Infers parameter types            │
│     • Discovers relationships           │
│     • Learns authentication flows       │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│  3. Smart Generator:                    │
│     • Generates context-aware MCP tools │
│     • Creates semantic descriptions     │
│     • Auto-generates validation         │
│     • Includes example usage            │
└─────────────────────────────────────────┘
```

**Why this is powerful:**
- Works with APIs that don't have OpenAPI specs
- Learns actual behavior vs. documented behavior
- Generates better tool descriptions for LLMs
- Auto-discovers undocumented features

---

## 📋 Sprint 1: Foundation (Days 1-5)

### Phase 1.1: Core Parser (Day 1-2)
**Goal:** Parse OpenAPI 3.x specifications

**Files to create:**
- [x] `src/mcp_adapter/parsers/base.py` - Abstract parser interface
- [x] `src/mcp_adapter/parsers/openapi.py` - OpenAPI parser
- [x] `src/mcp_adapter/models/api_spec.py` - Unified API models

**Features:**
```python
class OpenAPIParser:
    def parse(url_or_file: str) -> NormalizedAPISpec:
        """Parse OpenAPI spec into unified format"""

    def extract_endpoints() -> List[Endpoint]:
        """Extract all endpoints with methods"""

    def extract_auth() -> AuthConfig:
        """Extract authentication requirements"""

    def extract_models() -> List[SchemaModel]:
        """Extract request/response schemas"""
```

**Deliverable:**
- Parser that converts OpenAPI → internal representation
- Unit tests with real-world OpenAPI examples
- Support for auth: API Key, Bearer Token, OAuth2

---

### Phase 1.2: Basic Python Generator (Day 3-4)
**Goal:** Generate working Python MCP server

**Files to create:**
- [x] `src/mcp_adapter/generators/python.py` - Python generator
- [x] `src/mcp_adapter/templates/python/server.py.jinja2` - Server template
- [x] `src/mcp_adapter/templates/python/tool.py.jinja2` - Tool template
- [x] `src/mcp_adapter/templates/python/pyproject.toml.jinja2` - Dependencies

**Template structure:**
```python
# Generated server.py
from mcp.server import Server
import httpx

server = Server("{{api_name}}-mcp")

{% for endpoint in endpoints %}
@server.tool()
async def {{endpoint.name}}(
    {% for param in endpoint.parameters %}
    {{param.name}}: {{param.type}},
    {% endfor %}
) -> dict:
    """{{endpoint.description}}

    Generated from: {{endpoint.method}} {{endpoint.path}}
    """
    async with httpx.AsyncClient() as client:
        response = await client.{{endpoint.method.lower()}}(
            "{{base_url}}{{endpoint.path}}",
            json={% if endpoint.has_body %}body{% else %}None{% endif %},
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
        return response.json()
{% endfor %}
```

**Deliverable:**
- Working Python MCP server generation
- Supports GET, POST, PUT, DELETE
- Includes error handling
- Generated pyproject.toml with dependencies

---

### Phase 1.3: First Demo (Day 5)
**Goal:** Proof of concept with real API

**Target:** JSONPlaceholder (simple, no auth needed)
- URL: https://jsonplaceholder.typicode.com
- Endpoints: posts, comments, users, todos

**Commands:**
```bash
# Generate MCP server
cd /tmp/mcp-universal-adapter
poetry run mcp-adapt https://jsonplaceholder.typicode.com/openapi.json \
  --output ./demo_generated/jsonplaceholder

# Test generated server
cd demo_generated/jsonplaceholder
python server.py

# Use in Claude Code
# "Get all posts from JSONPlaceholder"
# "Create a new todo item"
```

**Success criteria:**
- ✅ Generated server runs without errors
- ✅ All CRUD operations work
- ✅ Can be used in Claude/Cursor
- ✅ Generated code is readable

---

## 📋 Sprint 2: AI Enhancement (Days 6-10)

### Phase 2.1: API Explorer Agent (Day 6-7)
**Goal:** AI that learns API by probing it

**Files to create:**
- [x] `src/mcp_adapter/explorer/agent.py` - AI exploration agent
- [x] `src/mcp_adapter/explorer/probes.py` - Common probing strategies
- [x] `src/mcp_adapter/explorer/analyzer.py` - Response pattern analyzer

**How it works:**
```python
class APIExplorerAgent:
    def __init__(self, base_url: str, auth: Optional[dict]):
        self.llm = AnthropicClient()  # Claude for analysis

    async def explore(self) -> DiscoveredAPI:
        """Intelligently explore API"""
        # 1. Probe common paths
        endpoints = await self._probe_common_endpoints()

        # 2. Analyze responses with Claude
        patterns = await self._analyze_patterns(endpoints)

        # 3. Infer relationships
        relationships = await self._infer_relationships(patterns)

        # 4. Generate OpenAPI-like spec
        return self._synthesize_spec(patterns, relationships)

    async def _probe_common_endpoints(self):
        """Try common REST patterns"""
        paths = [
            "/api/v1/users", "/users", "/api/users",
            "/api/v1/posts", "/posts", "/api/posts",
            "/health", "/status", "/version"
        ]
        # Smart probing with rate limiting

    async def _analyze_patterns(self, responses):
        """Use Claude to understand API patterns"""
        prompt = f"""
        Analyze these API responses and identify:
        1. Resource types and their schemas
        2. Naming conventions
        3. Pagination patterns
        4. Authentication requirements
        5. Relationships between resources

        Responses: {responses}
        """
        analysis = await self.llm.complete(prompt)
        return analysis
```

**Key innovation:**
- LLM analyzes actual API behavior
- Learns conventions not in docs
- Discovers undocumented endpoints
- Infers parameter constraints from examples

---

### Phase 2.2: Smart Generator (Day 8-9)
**Goal:** Generate better MCP tools using AI insights

**Features:**
```python
class SmartPythonGenerator(PythonGenerator):
    def generate_tool_description(self, endpoint: Endpoint) -> str:
        """Use LLM to write clear tool descriptions for AI agents"""

    def generate_validation(self, param: Parameter, examples: List) -> str:
        """Infer validation rules from examples"""

    def generate_examples(self, endpoint: Endpoint) -> List[Example]:
        """Create realistic usage examples"""

    def group_endpoints(self, endpoints: List[Endpoint]) -> Dict[str, List]:
        """Semantically group related endpoints"""
```

**Example output:**
```python
@server.tool()
async def create_user(
    name: str,  # User's full name (2-100 chars)
    email: str,  # Valid email address
    role: Literal["admin", "user", "guest"] = "user"  # Inferred from examples!
) -> dict:
    """
    Create a new user account.

    This endpoint creates a user with the specified details.
    After creation, a welcome email is automatically sent.

    Example usage:
        create_user(name="John Doe", email="john@example.com", role="user")

    Returns:
        dict: Created user object with id, name, email, created_at

    Raises:
        ValidationError: If email is invalid or name too short
        ConflictError: If email already exists
    """
```

---

### Phase 2.3: Presets with Learning (Day 10)
**Goal:** Smart presets that enhance static configs

**Create presets:**
- [x] `src/mcp_adapter/presets/stripe.py`
- [x] `src/mcp_adapter/presets/github.py`
- [x] `src/mcp_adapter/presets/base.py`

**Preset + AI approach:**
```python
class StripePreset(BasePreset):
    openapi_url = "https://raw.githubusercontent.com/stripe/openapi/master/openapi/spec3.json"

    async def enhance(self) -> EnhancedSpec:
        """Enhance static spec with AI learning"""
        # 1. Parse OpenAPI
        spec = await self.parser.parse(self.openapi_url)

        # 2. Test real API (if API key provided)
        if self.api_key:
            explorer = APIExplorerAgent(
                "https://api.stripe.com",
                {"Authorization": f"Bearer {self.api_key}"}
            )
            insights = await explorer.explore()

            # 3. Merge static spec + learned behavior
            spec = self._merge(spec, insights)

        return spec

    def priority_tools(self) -> List[str]:
        """Most commonly used Stripe operations"""
        return [
            "create_customer",
            "create_payment_intent",
            "create_charge",
            "list_customers"
        ]
```

---

## 📋 Sprint 3: Polish & Release (Days 11-14)

### Phase 3.1: CLI Enhancement (Day 11)
**Commands:**
```bash
# Traditional mode
mcp-adapt https://api.example.com/openapi.json

# 🚀 AI Learning mode
mcp-adapt https://api.example.com --learn --api-key xxx

# Interactive mode
mcp-adapt --interactive
> Enter API base URL: https://api.example.com
> Enter auth method: [1] API Key [2] Bearer [3] OAuth2
> API Key: sk_test_xxx
> 🔍 Exploring API... found 12 endpoints
> ✅ Generated MCP server in ./example-mcp/

# Preset mode with learning
mcp-adapt --preset stripe --api-key sk_test_xxx --enhance
```

---

### Phase 3.2: Testing & Documentation (Day 12-13)
- Unit tests (>80% coverage)
- Integration tests with real APIs
- Documentation: Quickstart, API Reference
- Example recipes in `docs/cookbook/`

---

### Phase 3.3: Release (Day 14)
- Publish to PyPI
- Create demo video
- Write launch blog post
- Submit to awesome-mcp-servers

---

## 🎨 Architecture Improvements

### Current vs Enhanced Architecture

**Before (traditional):**
```
OpenAPI URL → Parser → Generator → MCP Server
```

**After (with AI):**
```
                    ┌─────────────┐
                    │  Input      │
                    │  • URL      │
                    │  • Spec     │
                    │  • Preset   │
                    └──────┬──────┘
                           ↓
         ┌─────────────────┴─────────────────┐
         ↓                                   ↓
    ┌────────────┐                  ┌────────────────┐
    │  Static    │                  │  AI Explorer   │
    │  Parser    │                  │  Agent         │
    │  (OpenAPI) │                  │  (learns API)  │
    └─────┬──────┘                  └────────┬───────┘
          │                                  │
          │         ┌──────────────┐         │
          └────────→│   Merger     │←────────┘
                    │   (AI-enhanced)
                    └───────┬──────┘
                            ↓
                   ┌────────────────┐
                   │ Smart Generator│
                   │ (context-aware)│
                   └────────┬───────┘
                            ↓
                    ┌───────────────┐
                    │  MCP Server   │
                    │  (production) │
                    └───────────────┘
```

---

## 🚀 Key Differentiators

### What makes this unique:

1. **AI-Powered Learning**
   - First MCP adapter that learns API behavior
   - Works without OpenAPI specs
   - Discovers undocumented features

2. **Context-Aware Generation**
   - Tool descriptions optimized for LLMs
   - Semantic endpoint grouping
   - Auto-generated examples

3. **Hybrid Approach**
   - Combines static specs + dynamic learning
   - Best of both worlds

4. **Developer Experience**
   - One command: `mcp-adapt URL --learn`
   - Works with any API
   - Generated code is readable

---

## 📊 Success Metrics

**Technical:**
- [ ] Supports 5+ API formats (OpenAPI, GraphQL, REST, HAR, Postman)
- [ ] Generates Python + TypeScript servers
- [ ] >80% test coverage
- [ ] <5min generation time for typical API

**Community:**
- [ ] 1000+ GitHub stars (30 days)
- [ ] 50+ generated servers shared
- [ ] 10+ API presets
- [ ] Listed in awesome-mcp-servers

**Innovation:**
- [ ] AI learning mode working with 10+ real APIs
- [ ] 90%+ accuracy in endpoint discovery
- [ ] Generated tools rated 4+ stars by users

---

## 🔧 Implementation Priority

### Immediate (Sprint 1):
1. ✅ Basic OpenAPI parser
2. ✅ Python generator with templates
3. ✅ JSONPlaceholder demo
4. ✅ CLI framework

### Near-term (Sprint 2):
1. 🚀 AI Explorer Agent (INNOVATION)
2. 🚀 Smart Generator with LLM
3. Stripe preset
4. Error handling

### Future:
1. TypeScript generator
2. GraphQL support
3. HAR import
4. Web UI (Streamlit)
5. VS Code extension
6. Community preset marketplace

---

## 📝 Notes & Decisions

### Technology Choices:
- **Parser:** `openapi-parser` (lightweight, fast)
- **LLM:** Anthropic Claude (for exploration/analysis)
- **Templates:** Jinja2 (standard, flexible)
- **CLI:** Typer (modern, type-safe)
- **HTTP:** httpx (async, modern)

### Design Decisions:
1. **Unified API model:** All parsers convert to common format
2. **Template-based generation:** Easy to customize/extend
3. **Optional AI learning:** Works with or without API key
4. **Fail gracefully:** Falls back to basic mode if AI fails

---

## 🤝 Contributing

Priority areas for contributors:
1. API presets (Stripe, GitHub, OpenAI, etc.)
2. TypeScript generator
3. AI prompt engineering (exploration/analysis)
4. Test coverage
5. Documentation & examples

---

**Next Step:** Start with Phase 1.1 - Core Parser implementation
