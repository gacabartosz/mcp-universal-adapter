# Contributing to MCP Universal Adapter

Thank you for your interest in contributing! This project is in early development and we welcome all contributions.

## Project Status

⚠️ **This project is in active development.** Core functionality is being implemented. Please check the [README](README.md) for current status.

## How to Contribute

### Reporting Bugs

Use the [Bug Report](.github/ISSUE_TEMPLATE/bug_report.md) template to report issues.

### Suggesting Features

Use the [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md) template to suggest new features.

### Requesting API Presets

Use the [Preset Request](.github/ISSUE_TEMPLATE/preset_request.md) template to request support for a specific API.

### Code Contributions

1. **Fork the repository**

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/mcp-universal-adapter.git
   cd mcp-universal-adapter
   ```

3. **Set up development environment**
   ```bash
   # Install Poetry if you haven't already
   curl -sSL https://install.python-poetry.org | python3 -

   # Install dependencies
   poetry install

   # Install pre-commit hooks
   poetry run pre-commit install
   ```

4. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

5. **Make your changes**
   - Write clear, documented code
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation as needed

6. **Run tests and checks**
   ```bash
   # Run tests
   poetry run pytest

   # Run type checking
   poetry run mypy src/

   # Run linting
   poetry run ruff check src/
   poetry run black --check src/
   ```

7. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

   We follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` - New features
   - `fix:` - Bug fixes
   - `docs:` - Documentation changes
   - `test:` - Test additions or modifications
   - `refactor:` - Code refactoring
   - `chore:` - Maintenance tasks

8. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

9. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill in the PR template
   - Link related issues

## Development Guidelines

### Code Style

- Use Python 3.10+ features
- Follow PEP 8 style guide
- Use type hints for all functions
- Write docstrings for public APIs
- Keep functions focused and testable

### Testing

- Write unit tests for new functionality
- Maintain or improve code coverage
- Test edge cases and error conditions
- Use fixtures for common test data

### Documentation

- Update README.md if adding user-facing features
- Add docstrings to all public functions/classes
- Update examples if changing APIs
- Keep documentation concise and clear

## Architecture

The project follows a modular architecture:

```
src/mcp_adapter/
├── parsers/      # API specification parsers (OpenAPI, GraphQL, etc.)
├── generators/   # Code generators for target languages
├── templates/    # Jinja2 templates for code generation
├── presets/      # Pre-configured API definitions
├── validators/   # Validation utilities
└── cli.py        # Command-line interface
```

## Priority Areas

Current development priorities:

1. **OpenAPI Parser** - Parse OpenAPI 3.x specifications
2. **Python Generator** - Generate Python MCP servers
3. **Stripe Preset** - First working preset
4. **Documentation** - Usage guides and examples

Check the [Issues](https://github.com/bgacainvest/mcp-universal-adapter/issues) page for tasks marked as "good first issue".

## Questions?

- Open a [Discussion](https://github.com/bgacainvest/mcp-universal-adapter/discussions)
- Reach out via email: gaca.bartosz@gmail.com

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
