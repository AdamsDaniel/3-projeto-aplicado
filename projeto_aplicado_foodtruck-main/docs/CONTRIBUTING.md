# 🛠️ Food Truck Development Guide

[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://python.org)
[![uv](https://img.shields.io/badge/package%20manager-uv-orange.svg)](https://github.com/astral-sh/uv)
[![Code Quality](https://img.shields.io/badge/code%20quality-ruff-black.svg)](https://docs.astral.sh/ruff/)
[![Testing](https://img.shields.io/badge/testing-pytest-green.svg)](https://pytest.org/)

> **Contributing to Food Truck — setup, development workflow, testing requirements, and PR guidelines**

## 📋 Table of Contents

- [🚀 Developer Setup](#-developer-setup)
- [🛠️ Development Tasks](#️-development-tasks)
- [🧪 Testing](#-testing)
- [📝 Code Quality](#-code-quality)
- [🔄 Pull Request Checklist](#-pull-request-checklist)

---

## 🚀 Developer Setup

### 1. Prerequisites

Ensure you have the required tools installed:

- **Python 3.13+** — Required runtime version
- **uv** — Python package manager
- **Docker** — For PostgreSQL, Redis, and test containers
- **Git** — Version control

### 2. Clone & Setup Project

```bash
# Clone the repository
git clone https://github.com/bentoluizv/projeto_aplicado_foodtruck.git
cd projeto_aplicado_foodtruck

# Create Python virtual environment with Python 3.13
uv venv --python 3.13
source .venv/bin/activate

# Install all dependencies (dev + test groups)
uv sync --group dev --group test
```

### 3. Environment Configuration

Copy the `.env.template` to `.env` and set your values:

```bash
cp .env.template .env
```

Then edit `.env` with your configuration:

```bash
# Database (required)
POSTGRES_PASSWORD=dev-password
POSTGRES_USER=postgres

# JWT Settings (required)
JWT_SECRET_KEY=dev-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Optional: Application settings
DEFAULT_ADMIN_EMAIL=admin@foodtruck.com
DEFAULT_ADMIN_NAME=Admin
DEFAULT_ADMIN_PASSWORD=admin123
```

### 4. Start Services

For development, start PostgreSQL and Redis in Docker:

```bash
# Start all services (backend, frontend, postgres, redis, traefik)
cd /path/to/repo/projeto_aplicado_foodtruck-main
docker-compose up -d postgres redis

# Verify services are healthy
docker-compose ps
```

### 5. Verify Setup

```bash
# Run quick health check
uv run pytest -k "test_health" --tb=short

# Run full test suite (requires docker running)
uv run task test
```

---

## 🛠️ Development Tasks

Use **taskipy** to run common development tasks:

| Task | Command | Purpose |
|------|---------|---------|
| **Dev Server** | `uv run task dev` | Start FastAPI development server (auto-reload) |
| **Run** | `uv run task run` | Start FastAPI production server |
| **Lint** | `uv run task lint` | Check code with ruff |
| **Format** | `uv run task format` | Format and fix code with ruff |
| **Test** | `uv run task test` | Run pytest with coverage |
| **Export** | `uv run task export` | Generate requirements.txt from lock file |

### Examples

```bash
# Development workflow
uv run task dev          # Start server with auto-reload (http://localhost:8000)
uv run task lint         # Check for code issues
uv run task format       # Auto-format code
uv run task test         # Run tests with coverage
```

### Script Details

**Dev Server** (auto-reload on code changes):
```bash
uv run task dev
# Access: http://localhost:8000
# API docs: http://localhost:8000/docs
```

**Test Suite** (requires Docker for testcontainers):
```bash
uv run task test
# Runs pytest with:
# - Coverage reporting
# - PostgreSQL test container via testcontainers
# - Async test support
```

**Code Quality**:
```bash
# Lint (check only)
uv run task lint

# Format (auto-fix)
uv run task format

# Line length: 79 characters (enforced)
```

---

## 🧪 Testing

### Test Requirements

- **Minimum Coverage**: 80%
- **Framework**: pytest + pytest-asyncio
- **Test Isolation**: Each test uses a separate test database
- **Infrastructure**: testcontainers with PostgreSQL

### Running Tests

```bash
# Run all tests
uv run task test

# Run specific test file
uv run pytest tests/test_api_products.py

# Run with verbose output
uv run pytest -v

# Run specific test function
uv run pytest tests/test_api_products.py::test_create_product

# Run with coverage report
uv run pytest --cov=projeto_aplicado --cov-report=term-missing

# Run tests in parallel
uv run pytest -n auto
```

### Test Organization

Tests are organized by resource:

```
tests/
├── conftest.py           # Shared fixtures (database, client, auth)
├── test_api_users.py     # User endpoint tests
├── test_api_products.py  # Product endpoint tests
├── test_api_order.py     # Order endpoint tests
└── test_auth/            # Authentication tests
    └── test_security.py  # JWT and password tests
```

### Test Structure (AAA Pattern)

Use Arrange-Act-Assert structure for clarity:

```python
def test_create_product_with_valid_data(client, db_session, admin_token):
    # Arrange
    product_data = {
        "name": "X-Burger",
        "description": "Handcrafted burger",
        "price": 25.90,
        "category": "burger",
        "image_url": "https://example.com/burger.jpg",
        "is_available": True
    }
    
    # Act
    response = client.post(
        "/api/v1/products",
        json=product_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    # Assert
    assert response.status_code == 201
    assert response.json()["action"] == "created"
```

### Testing Database Access

Tests use **testcontainers** with PostgreSQL:

```python
# conftest.py sets up a fresh PostgreSQL container for each test
# No manual database setup needed — testcontainers handles it

# Database is automatically:
# - Created fresh for each test session
# - Migrated with latest schema
# - Cleaned up after tests
# - Isolated from other test runs
```

### Test Running Requirements

**Docker must be running** for tests to work:

```bash
# Verify Docker is accessible
docker ps

# If Docker is not running, tests will fail
uv run pytest
# Error: Cannot connect to Docker daemon
```

---

## 📝 Code Quality

### Linting & Formatting

Code quality is enforced with **ruff** (line length: 79 characters):

```bash
# Check for issues (no changes)
uv run task lint

# Fix and format code automatically
uv run task format
```

### Code Style Guidelines

- **Line Length**: 79 characters (hard limit)
- **Imports**: Organized and deduplicated
- **Naming**: `camelCase` for variables, `PascalCase` for classes
- **Type Hints**: Required on all functions
- **Docstrings**: Required on public functions

Example:

```python
def get_products(
    offset: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
) -> ProductList:
    """
    Fetch paginated list of products.
    
    Args:
        offset: Records to skip
        limit: Records to return
        session: Database session
        
    Returns:
        ProductList with pagination metadata
    """
    repository = ProductRepository(session)
    return repository.get_all(offset=offset, limit=limit)
```

### Before Committing

```bash
# 1. Format code
uv run task format

# 2. Run full test suite
uv run task test

# 3. Verify linting passes
uv run task lint

# 4. Check coverage is >= 80%
# (output from task test shows coverage)
```

---

## 🔄 Pull Request Checklist

Before submitting a pull request, verify:

### Code Quality
- [ ] All tests pass: `uv run task test`
- [ ] Code is formatted: `uv run task format`
- [ ] No linting issues: `uv run task lint`
- [ ] Test coverage >= 80%
- [ ] No hardcoded secrets or sensitive data
- [ ] No debug console.log or print statements

### Documentation
- [ ] Code changes are documented
- [ ] Public functions have docstrings
- [ ] Complex logic has explanatory comments
- [ ] README updated if applicable (for major features)

### Testing
- [ ] New features have corresponding tests
- [ ] Edge cases are covered
- [ ] Tests use AAA pattern (Arrange-Act-Assert)
- [ ] Tests are isolated and don't depend on each other

### Commit Standards
- [ ] Commits follow conventional format: `type: description`
- [ ] Commit messages are clear and descriptive
- [ ] Related commits are logically grouped

### PR Description
- [ ] PR title is clear and concise
- [ ] Detailed description of changes
- [ ] Link to related issues
- [ ] Test results/instructions for testing
- [ ] Screenshots/examples for UI changes

---

## 📚 Resources

- **[Installation Guide](INSTALL.md)** — Complete project setup
- **[Dependencies Guide](DEPENDENCIES.md)** — Manage dependencies with uv
- **[API Documentation](API.md)** — REST API reference
- **[Architecture Guide](ARCHITECTURE.md)** — System design overview
- **[Tests Guide](TESTS.md)** — Testing best practices

---

**📖 [Documentation Index](README.md)** • **🐛 [Report Issues](https://github.com/bentoluizv/projeto_aplicado_foodtruck/issues)** • **💡 [Request Features](https://github.com/bentoluizv/projeto_aplicado_foodtruck/issues)**
