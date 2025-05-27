# TaskMaster Cloud MCP Deployment Guide

## Prerequisites

1. Cloudflare account
2. Wrangler CLI authenticated
3. Environment variables configured

## Local Development

```bash
# Start local development server
npm run dev

# This will start the worker on http://localhost:8787
```

## Deployment Steps

### 1. Configure Secrets

```bash
# Set Xano credentials
wrangler secret put XANO_INSTANCE_ID
wrangler secret put XANO_WORKSPACE_ID  
wrangler secret put XANO_API_KEY

# Set OAuth credentials (when implemented)
wrangler secret put OAUTH_CLIENT_ID
wrangler secret put OAUTH_CLIENT_SECRET
```

### 2. Deploy to Cloudflare

```bash
# Deploy to production
npm run deploy

# Monitor logs
npm run tail
```

## Endpoints

Once deployed, your worker will be available at:
`https://taskmaster-cloud-mcp.<your-subdomain>.workers.dev`

### Available Routes

- `GET /` - Home page with status
- `GET /health` - Health check endpoint
- `POST /oauth/authorize` - OAuth authorization (pending)
- `POST /oauth/token` - OAuth token exchange (pending)
- `POST /api/v1/projects` - Project operations
- `POST /api/v1/tasks` - Task operations

## Testing the Deployment

```bash
# Health check
curl https://taskmaster-cloud-mcp.<your-subdomain>.workers.dev/health

# Should return:
{
  "status": "ok",
  "service": "taskmaster-cloud-mcp",
  "timestamp": "2025-05-27T22:00:00.000Z",
  "xano": "configured",
  "version": "1.0.0"
}
```

## Environment Variables

Required for production:
- `XANO_INSTANCE_ID` - Your Xano instance (xnwv-v1z6-dvnr)
- `XANO_WORKSPACE_ID` - Workspace ID (5 for Snappy)
- `XANO_API_KEY` - API key for Xano access

## Troubleshooting

### Common Issues

1. **Authentication Error**
   - Ensure wrangler is logged in: `wrangler login`
   - Check account permissions

2. **Deployment Fails**
   - Verify wrangler.toml syntax
   - Check worker.js for syntax errors
   - Ensure all dependencies are installed

3. **Runtime Errors**
   - Use `npm run tail` to see real-time logs
   - Check environment variables are set
   - Verify CORS settings if MCP client can't connect

## Next Steps

After deployment:
1. Set up custom domain (optional)
2. Configure rate limiting
3. Enable analytics
4. Set up monitoring alerts