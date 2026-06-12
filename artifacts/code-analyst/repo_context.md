# Repository: Abhay-Kumar-NTT/agenticSDLC-backend

The following is the complete source code and configuration of the repository.
Files are listed in directory order. Binary files, build artefacts, and
dependency directories (.cache, .git, .idea, .next, .nuxt, .nyc_output, .pytest_cache, .venv, .vscode, __pycache__, bin, build, coverage, dist, logs, node_modules, obj, target, tmp, vendor, venv) are excluded.

## Directory Structure

```
Abhay-Kumar-NTT/agenticSDLC-backend/
  .env.example
  .gitignore
  API.md
  GITHUB_SETUP.md
  QUICKSTART.md
  README.md
  REPOSITORY_SETUP.md
  SETUP.md
  package.json
  server.js
  setup-database.cjs
  test-db-simple.cjs
  config/
    database.config.js
  db/
    connection.js
    run-migration.cjs
    schema.sql
    migrations/
      002_create_repositories_table.sql
      002_workflow_node_executions.sql
  models/
    Repository.js
    execution.model.js
    workflow.model.js
  routes/
    execution.routes.js
    repository.routes.js
    workflow.routes.js
```

## File Contents

### `.env.example`

```example
# Environment Configuration
NODE_ENV=development

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=agenticsdlc_dev
DB_USER=postgres
DB_PASSWORD=postgres

# For SSL connections (production/staging)
# DB_SSL_CA=/path/to/ca-certificate.crt

# API Configuration
PORT=3001
CORS_ORIGIN=http://localhost:5173

# Logging
LOG_LEVEL=info

```


### `.gitignore`

```
# Dependencies
node_modules/
package-lock.json

# Environment variables
.env

# Logs
logs/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Operating System
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Test coverage
coverage/

# Build outputs
dist/
build/

# Temporary files
*.tmp
*.temp

```


### `API.md`

```md
# API Documentation

Complete API reference for AgenticSDLC Backend.

## Base URL

```
http://localhost:3001
```

## Authentication

Currently, no authentication is required. Authentication will be added in future versions.

## Response Format

All API responses follow this format:

### Success Response
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation completed"
}
```

### Error Response
```json
{
  "success": false,
  "message": "Error description",
  "error": "Detailed error message"
}
```

## Endpoints

### Health Check

#### GET /health

Check if the server is running.

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2024-05-31T00:00:00.000Z"
}
```

**Example:**
```bash
curl http://localhost:3001/health
```

---

### Workflows

#### GET /api/workflows

Get all workflows (summary view).

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "name": "My Workflow",
      "status": "active",
      "node_count": "3",
      "edge_count": "2",
      "created_at": "2024-05-31T00:00:00.000Z"
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:3001/api/workflows
```

---

#### GET /api/workflows/:id

Get a specific workflow with all nodes and edges.

**Parameters:**
- `id` (path) - Workflow UUID

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "My Workflow",
    "status": "active",
    "created_at": "2024-05-31T00:00:00.000Z",
    "nodes": [
      {
        "id": "node-1",
        "type": "product-vision",
        "label": "Product Vision",
        "category": "Planning",
        "x": 100,
        "y": 100,
        "color": "#3b82f6"
      }
    ],
    "edges": [
      {
        "id": "edge-1",
        "fromId": "node-1",
        "toId": "node-2",
        "relationship": "successor"
      }
    ]
  }
}
```

**Example:**
```bash
curl http://localhost:3001/api/workflows/abc-123-def
```

---

#### POST /api/workflows

Create a new workflow.

**Request Body:**
```json
{
  "name": "My New Workflow",
  "status": "active",
  "nodes": [
    {
      "id": "node-1",
      "type": "product-vision",
      "label": "Product Vision",
      "category": "Planning",
      "x": 100,
      "y": 100,
      "color": "#3b82f6"
    }
  ],
  "edges": [
    {
      "id": "edge-1",
      "fromId": "node-1",
      "toId": "node-2",
      "relationship": "successor"
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Workflow created successfully",
  "workflowId": "new-uuid-here"
}
```

**Example:**
```bash
curl -X POST http://localhost:3001/api/workflows \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Workflow",
    "status": "active",
    "nodes": [],
    "edges": []
  }'
```

---

#### PUT /api/workflows/:id

Update an existing workflow.

**Parameters:**
- `id` (path) - Workflow UUID

**Request Body:**
```json
{
  "name": "Updated Workflow Name",
  "status": "paused",
  "nodes": [...],
  "edges": [...]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Workflow updated successfully"
}
```

**Example:**
```bash
curl -X PUT http://localhost:3001/api/workflows/abc-123 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Name",
    "status": "active",
    "nodes": [],
    "edges": []
  }'
```

---

#### DELETE /api/workflows/:id

Delete a workflow and all its nodes and edges.

**Parameters:**
- `id` (path) - Workflow UUID

**Response:**
```json
{
  "success": true,
  "message": "Workflow deleted successfully"
}
```

**Example:**
```bash
curl -X DELETE http://localhost:3001/api/workflows/abc-123
```

---

## Data Models

### Workflow

```typescript
{
  id: string;           // UUID
  name: string;         // Workflow name
  status: string;       // "active" | "paused" | "draft"
  created_at: string;   // ISO 8601 timestamp
  updated_at: string;   // ISO 8601 timestamp
  nodes: Node[];        // Array of nodes
  edges: Edge[];        // Array of edges
}
```

### Node

```typescript
{
  id: string;           // Node ID (e.g., "node-1")
  type: string;         // Node type (e.g., "product-vision")
  label: string;        // Display label
  category: string;     // Category (e.g., "Planning")
  x: number;            // X position on canvas
  y: number;            // Y position on canvas
  color: string;        // Hex color (e.g., "#3b82f6")
}
```

### Edge

```typescript
{
  id: string;           // Edge ID (e.g., "edge-1")
  fromId: string;       // Source node ID
  toId: string;         // Target node ID
  relationship: string; // Relationship type (e.g., "successor")
}
```

### Relationship Types

- `successor` - Sequential flow
- `predecessor` - Reverse flow
- `triggers` - Activation relationship
- `blocks` - Blocking relationship
- `validates` - Validation relationship
- `generates` - Generation relationship
- `depends-on` - Dependency relationship
- `reviewed-by` - Review relationship

---

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid input |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error |

---

## Rate Limiting

Currently, no rate limiting is implemented. This will be added in future versions.

---

## Examples

### Complete Workflow Creation Flow

```bash
# 1. Create a workflow
WORKFLOW_ID=$(curl -X POST http://localhost:3001/api/workflows \
  -H "Content-Type: application/json" \
  -d '{
    "name": "E-commerce Product Launch",
    "status": "active",
    "nodes": [
      {
        "id": "node-1",
        "type": "product-vision",
        "label": "Product Vision",
        "category": "Planning",
        "x": 100,
        "y": 100,
        "color": "#3b82f6"
      },
      {
        "id": "node-2",
        "type": "requirements",
        "label": "Requirements",
        "category": "Planning",
        "x": 300,
        "y": 100,
        "color": "#3b82f6"
      }
    ],
    "edges": [
      {
        "id": "edge-1",
        "fromId": "node-1",
        "toId": "node-2",
        "relationship": "successor"
      }
    ]
  }' | jq -r '.workflowId')

# 2. Retrieve the workflow
curl http://localhost:3001/api/workflows/$WORKFLOW_ID | jq

# 3. Update the workflow
curl -X PUT http://localhost:3001/api/workflows/$WORKFLOW_ID \
  -H "Content-Type: application/json" \
  -d '{
    "name": "E-commerce Product Launch v2",
    "status": "active",
    "nodes": [...],
    "edges": [...]
  }' | jq

# 4. Delete the workflow
curl -X DELETE http://localhost:3001/api/workflows/$WORKFLOW_ID | jq
```

---

## Testing

Use the provided examples with `curl` or use tools like:

- **Postman** - GUI for API testing
- **Insomnia** - REST client
- **HTTPie** - Command-line HTTP client

---

## Support

For issues or questions, please refer to the main [README.md](README.md).

```


### `GITHUB_SETUP.md`

```md
# GitHub Repository Setup

Instructions to push this backend code to a new GitHub repository.

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `agenticSDLC-backend`
3. Description: `Backend API server for AgenticSDLC workflow orchestration platform`
4. Visibility: Choose Public or Private
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Step 2: Configure Git Remote

GitHub will show you commands. Use these:

```bash
cd agenticSDLC-backend
git remote add origin https://github.com/YOUR_USERNAME/agenticSDLC-backend.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 3: Verify

1. Go to your GitHub repository page
2. You should see all files including:
   - README.md
   - SETUP.md
   - API.md
   - config/, db/, models/, routes/ folders
   - server.js, package.json

## Step 4: Update Frontend Reference

In your frontend repository (`agenticSDLC-UI-Code`):

Update README.md to reference the backend repo:
```markdown
## Related Repositories

- **Backend**: https://github.com/YOUR_USERNAME/agenticSDLC-backend
- **Agents**: https://github.com/YOUR_USERNAME/agenticsdlc-agents
```

## Step 5: Add Topics (Optional)

On GitHub repository page:
1. Click "⚙️ Settings"
2. Under "Topics", add:
   - `nodejs`
   - `express`
   - `postgresql`
   - `rest-api`
   - `workflow`
   - `orchestration`

## Example Remote URLs

### HTTPS (recommended)
```bash
git remote add origin https://github.com/YOUR_USERNAME/agenticSDLC-backend.git
```

### SSH (if you have SSH keys set up)
```bash
git remote add origin git@github.com:YOUR_USERNAME/agenticSDLC-backend.git
```

## Verify Remote

```bash
git remote -v
```

Should show:
```
origin  https://github.com/YOUR_USERNAME/agenticSDLC-backend.git (fetch)
origin  https://github.com/YOUR_USERNAME/agenticSDLC-backend.git (push)
```

## Clone Instructions for Others

After pushing, others can clone with:
```bash
git clone https://github.com/YOUR_USERNAME/agenticSDLC-backend.git
cd agenticSDLC-backend
npm install
cp .env.example .env
# Edit .env with database credentials
npm run setup-db
npm run dev
```

## Repository Settings Recommendations

### Branch Protection
1. Go to Settings → Branches
2. Add rule for `main` branch
3. Enable:
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass before merging

### Secrets (for CI/CD)
If you add GitHub Actions later:
1. Settings → Secrets and variables → Actions
2. Add secrets like:
   - `DB_PASSWORD`
   - `DATABASE_URL`

## Next Steps

After pushing to GitHub:
1. ✅ Repository is now backed up
2. ✅ Others can collaborate
3. ✅ Can set up CI/CD pipelines
4. ✅ Can deploy to cloud services

## Integration with Frontend

The frontend repository should reference this backend:

**In frontend `.env`:**
```env
# Development
VITE_API_BASE_URL=http://localhost:3001

# Production
VITE_API_BASE_URL=https://api.your-domain.com
```

**In frontend README:**
```markdown
## Backend Repository

This frontend connects to the AgenticSDLC Backend API.

Repository: https://github.com/YOUR_USERNAME/agenticSDLC-backend

See backend README for setup instructions.
```

## Common Issues

### Push rejected
```bash
git pull origin main --rebase
git push -u origin main
```

### Authentication failed
Use a Personal Access Token instead of password:
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` scope
3. Use token as password when pushing

### Wrong remote URL
```bash
git remote remove origin
git remote add origin <correct-url>
```

## Done!

Your backend is now on GitHub and ready for collaboration! 🎉

```


### `QUICKSTART.md`

```md
# Quick Start Guide

Get the backend running in 3 minutes.

## Prerequisites
- Node.js installed
- PostgreSQL installed and running
- Database credentials ready

## Steps

### 1. Install Dependencies (30 seconds)
```bash
npm install
```

### 2. Configure Environment (1 minute)
```bash
cp .env.example .env
```

Edit `.env`:
```env
DB_PASSWORD="YourActualPassword"
```

### 3. Setup Database (30 seconds)
```bash
npm run setup-db
```

### 4. Start Server (10 seconds)
```bash
npm run dev
```

## Verify

Open browser: http://localhost:3001/health

Should see:
```json
{"status":"ok","timestamp":"..."}
```

## Done! ✅

Backend is now running on port 3001.

## Next

- Read [SETUP.md](SETUP.md) for detailed instructions
- Check [API.md](API.md) for API documentation
- See [README.md](README.md) for complete guide

## Troubleshooting

**Can't connect to database?**
```bash
npm run test-db
```

**Port 3001 already in use?**
```bash
# Windows
netstat -ano | findstr :3001
# Kill the process using that port
```

**Need help?**
Check [SETUP.md](SETUP.md) troubleshooting section.

```


### `README.md`

```md
# AgenticSDLC Backend API

Backend API server for the AgenticSDLC workflow orchestration platform.

## Overview

This is a Node.js/Express REST API that provides backend services for managing workflows, nodes, edges, and workflow executions. It connects to a PostgreSQL database and provides endpoints for the frontend application.

## Tech Stack

- **Runtime**: Node.js
- **Framework**: Express.js
- **Database**: PostgreSQL
- **ORM**: pg (node-postgres)
- **Environment**: dotenv

## Features

- RESTful API for workflow management
- PostgreSQL database integration
- Environment-based configuration (dev/staging/production)
- CORS enabled for frontend integration
- Connection pooling for database efficiency
- Comprehensive error handling

## Prerequisites

- Node.js (v16 or higher)
- PostgreSQL (v12 or higher)
- npm or yarn

## Installation

1. Clone the repository:
```bash
git clone <your-backend-repo-url>
cd agenticSDLC-backend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env
```

4. Edit `.env` with your database credentials:
```env
NODE_ENV=development
PORT=3001

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=agenticsdlc
DB_USER=postgres
DB_PASSWORD="YourPassword"

# CORS Configuration
CORS_ORIGIN=http://localhost:5173
```

5. Set up the database:
```bash
npm run setup-db
```

## Database Setup

The database schema includes:

- **workflows** - Workflow definitions
- **workflow_nodes** - Nodes in workflows
- **workflow_edges** - Connections between nodes
- **workflow_executions** - Runtime execution tracking

Run the setup script to create all tables:
```bash
npm run setup-db
```

Or manually run the SQL schema:
```bash
psql -U postgres -d agenticsdlc -f db/schema.sql
```

## Running the Server

### Development Mode
```bash
npm run dev
```

The server will start on `http://localhost:3001` with auto-reload enabled.

### Production Mode
```bash
npm start
```

## API Endpoints

### Health Check
- `GET /health` - Check if server is running

### Workflows
- `GET /api/workflows` - Get all workflows
- `GET /api/workflows/:id` - Get workflow by ID (includes nodes and edges)
- `POST /api/workflows` - Create new workflow
- `PUT /api/workflows/:id` - Update workflow
- `DELETE /api/workflows/:id` - Delete workflow

## Project Structure

```
agenticSDLC-backend/
├── config/
│   └── database.config.js    # Database configuration per environment
├── db/
│   ├── connection.js          # Database connection pool
│   └── schema.sql             # Database schema
├── models/
│   └── workflow.model.js      # Workflow data access layer
├── routes/
│   └── workflow.routes.js     # API route definitions
├── .env                       # Environment variables (not in git)
├── .env.example              # Example environment variables
├── package.json              # Dependencies and scripts
├── server.js                 # Express server entry point
├── setup-database.cjs        # Database setup script
└── test-db-simple.cjs        # Simple database test
```

## Scripts

- `npm start` - Start production server
- `npm run dev` - Start development server with auto-reload
- `npm run setup-db` - Set up database schema
- `npm run test-db` - Test database connection

## Related Repositories

- Frontend: [agenticSDLC-UI-Code](link-to-frontend-repo)
- Agents: [agenticsdlc-agents](link-to-agents-repo)

```


### `REPOSITORY_SETUP.md`

```md
# Repository Connection Setup

This guide explains how to set up the database and backend for the GitHub repository connection feature.

## Prerequisites

- PostgreSQL database running
- Backend server configured (see SETUP.md)
- Node.js and npm installed

## Database Migration

Run the migration to create the `repositories` table:

```bash
cd agenticSDLC-backend
node db/run-migration.cjs 002_create_repositories_table.sql
```

You should see:
```
✅ Migration completed successfully!
```

## Database Schema

The `repositories` table stores connected GitHub repositories with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Unique repository identifier |
| name | VARCHAR(255) | Repository name |
| owner | VARCHAR(255) | Repository owner/organization |
| full_name | VARCHAR(512) | Full repository name (owner/repo) |
| language | VARCHAR(100) | Primary programming language |
| stars | INTEGER | Number of GitHub stars |
| branches | INTEGER | Number of branches |
| description | TEXT | Repository description |
| url | TEXT | GitHub repository URL |
| status | VARCHAR(50) | Connection status (active/inactive) |
| connected_at | TIMESTAMP | When repository was connected |
| created_at | TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | Record last update timestamp |

## API Endpoints

### GET /api/repositories
Get all connected repositories

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "name": "claude-code",
      "owner": "anthropics",
      "fullName": "anthropics/claude-code",
      "language": "TypeScript",
      "stars": 1234,
      "branches": 5,
      "description": "Claude Code CLI tool",
      "url": "https://github.com/anthropics/claude-code",
      "status": "active",
      "connectedAt": "2024-06-05T10:00:00Z",
      "created_at": "2024-06-05T10:00:00Z",
      "updated_at": "2024-06-05T10:00:00Z"
    }
  ]
}
```

### POST /api/repositories
Connect a new repository

**Request:**
```json
{
  "name": "claude-code",
  "owner": "anthropics",
  "fullName": "anthropics/claude-code",
  "language": "TypeScript",
  "stars": 1234,
  "branches": 5,
  "description": "Claude Code CLI tool",
  "url": "https://github.com/anthropics/claude-code",
  "status": "active"
}
```

**Response:**
```json
{
  "success": true,
  "data": { /* repository object */ },
  "message": "Repository connected successfully"
}
```

### PUT /api/repositories/:id
Update repository details

**Request:**
```json
{
  "stars": 1500,
  "branches": 8
}
```

### DELETE /api/repositories/:id
Disconnect a repository

**Response:**
```json
{
  "success": true,
  "message": "Repository disconnected successfully"
}
```

## Testing

### 1. Check Backend is Running
```bash
curl http://localhost:3001/health
```

### 2. Connect a Repository (via frontend)
- Go to GitHub Operations → Repositories
- Click "Connect Repository"
- Enter owner: `anthropics`
- Enter name: `claude-code`
- Click "Connect"

### 3. Verify Database
```bash
psql -U agenticsdlc_user -d agenticsdlc -c "SELECT * FROM repositories;"
```

## Troubleshooting

### Migration fails
- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Verify database exists: `psql -U agenticsdlc_user -l`

### API returns 500 error
- Check backend logs for errors
- Verify database connection in `config/database.config.js`
- Ensure migration ran successfully

### Repository already exists error
- Each repository can only be connected once
- Use full_name (owner/repo) to identify unique repositories
- Delete existing entry to reconnect

## Features

✅ **Connect Repository** - Link any public GitHub repository  
✅ **Save to Database** - Persistent storage of repository details  
✅ **Load on Startup** - Automatically load connected repos  
✅ **Disconnect** - Remove repository connections  
✅ **Real-time Updates** - Fetch live data from GitHub API  
✅ **Empty State** - Clean UI when no repos connected  

## Next Steps

- Add repository sync to update stars/branches
- Show commit activity graphs
- Display GitHub Actions workflows
- Add webhook integration for real-time updates

```


### `SETUP.md`

```md
# Setup Guide - AgenticSDLC Backend

Quick setup guide to get the backend API running.

## Step 1: Install Dependencies

```bash
npm install
```

## Step 2: Configure Environment

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` with your configuration:
```env
NODE_ENV=development
PORT=3001

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=agenticsdlc
DB_USER=postgres
DB_PASSWORD="YourPassword"

# CORS Configuration
CORS_ORIGIN=http://localhost:5173
```

**Important**: Quote passwords with special characters!

## Step 3: Set Up Database

### Option A: Automated Setup (Recommended)
```bash
npm run setup-db
```

This will:
- Create the database if it doesn't exist
- Create all required tables
- Set up indexes and constraints

### Option B: Manual Setup
```bash
# Create database
createdb -U postgres agenticsdlc

# Run schema
psql -U postgres -d agenticsdlc -f db/schema.sql
```

## Step 4: Test Database Connection

```bash
npm run test-db
```

Expected output:
```
✅ Database connection successful
```

## Step 5: Start Server

### Development (with auto-reload)
```bash
npm run dev
```

### Production
```bash
npm start
```

Server will start at: `http://localhost:3001`

## Step 6: Verify Installation

### Test Health Endpoint
```bash
curl http://localhost:3001/health
```

Expected response:
```json
{
  "status": "ok",
  "timestamp": "2024-05-31T00:00:00.000Z"
}
```

### Test Workflows Endpoint
```bash
curl http://localhost:3001/api/workflows
```

Expected response:
```json
{
  "success": true,
  "data": []
}
```

## Troubleshooting

### Port Already in Use

**Windows:**
```bash
netstat -ano | findstr :3001
taskkill /PID <pid> /F
```

**Linux/Mac:**
```bash
lsof -i :3001
kill -9 <pid>
```

### Database Connection Failed

1. Check PostgreSQL is running:
```bash
# Windows
net start postgresql-x64-<version>

# Linux/Mac
sudo systemctl status postgresql
```

2. Verify credentials in `.env`
3. Ensure database exists
4. Quote special characters in password

### Common Errors

**"ECONNREFUSED"**
- PostgreSQL not running
- Wrong host/port

**"password authentication failed"**
- Wrong credentials
- Password needs quotes

**"database does not exist"**
- Run: `createdb -U postgres agenticsdlc`

## Next Steps

Once the backend is running:

1. Keep the terminal open (server must run continuously)
2. Start the frontend application
3. Access the workflow designer at `http://localhost:5173`

## Scripts Reference

- `npm start` - Start server (production)
- `npm run dev` - Start with auto-reload (development)
- `npm run setup-db` - Initialize database
- `npm run test-db` - Test database connection

## Need Help?

Check the main [README.md](README.md) for detailed documentation.

```


### `package.json`

```json
{
  "name": "agenticsdlc-backend",
  "version": "1.0.0",
  "description": "Backend API for AgenticSDLC Workflow Designer",
  "main": "server.js",
  "type": "module",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js",
    "setup-db": "node setup-database.cjs",
    "test-db": "node test-db-simple.cjs"
  },
  "keywords": [
    "workflow",
    "orchestration",
    "api",
    "rest",
    "express",
    "postgresql"
  ],
  "author": "",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/yourusername/agenticSDLC-backend"
  },
  "dependencies": {
    "body-parser": "^1.20.2",
    "cors": "^2.8.5",
    "dotenv": "^16.3.1",
    "express": "^4.18.2",
    "pg": "^8.21.0"
  },
  "devDependencies": {
    "nodemon": "^3.0.1"
  },
  "engines": {
    "node": ">=16.0.0",
    "npm": ">=8.0.0"
  }
}

```


### `server.js`

```js
/**
 * AgenticSDLC Backend Server
 *
 * Main Express server for handling workflow API requests
 */

// Load env FIRST — must be before any other import that reads process.env
import dotenv from 'dotenv';
dotenv.config();

import express from 'express';
import cors from 'cors';
import bodyParser from 'body-parser';
import workflowRoutes from './routes/workflow.routes.js';
import repositoryRoutes from './routes/repository.routes.js';
import executionRoutes from './routes/execution.routes.js';
import { environment } from './config/database.config.js';

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors({
  origin: process.env.CORS_ORIGIN || 'http://localhost:5173',
  credentials: true,
}));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Request logging
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
  next();
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    environment: environment,
    timestamp: new Date().toISOString(),
  });
});

// API routes
app.use('/api/workflows', workflowRoutes);
app.use('/api/workflows/:id', executionRoutes);
app.use('/api/repositories', repositoryRoutes);

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    success: false,
    error: 'Endpoint not found',
    path: req.path,
  });
});

// Error handler
app.use((err, req, res, next) => {
  console.error('Server error:', err);
  res.status(500).json({
    success: false,
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'development' ? err.message : undefined,
  });
});

// Start server
app.listen(PORT, () => {
  console.log('');
  console.log('╔════════════════════════════════════════╗');
  console.log('║   AgenticSDLC Backend Server Started   ║');
  console.log('╚════════════════════════════════════════╝');
  console.log('');
  console.log(`🚀 Server running on: http://localhost:${PORT}`);
  console.log(`🌍 Environment: ${environment}`);
  console.log(`📡 API endpoint: http://localhost:${PORT}/api/workflows`);
  console.log(`💚 Health check: http://localhost:${PORT}/health`);
  console.log('');
  console.log('Press Ctrl+C to stop the server');
  console.log('');
});

export default app;

```


### `config/database.config.js`

```js
/**
 * Database Configuration
 *
 * This file contains database connection settings for different environments.
 * Update these settings based on your PostgreSQL setup.
 */

import dotenv from 'dotenv';
dotenv.config();

const environments = {
  development: {
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 5432,
    database: process.env.DB_NAME || 'agenticsdlc_dev',
    user: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD || 'postgres',
    max: 20, // Maximum number of clients in the pool
    idleTimeoutMillis: 30000, // How long a client is allowed to remain idle
    connectionTimeoutMillis: 2000, // How long to wait for a connection
  },

  staging: {
    host: process.env.DB_HOST || 'staging-db.example.com',
    port: process.env.DB_PORT || 5432,
    database: process.env.DB_NAME || 'agenticsdlc_staging',
    user: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD,
    max: 50,
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 2000,
    ssl: {
      rejectUnauthorized: false, // For staging
    },
  },

  production: {
    host: process.env.DB_HOST,
    port: process.env.DB_PORT || 5432,
    database: process.env.DB_NAME,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    max: 100,
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 2000,
    ssl: {
      rejectUnauthorized: true, // Enforce SSL in production
      ca: process.env.DB_SSL_CA, // SSL certificate
    },
  },
};

// Get current environment from NODE_ENV or default to development
const currentEnv = process.env.NODE_ENV || 'development';

// Validate required environment variables in production
if (currentEnv === 'production') {
  const required = ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD'];
  const missing = required.filter(key => !process.env[key]);

  if (missing.length > 0) {
    throw new Error(`Missing required environment variables: ${missing.join(', ')}`);
  }
}

// Export the configuration for the current environment
export const dbConfig = environments[currentEnv];

// Export environment name for logging
export const environment = currentEnv;

// Export all environments for reference
export default environments;

```


### `db/connection.js`

```js
/**
 * Database Connection Pool
 *
 * This file manages the PostgreSQL connection pool using pg library.
 */

import pkg from 'pg';
const { Pool } = pkg;
import { dbConfig, environment } from '../config/database.config.js';

// Create connection pool
const pool = new Pool(dbConfig);

// Log pool creation
console.log(`🔌 Database pool created for environment: ${environment}`);
console.log(`📍 Connecting to: ${dbConfig.host}:${dbConfig.port}/${dbConfig.database}`);

// Handle pool errors
pool.on('error', (err, client) => {
  console.error('❌ Unexpected error on idle client', err);
  process.exit(-1);
});

// Test connection on startup
pool.query('SELECT NOW()', (err, res) => {
  if (err) {
    console.error('❌ Database connection failed:', err.message);
  } else {
    console.log('✅ Database connected successfully at:', res.rows[0].now);
  }
});

/**
 * Execute a query
 * @param {string} text - SQL query
 * @param {Array} params - Query parameters
 * @returns {Promise} Query result
 */
export const query = async (text, params) => {
  const start = Date.now();
  try {
    const res = await pool.query(text, params);
    const duration = Date.now() - start;
    console.log('📊 Query executed:', { text, duration: `${duration}ms`, rows: res.rowCount });
    return res;
  } catch (error) {
    console.error('❌ Query error:', { text, error: error.message });
    throw error;
  }
};

/**
 * Get a client from the pool for transactions
 * @returns {Promise} Client connection
 */
export const getClient = async () => {
  const client = await pool.connect();
  const query = client.query.bind(client);
  const release = client.release.bind(client);

  // Set a timeout to release client after 30 seconds
  const timeout = setTimeout(() => {
    console.warn('⚠️ Client has been checked out for more than 30 seconds!');
  }, 30000);

  // Override release to clear timeout
  client.release = () => {
    clearTimeout(timeout);
    client.removeAllListeners('error');
    release();
  };

  return client;
};

/**
 * Gracefully close the pool
 */
export const close = async () => {
  await pool.end();
  console.log('🔌 Database pool closed');
};

// Handle process termination
process.on('SIGINT', async () => {
  await close();
  process.exit(0);
});

process.on('SIGTERM', async () => {
  await close();
  process.exit(0);
});

export default { query, getClient, close };

```


### `db/schema.sql`

```sql
-- AgenticSDLC Workflow Database Schema
-- PostgreSQL 12+

-- Create extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Workflows table
CREATE TABLE IF NOT EXISTS workflows (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'draft' CHECK (status IN ('draft', 'active', 'paused', 'archived')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(255),
    version INTEGER DEFAULT 1,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Workflow nodes table
CREATE TABLE IF NOT EXISTS workflow_nodes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
    node_id VARCHAR(100) NOT NULL, -- Client-side generated ID
    node_type VARCHAR(100) NOT NULL,
    label VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    color VARCHAR(20) NOT NULL,
    position_x NUMERIC(10, 2) NOT NULL,
    position_y NUMERIC(10, 2) NOT NULL,
    config JSONB DEFAULT '{}'::jsonb, -- Additional node configuration
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(workflow_id, node_id)
);

-- Workflow edges table
CREATE TABLE IF NOT EXISTS workflow_edges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
    edge_id VARCHAR(100) NOT NULL, -- Client-side generated ID
    from_node_id VARCHAR(100) NOT NULL,
    to_node_id VARCHAR(100) NOT NULL,
    relationship VARCHAR(100) NOT NULL,
    config JSONB DEFAULT '{}'::jsonb, -- Additional edge configuration
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(workflow_id, edge_id),
    FOREIGN KEY (workflow_id, from_node_id) REFERENCES workflow_nodes(workflow_id, node_id) ON DELETE CASCADE,
    FOREIGN KEY (workflow_id, to_node_id) REFERENCES workflow_nodes(workflow_id, node_id) ON DELETE CASCADE
);

-- Workflow execution history
CREATE TABLE IF NOT EXISTS workflow_executions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'running' CHECK (status IN ('running', 'completed', 'failed', 'cancelled')),
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    duration_ms INTEGER,
    result JSONB,
    error_message TEXT,
    triggered_by VARCHAR(255)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_workflows_status ON workflows(status);
CREATE INDEX IF NOT EXISTS idx_workflows_created_at ON workflows(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_workflow_nodes_workflow_id ON workflow_nodes(workflow_id);
CREATE INDEX IF NOT EXISTS idx_workflow_edges_workflow_id ON workflow_edges(workflow_id);
CREATE INDEX IF NOT EXISTS idx_workflow_executions_workflow_id ON workflow_executions(workflow_id);
CREATE INDEX IF NOT EXISTS idx_workflow_executions_status ON workflow_executions(status);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for workflows table
CREATE TRIGGER update_workflows_updated_at
    BEFORE UPDATE ON workflows
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Sample data (optional - for testing)
-- INSERT INTO workflows (name, description, status, created_by)
-- VALUES ('Sample Workflow', 'Test workflow for development', 'draft', 'system');

-- View for workflow summary
CREATE OR REPLACE VIEW workflow_summary AS
SELECT
    w.id,
    w.name,
    w.status,
    w.created_at,
    w.updated_at,
    COUNT(DISTINCT wn.id) as node_count,
    COUNT(DISTINCT we.id) as edge_count,
    COUNT(DISTINCT wex.id) as execution_count
FROM workflows w
LEFT JOIN workflow_nodes wn ON w.id = wn.workflow_id
LEFT JOIN workflow_edges we ON w.id = we.workflow_id
LEFT JOIN workflow_executions wex ON w.id = wex.workflow_id
GROUP BY w.id, w.name, w.status, w.created_at, w.updated_at;

-- Grant permissions (adjust based on your user setup)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_db_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_db_user;

```


### `db/migrations/002_create_repositories_table.sql`

```sql
-- Migration: Create repositories table
-- Description: Stores connected GitHub repositories
-- Date: 2024-06-05

-- Create repositories table
CREATE TABLE IF NOT EXISTS repositories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  owner VARCHAR(255) NOT NULL,
  full_name VARCHAR(512) NOT NULL UNIQUE,
  language VARCHAR(100),
  stars INTEGER DEFAULT 0,
  branches INTEGER DEFAULT 0,
  description TEXT,
  url TEXT NOT NULL,
  status VARCHAR(50) DEFAULT 'active',
  connected_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_repositories_full_name ON repositories(full_name);
CREATE INDEX IF NOT EXISTS idx_repositories_owner ON repositories(owner);
CREATE INDEX IF NOT EXISTS idx_repositories_status ON repositories(status);
CREATE INDEX IF NOT EXISTS idx_repositories_created_at ON repositories(created_at DESC);

-- Add comments
COMMENT ON TABLE repositories IS 'Connected GitHub repositories';
COMMENT ON COLUMN repositories.id IS 'Unique repository identifier';
COMMENT ON COLUMN repositories.name IS 'Repository name';
COMMENT ON COLUMN repositories.owner IS 'Repository owner/organization';
COMMENT ON COLUMN repositories.full_name IS 'Full repository name (owner/repo)';
COMMENT ON COLUMN repositories.language IS 'Primary programming language';
COMMENT ON COLUMN repositories.stars IS 'Number of GitHub stars';
COMMENT ON COLUMN repositories.branches IS 'Number of branches';
COMMENT ON COLUMN repositories.description IS 'Repository description';
COMMENT ON COLUMN repositories.url IS 'GitHub repository URL';
COMMENT ON COLUMN repositories.status IS 'Connection status (active/inactive)';
COMMENT ON COLUMN repositories.connected_at IS 'When repository was connected';
COMMENT ON COLUMN repositories.created_at IS 'Record creation timestamp';
COMMENT ON COLUMN repositories.updated_at IS 'Record last update timestamp';

-- Log migration completion
DO $$
BEGIN
  RAISE NOTICE 'Migration completed: 002_create_repositories_table';
END $$;

```


### `db/migrations/002_workflow_node_executions.sql`

```sql
-- Migration 002: Add workflow node executions table for per-node execution tracking

CREATE TABLE IF NOT EXISTS workflow_node_executions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
    execution_id UUID NOT NULL REFERENCES workflow_executions(id) ON DELETE CASCADE,
    node_id VARCHAR(100) NOT NULL,
    node_type VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending'
        CHECK (status IN ('pending', 'running', 'completed', 'failed', 'awaiting_approval', 'rejected')),
    github_run_id BIGINT,                  -- GitHub Actions run ID once triggered
    github_workflow_file VARCHAR(255),     -- e.g. code-analyst.yml
    inputs JSONB DEFAULT '{}'::jsonb,      -- inputs passed to the GitHub workflow
    outputs JSONB DEFAULT '{}'::jsonb,     -- any outputs captured
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(execution_id, node_id)
);

-- Extend workflow_executions to carry current executing node
ALTER TABLE workflow_executions
    ADD COLUMN IF NOT EXISTS current_node_id VARCHAR(100),
    ADD COLUMN IF NOT EXISTS triggered_nodes JSONB DEFAULT '[]'::jsonb;

-- Indexes
CREATE INDEX IF NOT EXISTS idx_wne_workflow_id   ON workflow_node_executions(workflow_id);
CREATE INDEX IF NOT EXISTS idx_wne_execution_id  ON workflow_node_executions(execution_id);
CREATE INDEX IF NOT EXISTS idx_wne_status        ON workflow_node_executions(status);
CREATE INDEX IF NOT EXISTS idx_wne_github_run_id ON workflow_node_executions(github_run_id);

```


### `models/Repository.js`

```js
/**
 * Repository Model
 *
 * Handles all database operations for connected GitHub repositories
 */

import { query } from '../db/connection.js';

export class Repository {
  /**
   * Find all repositories
   * @returns {Promise<Array>} List of repositories
   */
  static async findAll() {
    const result = await query(
      `SELECT
        id,
        name,
        owner,
        full_name as "fullName",
        language,
        stars,
        branches,
        description,
        url,
        status,
        connected_at as "connectedAt",
        created_at,
        updated_at
      FROM repositories
      ORDER BY created_at DESC`
    );

    return result.rows;
  }

  /**
   * Find repository by ID
   * @param {string} id - Repository ID
   * @returns {Promise<Object|null>} Repository or null
   */
  static async findById(id) {
    const result = await query(
      `SELECT
        id,
        name,
        owner,
        full_name as "fullName",
        language,
        stars,
        branches,
        description,
        url,
        status,
        connected_at as "connectedAt",
        created_at,
        updated_at
      FROM repositories
      WHERE id = $1`,
      [id]
    );

    return result.rows[0] || null;
  }

  /**
   * Find repository by full name (owner/repo)
   * @param {string} fullName - Repository full name (e.g., "owner/repo")
   * @returns {Promise<Object|null>} Repository or null
   */
  static async findByFullName(fullName) {
    const result = await query(
      `SELECT
        id,
        name,
        owner,
        full_name as "fullName",
        language,
        stars,
        branches,
        description,
        url,
        status,
        connected_at as "connectedAt",
        created_at,
        updated_at
      FROM repositories
      WHERE full_name = $1`,
      [fullName]
    );

    return result.rows[0] || null;
  }

  /**
   * Create a new repository
   * @param {Object} data - Repository data
   * @returns {Promise<Object>} Created repository
   */
  static async create(data) {
    const {
      name,
      owner,
      full_name,
      language,
      stars,
      branches,
      description,
      url,
      status,
      connected_at
    } = data;

    const result = await query(
      `INSERT INTO repositories (
        name,
        owner,
        full_name,
        language,
        stars,
        branches,
        description,
        url,
        status,
        connected_at
      )
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
      RETURNING
        id,
        name,
        owner,
        full_name as "fullName",
        language,
        stars,
        branches,
        description,
        url,
        status,
        connected_at as "connectedAt",
        created_at,
        updated_at`,
      [
        name,
        owner,
        full_name,
        language || 'Unknown',
        stars || 0,
        branches || 0,
        description || null,
        url,
        status || 'active',
        connected_at || new Date().toISOString()
      ]
    );

    return result.rows[0];
  }

  /**
   * Update a repository
   * @param {string} id - Repository ID
   * @param {Object} updates - Fields to update
   * @returns {Promise<Object>} Updated repository
   */
  static async update(id, updates) {
    const fields = [];
    const values = [];
    let paramIndex = 1;

    // Build dynamic SET clause
    for (const [key, value] of Object.entries(updates)) {
      fields.push(`${key} = $${paramIndex}`);
      values.push(value);
      paramIndex++;
    }

    // Add updated_at
    fields.push(`updated_at = NOW()`);

    // Add id for WHERE clause
    values.push(id);

    const result = await query(
      `UPDATE repositories
       SET ${fields.join(', ')}
       WHERE id = $${paramIndex}
       RETURNING
        id,
        name,
        owner,
        full_name as "fullName",
        language,
        stars,
        branches,
        description,
        url,
        status,
        connected_at as "connectedAt",
        created_at,
        updated_at`,
      values
    );

    return result.rows[0];
  }

  /**
   * Delete a repository
   * @param {string} id - Repository ID
   * @returns {Promise<boolean>} Success status
   */
  static async delete(id) {
    const result = await query(
      `DELETE FROM repositories WHERE id = $1`,
      [id]
    );

    return result.rowCount > 0;
  }
}

export default Repository;

```


### `models/execution.model.js`

```js
/**
 * Execution Model
 *
 * Drives sequential, graph-aware execution of workflow nodes.
 * Each node triggers its corresponding GitHub Actions workflow.
 * human-in-loop nodes pause execution until approved via API.
 */

import https from 'https';
import { query, getClient } from '../db/connection.js';
import { WorkflowModel } from './workflow.model.js';

// Works on Node 16+ (no dependency on global fetch)
function httpsRequest(url, options = {}, body = null) {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const reqOptions = {
      hostname: parsed.hostname,
      path: parsed.pathname + parsed.search,
      method: options.method || 'GET',
      headers: options.headers || {},
      rejectUnauthorized: false, // corporate proxy uses self-signed cert
    };
    const req = https.request(reqOptions, (res) => {
      let data = '';
      res.on('data', chunk => { data += chunk; });
      res.on('end', () => {
        const body = data;
        resolve({
          status: res.statusCode,
          ok: res.statusCode >= 200 && res.statusCode < 300,
          json: () => Promise.resolve(body ? JSON.parse(body) : {}),
          text: () => Promise.resolve(body),
        });
      });
      res.on('error', reject);
    });
    // 15 second timeout
    req.setTimeout(15000, () => {
      req.destroy(new Error('Request timed out after 15s'));
    });
    req.on('error', (err) => {
      console.error(`[httpsRequest] Error for ${options.method || 'GET'} ${url}: ${err.message}`);
      reject(err);
    });
    if (body) req.write(body);
    req.end();
  });
}

// Ensure tables exist on first use (idempotent)
async function ensureSchema() {
  await query(`
    CREATE TABLE IF NOT EXISTS workflow_node_executions (
      id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
      workflow_id UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
      execution_id UUID NOT NULL REFERENCES workflow_executions(id) ON DELETE CASCADE,
      node_id VARCHAR(100) NOT NULL,
      node_type VARCHAR(100) NOT NULL,
      status VARCHAR(50) DEFAULT 'pending'
        CHECK (status IN ('pending','running','completed','failed','awaiting_approval','rejected')),
      github_run_id BIGINT,
      github_workflow_file VARCHAR(255),
      inputs JSONB DEFAULT '{}'::jsonb,
      outputs JSONB DEFAULT '{}'::jsonb,
      started_at TIMESTAMP WITH TIME ZONE,
      completed_at TIMESTAMP WITH TIME ZONE,
      error_message TEXT,
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      UNIQUE(execution_id, node_id)
    )
  `);
  // Add columns to workflow_executions if missing
  await query(`ALTER TABLE workflow_executions ADD COLUMN IF NOT EXISTS current_node_id VARCHAR(100)`);
  await query(`ALTER TABLE workflow_executions ADD COLUMN IF NOT EXISTS triggered_nodes JSONB DEFAULT '[]'::jsonb`);
}

const GITHUB_API_BASE = 'https://api.github.com';

// Read lazily at call-time — constants evaluated at import time miss dotenv
function ghToken() { return process.env.GITHUB_TOKEN || ''; }
function ghOwner() { return process.env.GITHUB_OWNER || ''; }
function ghRepo()  { return process.env.GITHUB_REPO  || ''; }

// Map canvas node types → GitHub workflow files + input key from node config
const NODE_WORKFLOW_MAP = {
  'product-vision':   { file: 'product-agent.yml',       inputKey: 'vision_document' },
  'prd':              { file: 'business-analyst.yml',     inputKey: 'vision_path' },
  'epic':             { file: 'product-strategist.yml',   inputKey: 'prd_path' },
  'user-story':       { file: 'product-strategist.yml',   inputKey: 'epic_path' },
  'code-analysis':    { file: 'code-analyst.yml',         inputKey: 'repository_url_or_path' },
  'design-analysis':  { file: 'design-analyst.yml',       inputKey: 'design_path' },
  'hld':              { file: 'solution-architect.yml',   inputKey: 'requirements_path' },
  'lld':              { file: 'architecture-agent.yml',   inputKey: 'hld_path' },
  'adr':              { file: 'solution-architect.yml',   inputKey: 'context_path' },
  'api-contract':     { file: 'solution-architect.yml',   inputKey: 'spec_path' },
  'ui-ux':            { file: 'design-analyst.yml',       inputKey: 'requirements_path' },
  'code-module':      { file: 'frontend-developer.yml',   inputKey: 'story_path' },
  'pull-request':     null, // auto-created by dev agent, no trigger
  'test-strategy':    { file: 'qa-agent.yml',             inputKey: 'requirements_path' },
  'test-cases':       { file: 'qa-engineer.yml',          inputKey: 'test_strategy_path' },
  'test-plan':        { file: 'qa-agent.yml',             inputKey: 'story_path' },
  'test-suite':       { file: 'qa-engineer.yml',          inputKey: 'test_cases_path' },
  'test-report':      { file: 'qa-engineer.yml',          inputKey: 'test_suite_path' },
  'ai-agent-reviewer':{ file: 'security-reviewer.yml',    inputKey: 'code_path' },
  'human-in-loop':    null, // PAUSE — requires human approval
  'deployment':       { file: 'devops-agent.yml',         inputKey: 'artifact_path' },
  'release':          { file: 'devops-agent.yml',         inputKey: 'deployment_path' },
  'incident':         { file: 'incident-analyzer.yml',    inputKey: 'incident_details' },
  'monitoring':       { file: 'sre-agent.yml',            inputKey: 'service_name' },
};

// ---------- GitHub helpers ----------

async function githubDispatch(workflowFile, inputs = {}) {
  const url = `${GITHUB_API_BASE}/repos/${ghOwner()}/${ghRepo()}/actions/workflows/${workflowFile}/dispatches`;
  const body = JSON.stringify({ ref: 'main', inputs });
  console.log(`[GitHub] Dispatching ${workflowFile} | Owner: ${ghOwner()} | Repo: ${ghRepo()} | Token: ${ghToken() ? 'present' : 'MISSING'}`);
  console.log(`[GitHub] Inputs being sent: ${body}`);
  const res = await httpsRequest(url, {
    method: 'POST',
    headers: {
      'Accept': 'application/vnd.github+json',
      'Authorization': `Bearer ${ghToken()}`,
      'X-GitHub-Api-Version': '2022-11-28',
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(body),
      'User-Agent': 'agenticSDLC-backend/1.0',
    },
  }, body);
  const responseText = await res.text();
  console.log(`[GitHub] Dispatch response: ${res.status} | Body: ${responseText || '(empty)'}`);
  if (res.status !== 204 && !res.ok) {
    throw new Error(responseText || `GitHub dispatch failed: ${res.status}`);
  }
}

async function getLatestGitHubRunId(workflowFile) {
  await new Promise(r => setTimeout(r, 4000));
  const url = `${GITHUB_API_BASE}/repos/${ghOwner()}/${ghRepo()}/actions/workflows/${workflowFile}/runs?per_page=1`;
  const res = await httpsRequest(url, {
    headers: {
      'Accept': 'application/vnd.github+json',
      'Authorization': `Bearer ${ghToken()}`,
      'X-GitHub-Api-Version': '2022-11-28',
      'User-Agent': 'agenticSDLC-backend/1.0',
    },
  });
  if (!res.ok) return null;
  const data = await res.json();
  return data.workflow_runs?.[0]?.id ?? null;
}

async function pollGitHubRunUntilDone(runId, timeoutMs = 30 * 60 * 1000) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    await new Promise(r => setTimeout(r, 15000));
    const url = `${GITHUB_API_BASE}/repos/${ghOwner()}/${ghRepo()}/actions/runs/${runId}`;
    const res = await httpsRequest(url, {
      headers: {
        'Accept': 'application/vnd.github+json',
        'Authorization': `Bearer ${ghToken()}`,
        'X-GitHub-Api-Version': '2022-11-28',
      },
    });
    if (!res.ok) continue;
    const run = await res.json();
    if (run.status === 'completed') {
      return run.conclusion === 'success' ? 'completed' : 'failed';
    }
  }
  return 'failed'; // timed out
}

// ---------- DB helpers ----------

async function updateNodeExecution(executionId, nodeId, fields) {
  const setClauses = Object.keys(fields).map((k, i) => `${k} = $${i + 3}`).join(', ');
  const values = Object.values(fields);
  await query(
    `UPDATE workflow_node_executions SET ${setClauses} WHERE execution_id = $1 AND node_id = $2`,
    [executionId, nodeId, ...values]
  );
}

async function updateExecution(executionId, fields) {
  const setClauses = Object.keys(fields).map((k, i) => `${k} = $${i + 2}`).join(', ');
  const values = Object.values(fields);
  await query(
    `UPDATE workflow_executions SET ${setClauses} WHERE id = $1`,
    [executionId, ...values]
  );
}

// ---------- Topological sort ----------

function topoSort(nodes, edges) {
  const nodeIds = nodes.map(n => n.id);
  const inDegree = Object.fromEntries(nodeIds.map(id => [id, 0]));
  const adj = Object.fromEntries(nodeIds.map(id => [id, []]));

  for (const e of edges) {
    if (inDegree[e.toId] !== undefined) inDegree[e.toId]++;
    if (adj[e.fromId]) adj[e.fromId].push(e.toId);
  }

  const queue = nodeIds.filter(id => inDegree[id] === 0);
  const order = [];

  while (queue.length) {
    const id = queue.shift();
    order.push(id);
    for (const next of (adj[id] || [])) {
      inDegree[next]--;
      if (inDegree[next] === 0) queue.push(next);
    }
  }

  return order.map(id => nodes.find(n => n.id === id)).filter(Boolean);
}

// ---------- Execution Engine ----------

export class ExecutionModel {
  /**
   * Start a new execution for a workflow.
   * Spawns an async loop that drives nodes in topological order.
   */
  static async startExecution(workflowId) {
    await ensureSchema();
    const workflow = await WorkflowModel.getWorkflowById(workflowId);
    if (!workflow) throw new Error('Workflow not found');

    // Create execution record
    const execResult = await query(
      `INSERT INTO workflow_executions (workflow_id, status, triggered_by)
       VALUES ($1, 'running', 'user') RETURNING *`,
      [workflowId]
    );
    const execution = execResult.rows[0];

    // Create per-node execution records
    for (const node of workflow.nodes) {
      await query(
        `INSERT INTO workflow_node_executions
         (workflow_id, execution_id, node_id, node_type, status, inputs)
         VALUES ($1, $2, $3, $4, 'pending', $5)
         ON CONFLICT (execution_id, node_id) DO NOTHING`,
        [workflowId, execution.id, node.id, node.type,
         JSON.stringify(node.config?.inputs || node.config || {})]
      );
    }

    // Update workflow status to active
    await query(`UPDATE workflows SET status = 'active' WHERE id = $1`, [workflowId]);

    // Drive execution asynchronously (fire and forget)
    setImmediate(() => ExecutionModel._drive(execution.id, workflow).catch(err => {
      console.error(`Execution ${execution.id} failed:`, err.message);
      query(`UPDATE workflow_executions SET status = 'failed', completed_at = NOW(),
             error_message = $2 WHERE id = $1`, [execution.id, err.message]);
    }));

    return execution;
  }

  /**
   * Internal: drives nodes in topological order.
   */
  static async _drive(executionId, workflow) {
    const orderedNodes = topoSort(workflow.nodes, workflow.edges);

    for (const node of orderedNodes) {
      // Check if execution was cancelled/rejected
      const execRow = await query(
        `SELECT status FROM workflow_executions WHERE id = $1`, [executionId]
      );
      if (!execRow.rows.length || ['failed', 'cancelled'].includes(execRow.rows[0].status)) break;

      // Mark node running
      await updateNodeExecution(executionId, node.id, {
        status: 'running',
        started_at: new Date(),
      });
      await updateExecution(executionId, { current_node_id: node.id });

      const mapping = NODE_WORKFLOW_MAP[node.type];

      // human-in-loop: pause until approved
      if (node.type === 'human-in-loop') {
        await updateNodeExecution(executionId, node.id, { status: 'awaiting_approval' });
        // Wait for approval (poll DB every 10s)
        const approved = await ExecutionModel._waitForApproval(executionId, node.id);
        if (!approved) {
          await updateNodeExecution(executionId, node.id, {
            status: 'rejected',
            completed_at: new Date(),
          });
          await updateExecution(executionId, {
            status: 'failed',
            completed_at: new Date(),
            error_message: 'Rejected at human review stage',
          });
          await query(`UPDATE workflows SET status = 'paused' WHERE id = $1`, [workflow.id]);
          return;
        }
        await updateNodeExecution(executionId, node.id, {
          status: 'completed',
          completed_at: new Date(),
        });
        continue;
      }

      // No GitHub workflow for this type (e.g. pull-request auto-created)
      if (!mapping) {
        await updateNodeExecution(executionId, node.id, {
          status: 'completed',
          completed_at: new Date(),
        });
        continue;
      }

      // Build inputs: use node's stored config, map to workflow input key
      const nodeInputs = node.config?.inputs || node.config || {};
      const primaryValue = nodeInputs[mapping.inputKey]
        || nodeInputs['repository_url_or_path']
        || nodeInputs['repoToAnalyse']
        || '';
      const githubInputs = { [mapping.inputKey]: primaryValue };

      try {
        // Trigger GitHub Actions
        await githubDispatch(mapping.file, githubInputs);

        // Capture the GitHub run ID
        const githubRunId = await getLatestGitHubRunId(mapping.file);
        if (githubRunId) {
          await updateNodeExecution(executionId, node.id, {
            github_run_id: githubRunId,
            github_workflow_file: mapping.file,
            inputs: JSON.stringify(githubInputs),
          });
        }

        // Poll until GitHub run finishes
        const result = githubRunId
          ? await pollGitHubRunUntilDone(githubRunId)
          : 'completed'; // no run ID — assume success if dispatch didn't throw

        await updateNodeExecution(executionId, node.id, {
          status: result,
          completed_at: new Date(),
        });

        if (result === 'failed') {
          await updateExecution(executionId, {
            status: 'failed',
            completed_at: new Date(),
            error_message: `Node "${node.label}" GitHub workflow failed`,
          });
          await query(`UPDATE workflows SET status = 'paused' WHERE id = $1`, [workflow.id]);
          return;
        }
      } catch (err) {
        console.error(`[_drive] Node "${node.label}" (${node.type}) failed: ${err.message}`);
        await updateNodeExecution(executionId, node.id, {
          status: 'failed',
          completed_at: new Date(),
          error_message: err.message,
        });
        await updateExecution(executionId, {
          status: 'failed',
          completed_at: new Date(),
          error_message: err.message,
        });
        await query(`UPDATE workflows SET status = 'paused' WHERE id = $1`, [workflow.id]);
        return;
      }
    }

    // All nodes done
    await updateExecution(executionId, {
      status: 'completed',
      completed_at: new Date(),
      current_node_id: null,
    });
    await query(`UPDATE workflows SET status = 'archived' WHERE id = $1`, [workflow.id]);
  }

  /**
   * Poll the DB until a human-in-loop node is approved or rejected.
   * Returns true if approved, false if rejected or execution cancelled.
   */
  static async _waitForApproval(executionId, nodeId, timeoutMs = 4 * 60 * 60 * 1000) {
    const start = Date.now();
    while (Date.now() - start < timeoutMs) {
      await new Promise(r => setTimeout(r, 10000));
      const row = await query(
        `SELECT status FROM workflow_node_executions
         WHERE execution_id = $1 AND node_id = $2`,
        [executionId, nodeId]
      );
      const status = row.rows[0]?.status;
      if (status === 'completed') return true;
      if (status === 'rejected') return false;
    }
    return false; // timed out
  }

  /**
   * Get full execution state for a workflow (latest execution + all node statuses).
   */
  static async getExecutionState(workflowId) {
    await ensureSchema();
    const execRow = await query(
      `SELECT * FROM workflow_executions
       WHERE workflow_id = $1
       ORDER BY started_at DESC LIMIT 1`,
      [workflowId]
    );
    if (!execRow.rows.length) return null;
    const execution = execRow.rows[0];

    const nodeRows = await query(
      `SELECT node_id, node_type, status, github_run_id, github_workflow_file,
              inputs, outputs, started_at, completed_at, error_message
       FROM workflow_node_executions
       WHERE execution_id = $1
       ORDER BY created_at`,
      [execution.id]
    );

    return {
      ...execution,
      nodeExecutions: nodeRows.rows,
    };
  }

  /**
   * Approve a human-in-loop node — resumes execution.
   */
  static async approveNode(workflowId, nodeId) {
    const execRow = await query(
      `SELECT id FROM workflow_executions
       WHERE workflow_id = $1 AND status = 'running'
       ORDER BY started_at DESC LIMIT 1`,
      [workflowId]
    );
    if (!execRow.rows.length) throw new Error('No running execution found');
    const executionId = execRow.rows[0].id;

    await updateNodeExecution(executionId, nodeId, { status: 'completed' });
    return { approved: true, executionId };
  }

  /**
   * Reject a human-in-loop node — stops execution.
   */
  static async rejectNode(workflowId, nodeId) {
    const execRow = await query(
      `SELECT id FROM workflow_executions
       WHERE workflow_id = $1 AND status = 'running'
       ORDER BY started_at DESC LIMIT 1`,
      [workflowId]
    );
    if (!execRow.rows.length) throw new Error('No running execution found');
    const executionId = execRow.rows[0].id;

    await updateNodeExecution(executionId, nodeId, { status: 'rejected' });
    return { rejected: true, executionId };
  }
}

export default ExecutionModel;

```


### `models/workflow.model.js`

```js
/**
 * Workflow Model
 *
 * Handles all database operations for workflows, nodes, and edges.
 */

import { query, getClient } from '../db/connection.js';

export class WorkflowModel {
  /**
   * Create a new workflow with nodes and edges
   * @param {Object} workflowData - Workflow data
   * @returns {Promise<Object>} Created workflow
   */
  static async createWorkflow({ name, description, status, nodes, edges, createdBy, metadata }) {
    const client = await getClient();

    try {
      await client.query('BEGIN');

      // Insert workflow
      const workflowResult = await client.query(
        `INSERT INTO workflows (name, description, status, created_by, metadata)
         VALUES ($1, $2, $3, $4, $5)
         RETURNING *`,
        [name, description || null, status || 'draft', createdBy || null, JSON.stringify(metadata || {})]
      );

      const workflow = workflowResult.rows[0];

      // Insert nodes
      if (nodes && nodes.length > 0) {
        const nodeValues = nodes.map((node, index) => {
          const params = [
            workflow.id,
            node.id,
            node.type,
            node.label,
            node.category,
            node.color,
            node.x,
            node.y,
            JSON.stringify(node.config || {})
          ];
          const placeholders = params.map((_, i) => `$${index * 9 + i + 1}`).join(', ');
          return { params, placeholders };
        });

        const nodeInsertQuery = `
          INSERT INTO workflow_nodes
          (workflow_id, node_id, node_type, label, category, color, position_x, position_y, config)
          VALUES ${nodeValues.map(v => `(${v.placeholders})`).join(', ')}
        `;

        const allNodeParams = nodeValues.flatMap(v => v.params);
        await client.query(nodeInsertQuery, allNodeParams);
      }

      // Insert edges
      if (edges && edges.length > 0) {
        const edgeValues = edges.map((edge, index) => {
          const params = [
            workflow.id,
            edge.id,
            edge.fromId,
            edge.toId,
            edge.relationship,
            JSON.stringify(edge.config || {})
          ];
          const placeholders = params.map((_, i) => `$${index * 6 + i + 1}`).join(', ');
          return { params, placeholders };
        });

        const edgeInsertQuery = `
          INSERT INTO workflow_edges
          (workflow_id, edge_id, from_node_id, to_node_id, relationship, config)
          VALUES ${edgeValues.map(v => `(${v.placeholders})`).join(', ')}
        `;

        const allEdgeParams = edgeValues.flatMap(v => v.params);
        await client.query(edgeInsertQuery, allEdgeParams);
      }

      await client.query('COMMIT');

      // Return complete workflow with nodes and edges
      return await this.getWorkflowById(workflow.id);
    } catch (error) {
      await client.query('ROLLBACK');
      console.error('Error creating workflow:', error);
      throw error;
    } finally {
      client.release();
    }
  }

  /**
   * Get workflow by ID with nodes and edges
   * @param {string} workflowId - Workflow UUID
   * @returns {Promise<Object>} Workflow with nodes and edges
   */
  static async getWorkflowById(workflowId) {
    const workflowResult = await query(
      'SELECT * FROM workflows WHERE id = $1',
      [workflowId]
    );

    if (workflowResult.rows.length === 0) {
      return null;
    }

    const workflow = workflowResult.rows[0];

    // Get nodes
    const nodesResult = await query(
      `SELECT node_id as id, node_type as type, label, category, color,
              position_x as x, position_y as y, config
       FROM workflow_nodes
       WHERE workflow_id = $1
       ORDER BY created_at`,
      [workflowId]
    );

    // Get edges
    const edgesResult = await query(
      `SELECT edge_id as id, from_node_id as "fromId", to_node_id as "toId",
              relationship, config
       FROM workflow_edges
       WHERE workflow_id = $1
       ORDER BY created_at`,
      [workflowId]
    );

    return {
      ...workflow,
      nodes: nodesResult.rows,
      edges: edgesResult.rows,
    };
  }

  /**
   * Get all workflows (summary view)
   * @param {Object} filters - Filter options
   * @returns {Promise<Array>} List of workflows
   */
  static async getAllWorkflows({ status, limit = 50, offset = 0 } = {}) {
    let queryText = `
      SELECT w.*,
             COUNT(DISTINCT wn.id) as node_count,
             COUNT(DISTINCT we.id) as edge_count
      FROM workflows w
      LEFT JOIN workflow_nodes wn ON w.id = wn.workflow_id
      LEFT JOIN workflow_edges we ON w.id = we.workflow_id
    `;

    const params = [];
    if (status) {
      queryText += ' WHERE w.status = $1';
      params.push(status);
    }

    queryText += ' GROUP BY w.id ORDER BY w.created_at DESC LIMIT $' + (params.length + 1) + ' OFFSET $' + (params.length + 2);
    params.push(limit, offset);

    const result = await query(queryText, params);
    return result.rows;
  }

  /**
   * Update workflow
   * @param {string} workflowId - Workflow UUID
   * @param {Object} updates - Fields to update
   * @returns {Promise<Object>} Updated workflow
   */
  static async updateWorkflow(workflowId, { name, description, status, metadata }) {
    const updates = [];
    const params = [];
    let paramIndex = 1;

    if (name !== undefined) {
      updates.push(`name = $${paramIndex++}`);
      params.push(name);
    }
    if (description !== undefined) {
      updates.push(`description = $${paramIndex++}`);
      params.push(description);
    }
    if (status !== undefined) {
      updates.push(`status = $${paramIndex++}`);
      params.push(status);
    }
    if (metadata !== undefined) {
      updates.push(`metadata = $${paramIndex++}`);
      params.push(JSON.stringify(metadata));
    }

    if (updates.length === 0) {
      throw new Error('No fields to update');
    }

    params.push(workflowId);

    const result = await query(
      `UPDATE workflows SET ${updates.join(', ')} WHERE id = $${paramIndex} RETURNING *`,
      params
    );

    return result.rows[0];
  }

  /**
   * Delete workflow (cascades to nodes and edges)
   * @param {string} workflowId - Workflow UUID
   * @returns {Promise<boolean>} Success status
   */
  static async deleteWorkflow(workflowId) {
    const result = await query(
      'DELETE FROM workflows WHERE id = $1 RETURNING id',
      [workflowId]
    );

    return result.rowCount > 0;
  }

  /**
   * Update workflow nodes and edges
   * @param {string} workflowId - Workflow UUID
   * @param {Object} data - Nodes and edges data
   * @returns {Promise<Object>} Updated workflow
   */
  static async updateWorkflowContent(workflowId, { nodes, edges }) {
    const client = await getClient();

    try {
      await client.query('BEGIN');

      // Delete existing nodes and edges (cascade will handle edges)
      await client.query('DELETE FROM workflow_nodes WHERE workflow_id = $1', [workflowId]);

      // Insert new nodes
      if (nodes && nodes.length > 0) {
        const nodeValues = nodes.map((node, index) => {
          const params = [
            workflowId,
            node.id,
            node.type,
            node.label,
            node.category,
            node.color,
            node.x,
            node.y,
            JSON.stringify(node.config || {})
          ];
          const placeholders = params.map((_, i) => `$${index * 9 + i + 1}`).join(', ');
          return { params, placeholders };
        });

        const nodeInsertQuery = `
          INSERT INTO workflow_nodes
          (workflow_id, node_id, node_type, label, category, color, position_x, position_y, config)
          VALUES ${nodeValues.map(v => `(${v.placeholders})`).join(', ')}
        `;

        const allNodeParams = nodeValues.flatMap(v => v.params);
        await client.query(nodeInsertQuery, allNodeParams);
      }

      // Insert new edges
      if (edges && edges.length > 0) {
        const edgeValues = edges.map((edge, index) => {
          const params = [
            workflowId,
            edge.id,
            edge.fromId,
            edge.toId,
            edge.relationship,
            JSON.stringify(edge.config || {})
          ];
          const placeholders = params.map((_, i) => `$${index * 6 + i + 1}`).join(', ');
          return { params, placeholders };
        });

        const edgeInsertQuery = `
          INSERT INTO workflow_edges
          (workflow_id, edge_id, from_node_id, to_node_id, relationship, config)
          VALUES ${edgeValues.map(v => `(${v.placeholders})`).join(', ')}
        `;

        const allEdgeParams = edgeValues.flatMap(v => v.params);
        await client.query(edgeInsertQuery, allEdgeParams);
      }

      await client.query('COMMIT');

      return await this.getWorkflowById(workflowId);
    } catch (error) {
      await client.query('ROLLBACK');
      console.error('Error updating workflow content:', error);
      throw error;
    } finally {
      client.release();
    }
  }
}

export default WorkflowModel;

```


### `routes/execution.routes.js`

```js
/**
 * Execution API Routes
 *
 * POST   /api/workflows/:id/execute           — start execution
 * GET    /api/workflows/:id/execution         — get current execution state
 * POST   /api/workflows/:id/execution/approve/:nodeId  — approve human-in-loop
 * POST   /api/workflows/:id/execution/reject/:nodeId   — reject human-in-loop
 */

import express from 'express';
import { ExecutionModel } from '../models/execution.model.js';

const router = express.Router({ mergeParams: true });

/**
 * POST /api/workflows/:id/execute
 * Start execution of a saved workflow
 */
router.post('/execute', async (req, res) => {
  try {
    const { id } = req.params;
    const execution = await ExecutionModel.startExecution(id);
    res.status(201).json({
      success: true,
      message: 'Workflow execution started',
      data: execution,
    });
  } catch (error) {
    console.error('Start execution error:', error);
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to start execution',
    });
  }
});

/**
 * GET /api/workflows/:id/execution
 * Get current execution state (all node statuses)
 */
router.get('/execution', async (req, res) => {
  try {
    const { id } = req.params;
    const state = await ExecutionModel.getExecutionState(id);
    if (!state) {
      return res.status(404).json({ success: false, error: 'No execution found for this workflow' });
    }
    res.json({ success: true, data: state });
  } catch (error) {
    console.error('Get execution state error:', error);
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to fetch execution state',
    });
  }
});

/**
 * POST /api/workflows/:id/execution/approve/:nodeId
 * Approve a human-in-loop node and resume execution
 */
router.post('/execution/approve/:nodeId', async (req, res) => {
  try {
    const { id, nodeId } = req.params;
    const result = await ExecutionModel.approveNode(id, nodeId);
    res.json({ success: true, message: 'Node approved, execution resuming', data: result });
  } catch (error) {
    console.error('Approve node error:', error);
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to approve node',
    });
  }
});

/**
 * POST /api/workflows/:id/execution/reject/:nodeId
 * Reject a human-in-loop node and stop execution
 */
router.post('/execution/reject/:nodeId', async (req, res) => {
  try {
    const { id, nodeId } = req.params;
    const result = await ExecutionModel.rejectNode(id, nodeId);
    res.json({ success: true, message: 'Node rejected, execution halted', data: result });
  } catch (error) {
    console.error('Reject node error:', error);
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to reject node',
    });
  }
});

export default router;

```


### `routes/repository.routes.js`

```js
/**
 * Repository Routes
 *
 * Handles API routes for connected GitHub repositories
 */

import express from 'express';
import { Repository } from '../models/Repository.js';

const router = express.Router();

/**
 * GET /api/repositories
 * Get all connected repositories
 */
router.get('/', async (req, res) => {
  try {
    console.log('Fetching all connected repositories');
    const repositories = await Repository.findAll();

    console.log(`Found ${repositories.length} repositories`);
    res.json({
      success: true,
      data: repositories
    });
  } catch (error) {
    console.error('Error fetching repositories:', error);
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to fetch repositories'
    });
  }
});

/**
 * GET /api/repositories/:id
 * Get a single repository by ID
 */
router.get('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    console.log(`Fetching repository: ${id}`);

    const repository = await Repository.findById(id);

    if (!repository) {
      return res.status(404).json({
        success: false,
        error: 'Repository not found'
      });
    }

    res.json({
      success: true,
      data: repository
    });
  } catch (error) {
    console.error('Error fetching repository:', error);
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to fetch repository'
    });
  }
});

/**
 * POST /api/repositories
 * Connect a new repository
 */
router.post('/', async (req, res) => {
  try {
    const { name, owner, fullName, language, stars, branches, description, url, status } = req.body;

    // Validate required fields
    if (!name || !owner || !fullName || !url) {
      return res.status(400).json({
        success: false,
        error: 'Missing required fields: name, owner, fullName, url'
      });
    }

    console.log(`Connecting repository: ${fullName}`);

    // Check if repository already exists
    const existingRepo = await Repository.findByFullName(fullName);
    if (existingRepo) {
      return res.status(409).json({
        success: false,
        error: `Repository "${fullName}" is already connected`
      });
    }

    // Create repository
    const repositoryData = {
      name,
      owner,
      full_name: fullName,
      language: language || 'Unknown',
      stars: stars || 0,
      branches: branches || 0,
      description: description || null,
      url,
      status: status || 'active',
      connected_at: new Date().toISOString()
    };

    const repository = await Repository.create(repositoryData);

    console.log(`Repository connected successfully: ${repository.id}`);
    res.status(201).json({
      success: true,
      data: repository,
      message: 'Repository connected successfully'
    });
  } catch (error) {
    console.error('Error connecting repository:', error);
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to connect repository'
    });
  }
});

/**
 * PUT /api/repositories/:id
 * Update a repository
 */
router.put('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const updates = req.body;

    console.log(`Updating repository: ${id}`);

    // Check if repository exists
    const existingRepo = await Repository.findById(id);
    if (!existingRepo) {
      return res.status(404).json({
        success: false,
        error: 'Repository not found'
      });
    }

    // Map camelCase to snake_case for database
    const dbUpdates = {};
    if (updates.name !== undefined) dbUpdates.name = updates.name;
    if (updates.owner !== undefined) dbUpdates.owner = updates.owner;
    if (updates.fullName !== undefined) dbUpdates.full_name = updates.fullName;
    if (updates.language !== undefined) dbUpdates.language = updates.language;
    if (updates.stars !== undefined) dbUpdates.stars = updates.stars;
    if (updates.branches !== undefined) dbUpdates.branches = updates.branches;
    if (updates.description !== undefined) dbUpdates.description = updates.description;
    if (updates.url !== undefined) dbUpdates.url = updates.url;
    if (updates.status !== undefined) dbUpdates.status = updates.status;

    const repository = await Repository.update(id, dbUpdates);

    console.log(`Repository updated successfully: ${id}`);
    res.json({
      success: true,
      data: repository,
      message: 'Repository updated successfully'
    });
  } catch (error) {
    console.error('Error updating repository:', error);
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to update repository'
    });
  }
});

/**
 * DELETE /api/repositories/:id
 * Disconnect a repository
 */
router.delete('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    console.log(`Disconnecting repository: ${id}`);

    // Check if repository exists
    const existingRepo = await Repository.findById(id);
    if (!existingRepo) {
      return res.status(404).json({
        success: false,
        error: 'Repository not found'
      });
    }

    await Repository.delete(id);

    console.log(`Repository disconnected successfully: ${id}`);
    res.json({
      success: true,
      message: 'Repository disconnected successfully'
    });
  } catch (error) {
    console.error('Error disconnecting repository:', error);
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to disconnect repository'
    });
  }
});

export default router;

```


### `routes/workflow.routes.js`

```js
/**
 * Workflow API Routes
 */

import express from 'express';
import { WorkflowModel } from '../models/workflow.model.js';

const router = express.Router();

/**
 * POST /api/workflows
 * Create a new workflow
 */
router.post('/', async (req, res) => {
  try {
    const { name, description, status, nodes, edges, createdBy, metadata } = req.body;

    // Validation
    if (!name) {
      return res.status(400).json({ error: 'Workflow name is required' });
    }

    if (!nodes || !Array.isArray(nodes)) {
      return res.status(400).json({ error: 'Nodes array is required' });
    }

    const workflow = await WorkflowModel.createWorkflow({
      name,
      description,
      status,
      nodes,
      edges: edges || [],
      createdBy,
      metadata,
    });

    res.status(201).json({
      success: true,
      message: 'Workflow created successfully',
      data: workflow,
    });
  } catch (error) {
    console.error('Create workflow error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to create workflow',
      message: error.message,
    });
  }
});

/**
 * GET /api/workflows
 * Get all workflows
 */
router.get('/', async (req, res) => {
  try {
    const { status, limit, offset } = req.query;

    const workflows = await WorkflowModel.getAllWorkflows({
      status,
      limit: limit ? parseInt(limit) : undefined,
      offset: offset ? parseInt(offset) : undefined,
    });

    res.json({
      success: true,
      data: workflows,
      count: workflows.length,
    });
  } catch (error) {
    console.error('Get workflows error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch workflows',
      message: error.message,
    });
  }
});

/**
 * GET /api/workflows/:id
 * Get workflow by ID with full details
 */
router.get('/:id', async (req, res) => {
  try {
    const { id } = req.params;

    const workflow = await WorkflowModel.getWorkflowById(id);

    if (!workflow) {
      return res.status(404).json({
        success: false,
        error: 'Workflow not found',
      });
    }

    res.json({
      success: true,
      data: workflow,
    });
  } catch (error) {
    console.error('Get workflow error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch workflow',
      message: error.message,
    });
  }
});

/**
 * PUT /api/workflows/:id
 * Update workflow metadata
 */
router.put('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const { name, description, status, metadata } = req.body;

    const workflow = await WorkflowModel.updateWorkflow(id, {
      name,
      description,
      status,
      metadata,
    });

    if (!workflow) {
      return res.status(404).json({
        success: false,
        error: 'Workflow not found',
      });
    }

    res.json({
      success: true,
      message: 'Workflow updated successfully',
      data: workflow,
    });
  } catch (error) {
    console.error('Update workflow error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to update workflow',
      message: error.message,
    });
  }
});

/**
 * PUT /api/workflows/:id/content
 * Update workflow nodes and edges
 */
router.put('/:id/content', async (req, res) => {
  try {
    const { id } = req.params;
    const { nodes, edges } = req.body;

    if (!nodes || !Array.isArray(nodes)) {
      return res.status(400).json({ error: 'Nodes array is required' });
    }

    const workflow = await WorkflowModel.updateWorkflowContent(id, {
      nodes,
      edges: edges || [],
    });

    res.json({
      success: true,
      message: 'Workflow content updated successfully',
      data: workflow,
    });
  } catch (error) {
    console.error('Update workflow content error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to update workflow content',
      message: error.message,
    });
  }
});

/**
 * DELETE /api/workflows/:id
 * Delete workflow
 */
router.delete('/:id', async (req, res) => {
  try {
    const { id } = req.params;

    const deleted = await WorkflowModel.deleteWorkflow(id);

    if (!deleted) {
      return res.status(404).json({
        success: false,
        error: 'Workflow not found',
      });
    }

    res.json({
      success: true,
      message: 'Workflow deleted successfully',
    });
  } catch (error) {
    console.error('Delete workflow error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to delete workflow',
      message: error.message,
    });
  }
});

export default router;

```


_[End of repository]_
