# TaskMaster Cloud Standards

## Repository Standards

### Directory Structure
```
taskmaster-cloud-mcp/
├── README.md                 # Project overview and quick start
├── docs/                     # Detailed documentation
│   ├── ARCHITECTURE.md      # System design and decisions
│   ├── IMPLEMENTATION_STATUS.md  # Current progress
│   ├── CLEARLEADS_INTEGRATION.md # Client-specific docs
│   └── STANDARDS.md         # This file
├── src/                     # TypeScript source code
│   ├── index.ts            # Main entry point
│   ├── tools/              # MCP tool definitions
│   ├── api/                # Xano API integrations
│   └── utils/              # Shared utilities
├── tests/                   # Test files
├── scripts/                 # Utility scripts
└── .env.example            # Environment template
```

### Documentation Requirements

Every significant change must update:
1. **README.md** - If it affects setup or usage
2. **IMPLEMENTATION_STATUS.md** - Progress tracking
3. **Code comments** - Inline documentation
4. **Commit messages** - Clear, descriptive

### Commit Standards

Format: `type: description`

Types:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation only
- `refactor:` Code restructuring
- `test:` Test additions/changes
- `chore:` Maintenance tasks

Example:
```
feat: Add bulk task update endpoint
docs: Update API documentation for bulk operations
fix: Correct task dependency validation
```

## Code Standards

### TypeScript/JavaScript
```typescript
// Use clear, descriptive names
async function updateTaskStatus(
  projectKey: string,
  taskId: string,
  newStatus: TaskStatus
): Promise<Task> {
  // Implementation
}

// Document complex logic
/**
 * Validates task dependencies to prevent circular references
 * @param taskId - The task being updated
 * @param dependencies - Array of task IDs this depends on
 * @returns true if valid, throws error if circular
 */
function validateDependencies(
  taskId: string,
  dependencies: string[]
): boolean {
  // Implementation
}
```

### API Design

#### Endpoint Naming
- Use nouns for resources: `/tasks`, `/projects`
- Use verbs for actions: `/tasks/validate`, `/tasks/bulk-update`
- Keep URLs lowercase with hyphens

#### Request/Response Format
```javascript
// Request
{
  "api_key": "required_for_auth",
  "project_key": "client-clearleads",
  "data": {
    // Actual request data
  }
}

// Success Response
{
  "success": true,
  "data": { /* results */ },
  "message": "Human-readable message",
  "metadata": {
    "timestamp": "2025-05-27T21:00:00Z",
    "count": 42
  }
}

// Error Response
{
  "success": false,
  "error": {
    "code": "TASK_NOT_FOUND",
    "message": "Task with ID '15.2' not found",
    "details": { /* additional context */ }
  }
}
```

### Database Standards

#### Table Naming
- Use emoji prefixes for visual organization
- Plural names for collections: `tasks`, `projects`
- Descriptive names: `taskmaster_tasks` not just `tasks`

#### Field Naming
- snake_case for all fields
- Consistent naming across tables
- Foreign keys: `<table>_id` (e.g., `project_id`)
- Timestamps: `created_at`, `updated_at`

#### Data Types
- IDs: Auto-increment integers
- Keys: Text fields (e.g., `project_key`)
- JSON: Stored as text, parsed in application
- Status/Type fields: Text with defined values

## Testing Standards

### Test Organization
```
tests/
├── unit/           # Individual function tests
├── integration/    # API endpoint tests
├── e2e/           # Full workflow tests
└── fixtures/      # Test data
```

### Test Naming
```typescript
describe('TaskManager', () => {
  describe('updateTaskStatus', () => {
    it('should update status for valid task', async () => {
      // Test implementation
    });
    
    it('should throw error for invalid status', async () => {
      // Test implementation
    });
  });
});
```

## MCP Tool Standards

### Tool Definition
```typescript
{
  name: "taskmaster_cloud_get_tasks",
  description: "Retrieve tasks for a project with optional filtering",
  inputSchema: {
    type: "object",
    properties: {
      project_key: {
        type: "string",
        description: "Project identifier (e.g., client-clearleads)"
      },
      status: {
        type: "string",
        enum: ["pending", "in_progress", "done", "cancelled"],
        description: "Filter by task status"
      }
    },
    required: ["project_key"]
  }
}
```

### Error Handling
- Always return structured errors
- Include actionable error messages
- Log errors for debugging
- Gracefully degrade functionality

## Security Standards

### Authentication
- API keys in headers, not URLs
- Validate all inputs
- Use HTTPS everywhere
- Implement rate limiting

### Data Protection
- No sensitive data in logs
- Encrypt data at rest
- Validate user permissions
- Audit all modifications

## Performance Standards

### API Response Times
- GET requests: < 200ms
- POST/PUT requests: < 500ms
- Bulk operations: < 2000ms
- Timeout after 30 seconds

### Optimization Guidelines
- Index frequently queried fields
- Implement pagination for lists
- Cache read-heavy operations
- Batch database operations

## Deployment Standards

### Environment Variables
Required:
- `XANO_INSTANCE_ID`
- `XANO_WORKSPACE_ID`
- `XANO_API_KEY`
- `CLOUDFLARE_ACCOUNT_ID`
- `CLOUDFLARE_API_TOKEN`

### Version Control
- Tag releases with semantic versioning
- Maintain CHANGELOG.md
- Document breaking changes
- Provide migration guides

### Monitoring
- Log all API requests
- Track error rates
- Monitor response times
- Alert on anomalies