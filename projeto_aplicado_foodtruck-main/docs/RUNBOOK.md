# 🚀 Food Truck Deployment Runbook

[![Docker](https://img.shields.io/badge/docker-compose-blue.svg)](https://docs.docker.com/compose/)
[![PostgreSQL](https://img.shields.io/badge/database-postgresql%2016-336791.svg)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/cache-redis%207.4-dc382d.svg)](https://redis.io/)

> **Deployment, health checks, troubleshooting, and rollback procedures for Food Truck production**

## 📋 Table of Contents

- [📦 Deployment Architecture](#-deployment-architecture)
- [🚀 Deployment Steps](#-deployment-steps)
- [✅ Health Checks](#-health-checks)
- [🔧 Common Issues](#-common-issues)
- [↩️ Rollback Procedures](#️-rollback-procedures)
- [📊 Monitoring](#-monitoring)

---

## 📦 Deployment Architecture

### Service Stack

The Food Truck system runs as a **5-service Docker Compose stack**:

```
┌─────────────────────────────────────────────────────────────┐
│                    Traefik (Reverse Proxy)                  │
│                  Ports: 80, 8080 (admin)                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐  ┌──────────────────┐                 │
│  │    Backend API   │  │   Frontend Nginx │                 │
│  │   Port: 8000     │  │   Port: 3000     │                 │
│  └──────────────────┘  └──────────────────┘                 │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐  ┌──────────────────┐                 │
│  │   PostgreSQL 16  │  │    Redis 7.4.2   │                 │
│  │   Port: 5432     │  │   Port: 6379     │                 │
│  └──────────────────┘  └──────────────────┘                 │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Service Details

| Service | Image | Port | Purpose | Status |
|---------|-------|------|---------|--------|
| **traefik** | traefik:v3.4.1 | 80, 8080 | Reverse proxy & load balancer | Essential |
| **backend** | Custom (FastAPI) | 8000 | REST API server | Essential |
| **frontend** | nginx:alpine | 3000 | Static HTML/CSS/JS frontend | Essential |
| **postgres** | postgres:16 | 5432 | Primary database | Essential |
| **redis** | redis:7.4.2 | 6379 | Cache & sessions | Important |

### Data Volumes

- **postgres_data** — PostgreSQL database files (persistent)
- **redis_data** — Redis cache data (non-persistent)
- **migrations/** — Alembic database migrations (mounted from host)

---

## 🚀 Deployment Steps

### Prerequisites

Before deploying, ensure:

1. **Docker & Docker Compose installed**
   ```bash
   docker --version       # Docker version 20.10+
   docker-compose --version
   ```

2. **`.env` file configured**
   ```bash
   # Copy template and configure
   cp .env.template .env
   
   # Edit .env with your settings
   vim .env
   ```

3. **Sufficient disk space**
   - PostgreSQL database
   - Redis cache
   - Docker images (~2GB)

### Deployment Procedure

#### Step 1: Start Services

```bash
# From project root directory
cd /path/to/projeto_aplicado_foodtruck

# Build and start all services in background
docker-compose up -d --build

# Watch startup progress
docker-compose logs -f
```

Expected startup sequence:
1. **traefik** starts first (usually ~5s)
2. **backend** starts (waits for redis health check)
3. **frontend** starts
4. **postgres** starts (initializes database ~10s)
5. **redis** starts (initializes ~2s)

#### Step 2: Verify Database

```bash
# Initialize database schema (Alembic migrations)
docker-compose exec backend uv run python -m alembic upgrade head

# Create default admin user (if needed)
docker-compose exec backend uv run python -c \
  "from projeto_aplicado.app import init_default_admin; init_default_admin()"
```

#### Step 3: Health Checks

```bash
# Run all health checks (see ✅ Health Checks section below)
docker-compose ps
./scripts/health-check.sh  # If available
```

#### Step 4: Verify Access

```bash
# API Documentation
curl http://localhost:8000/docs

# Frontend
curl http://localhost:3000

# Traefik Dashboard
curl http://localhost:8080/dashboard
```

### Stopping Services

```bash
# Graceful shutdown (data preserved)
docker-compose down

# Full cleanup (includes volumes - ⚠️ DELETES DATA)
docker-compose down -v
```

---

## ✅ Health Checks

### Database Health

**PostgreSQL** (port 5432):

```bash
# Method 1: Docker health check
docker-compose ps postgres

# Method 2: Direct pg_isready
docker-compose exec postgres pg_isready -U postgres

# Method 3: Test connection
docker-compose exec postgres psql -U postgres -d foodtruck -c "SELECT 1"
```

**Expected output**:
```
accepting connections
```

### Cache Health

**Redis** (port 6379):

```bash
# Method 1: Docker health check
docker-compose ps redis

# Method 2: Direct redis-cli ping
docker-compose exec redis redis-cli ping

# Method 3: Check info
docker-compose exec redis redis-cli INFO server
```

**Expected output**:
```
PONG
```

### API Health

**Backend** (port 8000):

```bash
# Note: No dedicated health endpoint currently defined
# (Gap identified — consider adding GET /health)

# Method 1: Check API documentation endpoint
curl -s http://localhost:8000/docs | head -20

# Method 2: Check service is running
docker-compose ps backend

# Method 3: Test authentication (requires admin credentials)
curl -X POST http://localhost:8000/api/v1/token/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@foodtruck.com&password=admin123"
```

**Expected output**:
- HTTP 200 with access_token (if credentials correct)
- HTTP 422 if credentials missing

### Frontend Health

**Nginx Frontend** (port 3000):

```bash
# Check service is running
docker-compose ps frontend

# Verify HTML is served
curl -I http://localhost:3000

# Check specific page
curl http://localhost:3000/index.html | head -10
```

**Expected output**:
```
HTTP/1.1 200 OK
Content-Type: text/html
```

### Reverse Proxy Health

**Traefik** (ports 80, 8080):

```bash
# Check dashboard (admin interface)
curl http://localhost:8080/dashboard

# Check main routing (should redirect to backend)
curl -v http://localhost/api/v1/docs 2>&1 | grep -i location
```

### Full Health Check Script

Create `scripts/health-check.sh`:

```bash
#!/bin/bash

echo "🏥 Food Truck Health Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# PostgreSQL
echo "📊 PostgreSQL..."
if docker-compose exec -T postgres pg_isready -U postgres > /dev/null 2>&1; then
  echo "  ✅ Ready (port 5432)"
else
  echo "  ❌ Not responding"
fi

# Redis
echo "💾 Redis..."
if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
  echo "  ✅ Ready (port 6379)"
else
  echo "  ❌ Not responding"
fi

# Backend API
echo "🚀 Backend API..."
if curl -s http://localhost:8000/docs > /dev/null; then
  echo "  ✅ Ready (port 8000)"
else
  echo "  ❌ Not responding"
fi

# Frontend
echo "🌐 Frontend..."
if curl -s http://localhost:3000 > /dev/null; then
  echo "  ✅ Ready (port 3000)"
else
  echo "  ❌ Not responding"
fi

# Traefik
echo "🔀 Traefik..."
if curl -s http://localhost:8080/dashboard > /dev/null; then
  echo "  ✅ Ready (ports 80, 8080)"
else
  echo "  ❌ Not responding"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "All checks complete"
```

Run it:
```bash
chmod +x scripts/health-check.sh
./scripts/health-check.sh
```

---

## 🔧 Common Issues

### Issue: Port Already in Use

**Symptom**: `docker-compose up` fails with "port 8000 already in use"

**Solution**:

```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
docker-compose down
# Edit docker-compose.yaml to use different port
docker-compose up -d
```

### Issue: Database Not Initializing

**Symptom**: Backend logs show "connection refused" to postgres

**Solution**:

```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check PostgreSQL logs
docker-compose logs postgres

# Reset PostgreSQL
docker-compose down
docker volume rm proyecto-aplicado_postgres_data  # ⚠️ DELETES DATA
docker-compose up -d postgres
sleep 15
docker-compose exec postgres psql -U postgres -d foodtruck -c "SELECT 1"
```

### Issue: Redis Connection Timeout

**Symptom**: Backend logs show "redis connection timeout"

**Solution**:

```bash
# Check Redis is running and healthy
docker-compose ps redis
docker-compose exec redis redis-cli PING

# Restart Redis
docker-compose restart redis

# Check backend logs
docker-compose logs backend
```

### Issue: Frontend 404 on Static Files

**Symptom**: Browser shows 404 for CSS/JS files (blank/broken page)

**Solution**:

```bash
# Verify frontend volume mount
docker-compose exec frontend ls -la /usr/share/nginx/html/

# Check Nginx config
docker-compose exec frontend cat /etc/nginx/nginx.conf

# Restart frontend
docker-compose restart frontend
```

### Issue: Database Migrations Fail

**Symptom**: Backend won't start, logs show "migration failed"

**Solution**:

```bash
# Check migration history
docker-compose exec backend uv run alembic history

# Rollback to previous migration
docker-compose exec backend uv run alembic downgrade -1

# Manually apply migrations
docker-compose exec backend uv run alembic upgrade head

# Check SQL logs
docker-compose logs postgres | grep ERROR
```

### Issue: Authentication Token Not Working

**Symptom**: API calls return 401 "Invalid credentials" even with correct password

**Solution**:

```bash
# Verify admin user exists
docker-compose exec backend uv run python -c \
  "from projeto_aplicado.resources.user.repository import UserRepository; \
   from projeto_aplicado.ext.database.db import get_session; \
   session = next(get_session()); \
   repo = UserRepository(session); \
   user = repo.find_by_email('admin@foodtruck.com'); \
   print(f'Admin user found: {user}')"

# Reset admin password
docker-compose exec backend uv run python -c \
  "from projeto_aplicado.app import reset_admin_password; \
   reset_admin_password('newpassword123')"

# Check JWT settings in .env
grep "JWT_" .env
```

---

## ↩️ Rollback Procedures

### Quick Rollback (Last Deployment)

If deployment failed or introduced critical issues:

```bash
# 1. Stop current services (keep data)
docker-compose down

# 2. Checkout previous version
git checkout HEAD~1

# 3. Rebuild and restart
docker-compose up -d --build

# 4. Verify health
./scripts/health-check.sh
```

### Database Rollback

If database migration caused issues:

```bash
# 1. Check current migration
docker-compose exec backend uv run alembic current

# 2. Rollback one migration
docker-compose exec backend uv run alembic downgrade -1

# 3. Verify database
docker-compose exec postgres psql -U postgres -d foodtruck -c "SELECT COUNT(*) FROM users"
```

### Full Rollback (Complete Data Reset)

**⚠️ WARNING: This deletes all data — use only for testing**

```bash
# 1. Stop all services
docker-compose down -v

# 2. Remove all volumes
docker volume rm projeto-aplicado_postgres_data
docker volume rm projeto-aplicado_redis_data

# 3. Restart with clean state
docker-compose up -d --build

# 4. Re-initialize
docker-compose exec backend uv run alembic upgrade head
```

---

## 📊 Monitoring

### View Service Logs

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs postgres
docker-compose logs redis

# Follow logs (real-time)
docker-compose logs -f

# Last N lines
docker-compose logs --tail=50
```

### Service Status

```bash
# Check all services
docker-compose ps

# Detailed status
docker-compose ps --format "table {{.Service}}\t{{.Status}}\t{{.Ports}}"

# Resource usage
docker stats
```

### Access Databases Directly

```bash
# PostgreSQL
docker-compose exec postgres psql -U postgres -d foodtruck

# Redis
docker-compose exec redis redis-cli

# Run queries
docker-compose exec postgres psql -U postgres -d foodtruck -c "SELECT * FROM user LIMIT 5"
```

### Configuration Review

```bash
# Check environment variables
docker-compose config

# View backend settings
docker-compose exec backend python -c "from projeto_aplicado.settings import get_settings; s = get_settings(); print(f'Debug: {s.API_DEBUG}, Version: {s.API_VERSION}')"
```

---

## ⚠️ Known Limitations

1. **No Backend Health Check Endpoint** — Add `GET /health` endpoint to provide application-level health monitoring
2. **No Automated Alerting** — Configure Docker events or Prometheus for production monitoring
3. **Manual Backup** — Database backups require manual `pg_dump` commands; consider automated backup solutions
4. **No Secrets Management** — `.env` file is version-controlled; use a secret manager (Vault, AWS Secrets) for production

---

## 🔗 Related Documentation

- **[Installation Guide](INSTALL.md)** — Initial setup and prerequisites
- **[Architecture Guide](ARCHITECTURE.md)** — System design and components
- **[API Documentation](API.md)** — REST API endpoints
- **[Development Guide](CONTRIBUTING.md)** — Development workflow

---

**🏠 [Documentation Index](README.md)** • **🐛 [Report Issues](https://github.com/bentoluizv/projeto_aplicado_foodtruck/issues)** • **💡 [Request Features](https://github.com/bentoluizv/projeto_aplicado_foodtruck/issues)**
