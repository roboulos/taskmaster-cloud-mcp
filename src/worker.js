/**
 * TaskMaster Cloud MCP Worker
 * Provides cloud-based task management via MCP protocol
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // CORS headers for all responses
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      'Access-Control-Max-Age': '86400',
    };

    // Handle preflight requests
    if (request.method === 'OPTIONS') {
      return new Response(null, { 
        status: 204,
        headers: corsHeaders 
      });
    }

    try {
      // Route handling
      switch (url.pathname) {
        case '/':
          return handleHome(corsHeaders);
        
        case '/health':
          return handleHealth(env, corsHeaders);
        
        case '/oauth/authorize':
          return handleOAuthAuthorize(request, env, corsHeaders);
        
        case '/oauth/token':
          return handleOAuthToken(request, env, corsHeaders);
        
        case '/api/v1/projects':
          return handleProjects(request, env, corsHeaders);
        
        case '/api/v1/tasks':
          return handleTasks(request, env, corsHeaders);
        
        default:
          if (url.pathname.startsWith('/api/v1/')) {
            return handleAPIRoute(request, env, url, corsHeaders);
          }
          return new Response('Not Found', { 
            status: 404,
            headers: corsHeaders 
          });
      }
    } catch (error) {
      console.error('Worker error:', error);
      return new Response(JSON.stringify({
        error: 'Internal Server Error',
        message: error.message
      }), { 
        status: 500,
        headers: {
          ...corsHeaders,
          'Content-Type': 'application/json'
        }
      });
    }
  }
};

// Handler functions
function handleHome(corsHeaders) {
  const html = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>TaskMaster Cloud MCP</title>
      <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .status { color: green; }
        code { background: #f4f4f4; padding: 2px 4px; }
      </style>
    </head>
    <body>
      <h1>📋 TaskMaster Cloud MCP</h1>
      <p class="status">✅ Worker is running</p>
      <p>This is the CloudFlare Worker endpoint for TaskMaster Cloud MCP.</p>
      <h2>Available Endpoints:</h2>
      <ul>
        <li><code>GET /health</code> - Health check</li>
        <li><code>POST /oauth/authorize</code> - OAuth authorization</li>
        <li><code>POST /oauth/token</code> - OAuth token exchange</li>
        <li><code>POST /api/v1/projects</code> - Project operations</li>
        <li><code>POST /api/v1/tasks</code> - Task operations</li>
      </ul>
      <p>Configure your MCP client to use this endpoint.</p>
    </body>
    </html>
  `;
  
  return new Response(html, {
    headers: {
      ...corsHeaders,
      'Content-Type': 'text/html'
    }
  });
}

async function handleHealth(env, corsHeaders) {
  // Check if we can reach Xano
  let xanoStatus = 'unknown';
  
  try {
    if (env.XANO_INSTANCE_ID && env.XANO_API_KEY) {
      // Would make actual health check to Xano here
      xanoStatus = 'configured';
    } else {
      xanoStatus = 'not configured';
    }
  } catch (error) {
    xanoStatus = 'error';
  }
  
  return new Response(JSON.stringify({
    status: 'ok',
    service: 'taskmaster-cloud-mcp',
    timestamp: new Date().toISOString(),
    xano: xanoStatus,
    version: '1.0.0'
  }), {
    headers: {
      ...corsHeaders,
      'Content-Type': 'application/json'
    }
  });
}

async function handleOAuthAuthorize(request, env, corsHeaders) {
  // OAuth authorization endpoint
  // This would handle the OAuth flow for MCP clients
  return new Response(JSON.stringify({
    message: 'OAuth authorization endpoint',
    note: 'Implementation pending'
  }), {
    headers: {
      ...corsHeaders,
      'Content-Type': 'application/json'
    }
  });
}

async function handleOAuthToken(request, env, corsHeaders) {
  // OAuth token exchange endpoint
  return new Response(JSON.stringify({
    message: 'OAuth token endpoint',
    note: 'Implementation pending'
  }), {
    headers: {
      ...corsHeaders,
      'Content-Type': 'application/json'
    }
  });
}

async function handleProjects(request, env, corsHeaders) {
  // Project management endpoint
  if (request.method !== 'POST') {
    return new Response('Method not allowed', { 
      status: 405,
      headers: corsHeaders 
    });
  }
  
  return new Response(JSON.stringify({
    message: 'Projects endpoint',
    note: 'Would connect to Xano taskmaster_projects table'
  }), {
    headers: {
      ...corsHeaders,
      'Content-Type': 'application/json'
    }
  });
}

async function handleTasks(request, env, corsHeaders) {
  // Task management endpoint
  if (request.method !== 'POST') {
    return new Response('Method not allowed', { 
      status: 405,
      headers: corsHeaders 
    });
  }
  
  try {
    const body = await request.json();
    
    // This would call the appropriate Xano API based on the action
    return new Response(JSON.stringify({
      message: 'Tasks endpoint',
      note: 'Would connect to Xano taskmaster_tasks table',
      receivedAction: body.action || 'none'
    }), {
      headers: {
        ...corsHeaders,
        'Content-Type': 'application/json'
      }
    });
  } catch (error) {
    return new Response(JSON.stringify({
      error: 'Invalid request body'
    }), {
      status: 400,
      headers: {
        ...corsHeaders,
        'Content-Type': 'application/json'
      }
    });
  }
}

async function handleAPIRoute(request, env, url, corsHeaders) {
  // Generic API route handler
  return new Response(JSON.stringify({
    message: 'API endpoint',
    path: url.pathname,
    note: 'Dynamic routing for future endpoints'
  }), {
    headers: {
      ...corsHeaders,
      'Content-Type': 'application/json'
    }
  });
}