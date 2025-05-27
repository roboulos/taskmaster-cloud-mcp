# TaskMaster Cloud MCP

A cloud-based task management system built on Xano, extending the TaskMaster MCP to provide persistent, real-time task tracking across projects.

## 🎯 Project Vision

Transform the local TaskMaster MCP into a cloud-hosted solution that:
- Provides real-time task visibility across team members
- Persists tasks across workspace clones and environments
- Integrates with existing Snappy MCP authentication
- Enables future frontend dashboards and analytics

## 🏗️ Architecture

### Database Structure (Xano Workspace ID: 5 - Snappy)

```
📋 taskmaster_projects (Table ID: 257)
├── id (auto)
├── project_key (text) - URL-safe identifier (e.g., "client-clearleads")
├── name (text) - Human-readable project name
├── description (text) - Project goals and context
├── settings (text/JSON) - Project-specific configuration
├── created_at (timestamp)
└── updated_at (timestamp)

📝 taskmaster_tasks (Table ID: 258)
├── id (auto)
├── project_key (text) - Foreign key to projects
├── task_id (text) - Task identifier (e.g., "15" or "15.2")
├── parent_id (text, nullable) - For subtask hierarchy
├── title (text) - Task title
├── description (text) - Task description
├── details (text) - Implementation notes
├── status (text) - pending|in_progress|done|cancelled
├── priority (text) - high|medium|low
├── dependencies (text/JSON) - Array of dependent task IDs
├── metadata (text/JSON) - Flexible additional data
├── created_at (timestamp)
└── updated_at (timestamp)

📊 taskmaster_sessions (Table ID: 259)
├── id (auto)
├── project_key (text) - Associated project
├── user_id (int) - From users table
├── session_id (text) - Unique session identifier
├── last_command (text) - Last executed command
├── created_at (timestamp)
└── updated_at (timestamp)
```

### API Endpoints (Group ID: 99 - 📋 TaskMaster Cloud)

1. **get_tasks** (POST)
   - Input: api_key, project_key, status (optional)
   - Returns: List of tasks for the project

2. **create_task** (POST)
   - Input: api_key, project_key, task_id, title, description, priority
   - Returns: Success confirmation

3. **update_task_status** (POST)
   - Input: api_key, project_key, task_id, status
   - Returns: Success confirmation

## 🔌 Integration with Existing Systems

### Authentication
- Uses existing `👤 users` table from Snappy workspace
- API key authentication consistent with other MCP tools
- No separate auth system required

### Project Identification
- URL-safe project keys: "client-clearleads", "ai-productivity", "client-pvm"
- Maps to existing TaskMaster project structure
- Maintains compatibility with local TaskMaster files

## 🚀 Implementation Plan

### Phase 1: MCP Tool Transformation (Current)
1. ✅ Create Xano tables and API structure
2. 🔄 Clone xano-mcp-server repository
3. ⏳ Update tool definitions to use cloud APIs
4. ⏳ Deploy to Cloudflare Worker

### Phase 2: Feature Parity
- Implement all TaskMaster commands via cloud APIs
- Add caching layer for performance
- Create migration scripts for existing projects

### Phase 3: Enhanced Features
- Real-time updates via webhooks
- Task analytics and reporting
- Frontend dashboard for Jim and other clients
- Slack/Discord integration

## 🔧 Development Setup

```bash
# Clone the repository
git clone [repository-url] taskmaster-cloud-mcp
cd taskmaster-cloud-mcp

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with your Xano credentials

# Build the project
npm run build

# Deploy to Cloudflare
npm run deploy
```

## 📋 MCP Configuration

Add to your Claude Desktop config:

```json
{
  "taskmaster-cloud": {
    "command": "node",
    "args": ["/path/to/taskmaster-cloud-mcp/dist/index.js"],
    "env": {
      "TASKMASTER_URL": "https://taskmaster.yourdomain.com",
      "XANO_INSTANCE": "xnwv-v1z6-dvnr",
      "XANO_WORKSPACE": "5"
    }
  }
}
```

## 🔗 Related Projects

- **Xano MCP Server**: The foundation this project extends
- **Claude Task Master**: Original local TaskMaster implementation
- **ClearLeads Project**: Primary use case driving cloud requirements

## 📈 Benefits for ClearLeads Project

1. **Real-time Progress**: Jim can see task updates as they happen
2. **Persistence**: Tasks survive workspace clones and migrations
3. **Collaboration**: Multiple team members can update tasks
4. **Audit Trail**: Complete history of task changes
5. **Integration Ready**: Can trigger webhooks on task completion

## 🛣️ Roadmap

- [ ] Complete API implementation with full CRUD operations
- [ ] Add task filtering and search capabilities
- [ ] Implement dependency validation
- [ ] Create bulk operations endpoints
- [ ] Add task templates and recurring tasks
- [ ] Build notification system for task updates
- [ ] Create analytics endpoints for project velocity

## 🤝 Contributing

This project is part of the broader MCP ecosystem. Contributions should:
- Maintain compatibility with existing TaskMaster commands
- Use consistent authentication patterns
- Follow Xano best practices for API design
- Include comprehensive error handling

## 📝 License

[License details to be added]