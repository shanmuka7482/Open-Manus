# Docker Setup Guide for OpenManus

This guide provides instructions for running OpenManus using Docker and Docker Compose.

## 📋 Files Created

The following Docker-related files have been created:

1. **`backend/Dockerfile`** - Backend Python/FastAPI container
2. **`frontend/Dockerfile`** - Frontend React/Nginx container
3. **`frontend/server/Dockerfile`** - WebSocket proxy server container
4. **`frontend/nginx.conf`** - Nginx configuration for frontend
5. **`docker-compose.yml`** - Orchestration file (root directory)
6. **`backend/.dockerignore`** - Backend exclusions

## 🚀 Quick Start

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+

### Running the Application

1. **Clone and navigate to the project root:**
   ```bash
   cd e:\Shared_folder\working_model\Open-Manus
   ```

2. **Create environment files:**

   Create `backend/.env`:
   ```env
   # Leave empty or add custom environment variables
   ```

   Create `.env` in root (for docker-compose):
   ```env
   VITE_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key_here
   ```

3. **Ensure configuration file exists:**
   ```bash
   cp backend/config/config.example.toml backend/config/config.toml
   # Edit backend/config/config.toml with your API keys
   ```

4. **Build and start all services:**
   ```bash
   docker-compose up --build
   ```

5. **Access the application:**
   - **Frontend**: http://localhost
   - **Backend API**: http://localhost:8000
   - **WebSocket Server**: http://localhost:5000

### Stopping the Application

```bash
docker-compose down
```

To remove volumes as well:
```bash
docker-compose down -v
```

## 📦 Architecture

```
┌─────────────────┐
│   Frontend      │ Port 80
│   (Nginx)       │
└────────┬────────┘
         │
    ┌────┴──────────────┐
    │                   │
┌───▼────────┐  ┌───────▼──────┐
│  Backend   │  │  WS Server   │
│  (FastAPI) │  │  (Node.js)   │
│  Port 8000 │  │  Port 5000   │
└────────────┘  └──────────────┘
```

## 🔧 Individual Service Commands

### Build specific service:
```bash
docker-compose build backend
docker-compose build frontend
docker-compose build server
```

### Run specific service:
```bash
docker-compose up backend
docker-compose up frontend
docker-compose up server
```

### View logs:
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f server
```

### Execute commands in running container:
```bash
docker-compose exec backend python main.py
docker-compose exec backend bash
```

## 📝 Manual .dockerignore Files

Due to gitignore restrictions, you may need to manually create these files:

### `frontend/.dockerignore`
```
node_modules/
dist/
build/
.env.local
.env.development.local
.env.test.local
.env.production.local
npm-debug.log*
yarn-debug.log*
yarn-error.log*
*.log
.vscode/
.idea/
*.swp
*.swo
coverage/
.git/
.gitignore
*.md
README*
docker-compose.yml
.DS_Store
Thumbs.db
.eslintcache
```

### `frontend/server/.dockerignore`
```
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
*.log
.vscode/
.idea/
*.swp
*.swo
.git/
.gitignore
*.md
README*
docker-compose.yml
.DS_Store
Thumbs.db
```

## 🔍 Health Checks

All services include health checks:

- **Backend**: Checks `/files` endpoint every 30s
- **Server**: Checks `/health` endpoint every 30s
- **Frontend**: Checks root `/` endpoint every 30s

View health status:
```bash
docker-compose ps
```

## 🌍 Environment Variables

### Backend (`backend/.env`)
```env
LOG_LEVEL=INFO
PYTHONUNBUFFERED=1
```

### Frontend (root `.env`)
```env
VITE_CLERK_PUBLISHABLE_KEY=pk_test_...
```

### Server
No additional environment variables required. Backend URL is automatically set via docker-compose.

## 📊 Volumes

The docker-compose setup creates persistent volumes for:

- **Backend workspace**: `./backend/workspace` → `/app/workspace`
- **Backend logs**: `./backend/logs` → `/app/logs`
- **Backend config**: `./backend/config` → `/app/config` (read-only)

## 🔧 Troubleshooting

### Port Already in Use

If ports are already in use, modify `docker-compose.yml`:

```yaml
services:
  backend:
    ports:
      - "8001:8000"  # Use port 8001 instead

  frontend:
    ports:
      - "8080:80"    # Use port 8080 instead
```

### Backend Can't Connect to LLM API

Ensure your `backend/config/config.toml` has valid API keys:

```bash
docker-compose exec backend cat /app/config/config.toml
```

### Container Won't Start

View detailed logs:
```bash
docker-compose logs backend
docker-compose logs frontend
docker-compose logs server
```

### Rebuild from Scratch

```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

## 🚀 Production Deployment

For production deployment:

1. **Set production environment variables**
2. **Use secrets management** for API keys
3. **Enable HTTPS** with SSL certificates
4. **Configure proper CORS** settings
5. **Set up monitoring** and logging
6. **Use docker-compose.prod.yml** for production overrides

Example `docker-compose.prod.yml`:
```yaml
version: '3.8'

services:
  backend:
    restart: always
    environment:
      - LOG_LEVEL=WARNING

  frontend:
    restart: always
    ports:
      - "443:80"
```

Run with:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Nginx Configuration Reference](https://nginx.org/en/docs/)

## 🐛 Common Issues

### Issue: Playwright browsers not installed in backend

**Solution**: The Dockerfile already includes `playwright install chromium`. If issues persist, rebuild:
```bash
docker-compose build --no-cache backend
```

### Issue: Frontend can't reach backend/server

**Solution**: Ensure all services are in the same network. Check with:
```bash
docker network ls
docker network inspect openmanus_openmanus-network
```

### Issue: WebSocket connection fails

**Solution**: Verify the nginx.conf WebSocket proxy configuration and ensure the server service is healthy:
```bash
docker-compose ps server
docker-compose logs server
```

## 📝 Notes

- The frontend is built using a multi-stage Docker build for optimal image size
- Backend includes Playwright with Chromium for browser automation
- All services use health checks to ensure proper startup order
- Network isolation is maintained with a dedicated bridge network
- Volumes ensure data persistence across container restarts
