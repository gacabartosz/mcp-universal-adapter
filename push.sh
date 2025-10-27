#!/bin/bash

# Quick push script for mcp-universal-adapter
# This script will create GitHub repo and push all code

set -e

echo "🚀 MCP Universal Adapter - GitHub Push Script"
echo "=============================================="
echo ""

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Must run from mcp-universal-adapter root directory"
    exit 1
fi

# Check if gh is installed
if ! command -v gh &> /dev/null; then
    echo "❌ Error: GitHub CLI (gh) not installed"
    echo "Install: brew install gh"
    exit 1
fi

# Check git status
echo "📋 Current git status:"
git status --short
echo ""

# Check if remote already exists
if git remote | grep -q "origin"; then
    echo "✅ Remote 'origin' already exists"
    echo ""
    echo "🔍 Remote URL:"
    git remote get-url origin
    echo ""

    read -p "Push to existing remote? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "📤 Pushing to origin/main..."
        git push -u origin main
        echo ""
        echo "✅ Successfully pushed to GitHub!"
        echo ""
        echo "🌐 View your repo:"
        gh repo view --web
    fi
else
    echo "📝 Creating new GitHub repository..."
    echo ""
    echo "Repository details:"
    echo "  Name: mcp-universal-adapter"
    echo "  Visibility: Public"
    echo "  Description: Transform any API into MCP server automatically"
    echo ""

    read -p "Create and push? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        echo "🔐 Checking GitHub authentication..."

        if ! gh auth status &> /dev/null; then
            echo "⚠️  Not logged in to GitHub"
            echo "Starting login process..."
            gh auth login
        fi

        echo ""
        echo "✨ Creating repository and pushing..."

        gh repo create mcp-universal-adapter \
            --public \
            --source=. \
            --remote=origin \
            --description="Transform any API into a fully functional MCP server automatically. OpenAPI → Python/TS MCP with AI-powered learning." \
            --push

        echo ""
        echo "✅ Successfully created and pushed to GitHub!"
        echo ""
        echo "🌐 Your repository:"
        gh repo view --web

        echo ""
        echo "📝 Next steps:"
        echo "  1. Fix dependencies in pyproject.toml"
        echo "  2. Create first demo with Pet Store API"
        echo "  3. Add GitHub Actions CI/CD"
        echo "  4. Submit to awesome-mcp-servers"
    fi
fi

echo ""
echo "Done! 🎉"
