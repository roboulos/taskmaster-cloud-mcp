# TaskMaster Cloud Architecture

## System Overview

TaskMaster Cloud transforms the local file-based TaskMaster into a cloud-native solution using:
- **Xano** for database and API layer
- **Cloudflare Workers** for edge computing
- **OAuth** for secure authentication
- **MCP Protocol** for AI tool integration

## Data Flow

```
Claude Desktop / Terminal
        ↓
   MCP Protocol
        ↓
Cloudflare Worker (OAuth)
        ↓
  Xano REST APIs
        ↓
   PostgreSQL DB
```

## Key Design Decisions

### 1. Same Database, Same Auth
- Leverages existing Snappy infrastructure
- No duplicate user management
- Consistent API key authentication
- Reduces complexity and maintenance

### 2. Project Key Strategy
- URL-safe identifiers (e.g., "client-clearleads")
- Maps to existing project structure
- Enables clean REST URLs
- Supports multi-tenancy

### 3. Task ID Preservation
- Maintains existing numbering (15, 15.2)
- Supports hierarchical subtasks
- Compatible with local TaskMaster
- Enables smooth migration

### 4. Stateless API Design
- Each request contains full context
- No server-side session state
- Enables horizontal scaling
- Simplifies caching

## API Design Patterns

### Authentication Flow
```javascript
// Every request includes API key
{
  "api_key": "user_api_key_here",
  "project_key": "client-clearleads",
  // ... other parameters
}

// Server validates against users table
db.get '👤 users' {
  field_name = "api_key"
  field_value = $input.api_key
}
```

### Error Handling
- Consistent error format
- Descriptive error messages
- HTTP status codes aligned with REST standards
- Detailed logging for debugging

### Response Format
```javascript
{
  "success": true,
  "data": { /* actual response data */ },
  "message": "Human-readable message",
  "metadata": {
    "timestamp": "2025-05-27T21:00:00Z",
    "version": "1.0.0"
  }
}
```

## Performance Considerations

### Caching Strategy (Future)
- 5-minute cache for read operations
- Immediate cache invalidation on writes
- Project-level cache keys
- User-specific cache partitions

### Database Optimization
- Indexes on project_key and task_id
- Composite index on (project_key, status)
- JSON fields for flexible metadata
- Timestamp indexes for sorting

### API Rate Limiting (Future)
- Per-user rate limits
- Burst allowance for bulk operations
- Graceful degradation
- Clear rate limit headers

## Security Model

### Authentication
- API keys stored securely in users table
- No keys in URL parameters
- HTTPS required for all connections
- Key rotation support planned

### Authorization
- Project-level access control
- User can only access their projects
- Admin override capabilities
- Audit logging for all operations

### Data Protection
- Input validation on all fields
- SQL injection prevention via Xano
- XSS protection for future web UI
- Encrypted data at rest

## Scalability Path

### Phase 1: Current
- Single Xano instance
- Basic CRUD operations
- Manual deployment

### Phase 2: Enhanced
- Read replicas for queries
- Background job processing
- Automated deployments
- Monitoring and alerting

### Phase 3: Enterprise
- Multi-region deployment
- Real-time synchronization
- Advanced analytics
- Custom integrations

## Integration Points

### MCP Protocol
- Standard tool definitions
- Consistent parameter naming
- Error propagation
- Progress reporting

### Webhook Support (Future)
- Task completion notifications
- Status change alerts
- Custom webhook endpoints
- Retry logic for failures

### External Systems (Future)
- Slack notifications
- GitHub issue sync
- JIRA integration
- Custom CRM updates