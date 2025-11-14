# Using Public MCP Servers: Extending AI Capabilities

## Learning Objective
Learn how to discover, configure, and use public Model Context Protocol (MCP) servers to extend AI assistants with external tools, data sources, and APIs. Understand the MCP ecosystem and how to integrate various services.

## What is MCP?

The Model Context Protocol (MCP) is an open protocol that enables AI assistants to:
- Access external tools and APIs
- Query databases and data sources
- Interact with web services
- Execute system commands
- Access real-time information

Think of MCP as a way to give your AI assistant "superpowers" by connecting it to external services.

## Prerequisites
- Claude Code or GitHub Copilot installed
- Node.js 18+ installed (for most MCP servers)
- Basic understanding of JSON configuration
- API keys for services you want to use (varies by server)

---

## Part 1: MCP Server Discovery

### Popular Public MCP Servers

Here are some widely-used public MCP servers:

#### 1. **Filesystem MCP**
Access local files and directories
- **Repository:** `@modelcontextprotocol/server-filesystem`
- **Use cases:** Read/write files, search directories, file operations
- **No API key needed**

#### 2. **GitHub MCP**
Interact with GitHub repositories
- **Repository:** `@modelcontextprotocol/server-github`
- **Use cases:** Create issues, PRs, search repos, read code
- **Requires:** GitHub personal access token

#### 3. **Brave Search MCP**
Web search using Brave Search API
- **Repository:** `@modelcontextprotocol/server-brave-search`
- **Use cases:** Real-time web search, news, information lookup
- **Requires:** Brave Search API key (free tier available)

#### 4. **PostgreSQL MCP**
Query and manage PostgreSQL databases
- **Repository:** `@modelcontextprotocol/server-postgres`
- **Use cases:** Database queries, schema inspection, data analysis
- **Requires:** PostgreSQL connection string

#### 5. **Puppeteer MCP**
Browser automation and web scraping
- **Repository:** `@modelcontextprotocol/server-puppeteer`
- **Use cases:** Web scraping, screenshots, form filling
- **No API key needed** (uses local Chrome)

#### 6. **Google Drive MCP**
Access Google Drive files
- **Repository:** `@modelcontextprotocol/server-gdrive`
- **Use cases:** Read/search Drive files, list folders
- **Requires:** Google OAuth credentials

#### 7. **Slack MCP**
Interact with Slack workspaces
- **Repository:** `@modelcontextprotocol/server-slack`
- **Use cases:** Send messages, read channels, search conversations
- **Requires:** Slack bot token

#### 8. **Sequential Thinking MCP**
Advanced reasoning and problem-solving
- **Repository:** `@modelcontextprotocol/server-sequential-thinking`
- **Use cases:** Complex problem decomposition, step-by-step reasoning
- **No API key needed**

#### 9. **Memory MCP**
Persistent memory for conversations
- **Repository:** `@modelcontextprotocol/server-memory`
- **Use cases:** Remember facts across sessions, build knowledge base
- **No API key needed**

#### 10. **Fetch MCP**
HTTP requests and API calls
- **Repository:** `@modelcontextprotocol/server-fetch`
- **Use cases:** Call REST APIs, download web content
- **No API key needed** (unless target APIs require auth)

---

## Part 2: Setting Up MCP Servers

### Installation Methods

#### Method 1: Global NPM Installation

```bash
# Install MCP servers globally
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-brave-search
npm install -g @modelcontextprotocol/server-github
npm install -g @modelcontextprotocol/server-postgres
```

#### Method 2: Project-Specific Installation

```bash
# Create a dedicated MCP directory
mkdir ~/.mcp-servers
cd ~/.mcp-servers

# Initialize npm
npm init -y

# Install MCP servers locally
npm install @modelcontextprotocol/server-filesystem
npm install @modelcontextprotocol/server-brave-search
npm install @modelcontextprotocol/server-github
npm install @modelcontextprotocol/server-postgres
npm install @modelcontextprotocol/server-puppeteer
```

#### Method 3: Using npx (No Installation)

MCP servers can also be run directly with `npx` (configured in settings).

---

## Part 3: Configuration

### For Claude Code (Claude Desktop/CLI)

Create or edit `~/.config/mcp/config.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/home/username/projects",
        "/home/username/documents"
      ]
    },
    "brave-search": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-brave-search"
      ],
      "env": {
        "BRAVE_API_KEY": "your-brave-api-key-here"
      }
    },
    "github": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "github_pat_xxxxx"
      }
    },
    "postgres": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-postgres"
      ],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://user:pass@localhost:5432/dbname"
      }
    },
    "puppeteer": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-puppeteer"
      ]
    },
    "memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ]
    },
    "sequential-thinking": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sequential-thinking"
      ]
    }
  }
}
```

### For GitHub Copilot (VS Code)

Edit VS Code settings (`.vscode/settings.json` or user settings):

```json
{
  "github.copilot.chat.mcp.servers": {
    "filesystem": {
      "command": "node",
      "args": [
        "/path/to/node_modules/@modelcontextprotocol/server-filesystem/dist/index.js",
        "/home/username/projects"
      ]
    },
    "brave-search": {
      "command": "node",
      "args": [
        "/path/to/node_modules/@modelcontextprotocol/server-brave-search/dist/index.js"
      ],
      "env": {
        "BRAVE_API_KEY": "your-api-key"
      }
    }
  }
}
```

---

## Part 4: Getting API Keys

### Brave Search API
1. Go to [link](https://brave.com/search/api/)
1. Sign up for free tier (2,000 queries/month)
1. Create an API key
1. Add to your MCP config

### GitHub Personal Access Token
1. Go to [link](https://github.com/settings/tokens)
1. Click "Generate new token (classic)"
1. Select scopes: `repo`, `read:org`, `read:user`
1. Copy token and add to MCP config

### Google Drive OAuth
1. Go to [link](https://console.cloud.google.com/)
1. Create a new project
1. Enable Google Drive API
1. Create OAuth 2.0 credentials
1. Download credentials JSON
1. Configure in MCP settings

### Slack Bot Token
1. Go to [link](https://api.slack.com/apps)
1. Create a new app
1. Add bot token scopes: `channels:read`, `chat:write`, `users:read`
1. Install app to workspace
1. Copy bot token

---

## Part 5: Practical Exercises

### Exercise 5.1: Filesystem Operations

**Setup Filesystem MCP:**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/home/username/projects"
      ]
    }
  }
}
```

**Tasks:**

1. **List all Python files in a directory**

```txt
Ask your AI: "Using the filesystem tools, list all .py files in the projects directory"
```

1. **Read and analyze a file**

```txt
"Read the contents of config.py and explain what it does"
```

1. **Search for a specific function**

```txt
"Search all files for the function definition 'calculate_total'"
```

1. **Create a new file**

```txt
"Create a new file called 'test_utils.py' with basic pytest structure"
```

1. **Find TODO comments**

```txt
"Search all files for TODO comments and list them"
```

### Exercise 5.2: Web Search with Brave

**Setup Brave Search MCP:**
```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "your-key-here"
      }
    }
  }
}
```

**Tasks:**

1. **Find latest library versions**

```txt
"Use Brave Search to find the latest version of FastAPI and its release notes"
```

1. **Research a bug**

```txt
"Search for solutions to 'Python asyncio RuntimeError: Event loop is closed'"
```

1. **Find code examples**

```txt
"Search for examples of implementing JWT authentication in Express.js"
```

1. **Check documentation**

```txt
"Find the official documentation for PostgreSQL's JSONB operators"
```

1. **News about technology**

```txt
"What are the latest news about Python 3.13 release?"
```

### Exercise 5.3: GitHub Integration

**Setup GitHub MCP:**
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "github_pat_xxxxx"
      }
    }
  }
}
```

**Tasks:**

1. **Search repositories**

```txt
"Search GitHub for popular Python REST API frameworks with over 10k stars"
```

1. **Read a specific file**

```txt
"Read the README.md from the 'fastapi/fastapi' repository"
```

1. **Check issues**

```txt
"List open issues in the 'python/cpython' repo tagged with 'performance'"
```

1. **Create an issue** (if you have write access)

```txt
"Create an issue in my repo 'myuser/myproject' about adding Docker support"
```

1. **Analyze repository structure**

```txt
"Show me the directory structure of 'microsoft/vscode' repository"
```

### Exercise 5.4: Database Queries

**Setup PostgreSQL MCP:**
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://user:pass@localhost:5432/mydb"
      }
    }
  }
}
```

**Tasks:**

1. **Explore database schema**

```txt
"Show me all tables in the database with their column information"
```

1. **Write a query**

```txt
"Query the users table for all users created in the last 7 days"
```

1. **Analyze data**

```txt
"Calculate the average order value by customer segment"
```

1. **Generate report**

```txt
"Create a sales report showing monthly revenue for the last 6 months"
```

1. **Optimize query**

```txt
"Analyze this slow query and suggest optimizations with indexes"
```

### Exercise 5.5: Web Scraping with Puppeteer

**Setup Puppeteer MCP:**
```json
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
    }
  }
}
```

**Tasks:**

1. **Take a screenshot**

```txt
"Take a screenshot of https://example.com"
```

1. **Extract data**

```txt
"Scrape the main headline and first paragraph from https://news.ycombinator.com"
```

1. **Check page title**

```txt
"Navigate to https://github.com and tell me the page title"
```

1. **Fill a form** (be ethical!)

```txt
"Navigate to a test form page and demonstrate filling it out"
```

1. **Monitor page changes**

```txt
"Check if a specific element exists on a webpage"
```

### Exercise 5.6: Advanced Reasoning

**Setup Sequential Thinking MCP:**

```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    }
  }
}
```

**Tasks:**

1. **Complex algorithm design**

```txt
"Use sequential thinking to design an algorithm for finding the shortest path
in a graph with weighted edges and some blocked nodes"
```

1. **Architectural decisions**

```txt
"Help me think through the architecture for a real-time chat application
with 100k concurrent users"
```

1. **Debug a complex issue**

```txt
"Walk me through debugging a memory leak in a long-running Python service"
```

1. **System design**

```txt
"Design a distributed cache system with consistency guarantees"
```

1. **Optimization problem**

```txt
"How would you optimize a database with 100M rows for fast full-text search?"
```

---

## Part 6: Combining Multiple MCP Servers

The real power comes from using multiple MCP servers together.

### Scenario 1: Research and Implementation

**MCP Servers:** Brave Search + Filesystem + GitHub

**Task:** Research a library, download example code, and implement locally

```txt
User: "I need to implement OAuth2 authentication in my Express.js app"

AI with MCP:
1. [Brave Search] "Search for popular OAuth2 libraries for Express.js"
1. [GitHub] "Read the README of 'jaredhanson/passport'"
1. [Brave Search] "Find best practices for OAuth2 implementation"
1. [Filesystem] "Create a new file auth/oauth.js in my project"
1. [Filesystem] "Write the implementation based on the research"
```

### Scenario 2: Database Analysis and Reporting

**MCP Servers:** PostgreSQL + Filesystem

**Task:** Analyze database and create a report

```txt
User: "Analyze our customer data and create a markdown report"

AI with MCP:
1. [PostgreSQL] "Query customer demographics"
1. [PostgreSQL] "Calculate retention metrics"
1. [PostgreSQL] "Find top products by revenue"
1. [Filesystem] "Create reports/customer_analysis_2024.md"
1. [Filesystem] "Write formatted report with findings and visualizations"
```

### Scenario 3: Code Review with Context

**MCP Servers:** Filesystem + GitHub + Brave Search

**Task:** Review code with external research

```txt
User: "Review my authentication code for security issues"

AI with MCP:
1. [Filesystem] "Read src/auth/login.js"
1. [Brave Search] "Search for common authentication vulnerabilities 2024"
1. [GitHub] "Check how popular projects implement similar features"
1. [Filesystem] "List all files importing the auth module"
1. [Provide comprehensive review with industry best practices]
```

---

## Part 7: Creating Your Own MCP Server

While this exercise focuses on using public MCP servers, you can also create your own!

### Simple MCP Server Template

```typescript
#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  {
    name: "my-custom-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Define available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "my_tool",
        description: "Description of what this tool does",
        inputSchema: {
          type: "object",
          properties: {
            param1: {
              type: "string",
              description: "Description of param1",
            },
          },
          required: ["param1"],
        },
      },
    ],
  };
});

// Handle tool execution
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "my_tool") {
    const { param1 } = request.params.arguments;

    // Your tool logic here
    const result = `Processed: ${param1}`;

    return {
      content: [
        {
          type: "text",
          text: result,
        },
      ],
    };
  }

  throw new Error(`Unknown tool: ${request.params.name}`);
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("My Custom MCP server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
```

---

## Part 8: Troubleshooting Common Issues

### Issue 1: MCP Server Not Found

**Error:** "MCP server 'xyz' not responding"

**Solutions:**
1. Check the command path is correct
2. Verify npx can access the package: `npx @modelcontextprotocol/server-filesystem --help`
3. Try absolute paths instead of npx
4. Check Node.js is in PATH

### Issue 2: Authentication Failures

**Error:** "Invalid API key" or "Authentication failed"

**Solutions:**
1. Verify API key is correct (no extra spaces)
2. Check key hasn't expired
3. Verify key has necessary permissions
4. Check environment variables are loaded correctly

### Issue 3: Permission Denied

**Error:** "EACCES: permission denied"

**Solutions:**
1. Check file/directory permissions
2. For filesystem MCP, ensure paths in config are accessible
3. Run with appropriate user permissions
4. Check SELinux/AppArmor policies if on Linux

### Issue 4: MCP Server Crashes

**Error:** Server exits immediately or crashes

**Solutions:**
1. Check server logs (stderr output)
2. Verify all required environment variables are set
3. Test server manually: `npx @modelcontextprotocol/server-xyz`
4. Update to latest version: `npm update -g @modelcontextprotocol/server-xyz`

### Issue 5: Rate Limiting

**Error:** "Rate limit exceeded"

**Solutions:**
1. Check API usage limits
2. Implement caching for repeated queries
3. Upgrade to higher API tier
4. Add delays between requests

---

## Part 9: Best Practices

### Security

1. **Never commit API keys** to version control
   ```bash
   # Add to .gitignore
   echo "mcp-config.json" >> .gitignore
   echo ".env" >> .gitignore
   ```

1. **Use environment variables**
   ```bash
   # Store keys in .env file
   export BRAVE_API_KEY="your-key"
   export GITHUB_TOKEN="your-token"
   ```

1. **Limit filesystem access**
   ```json
   // Only allow specific directories
   {
     "filesystem": {
       "args": [
         "path/to/specific/project",
         "path/to/documents"
       ]
     }
   }
   ```

1. **Use read-only database connections** when possible

```url
postgresql://user:pass@localhost:5432/db?options=--search_path=readonly_schema
```

### Performance

1. **Cache API responses** when appropriate
1. **Limit concurrent MCP server instances**
1. **Use specific tools** rather than asking AI to choose
1. **Set appropriate timeouts**

### Reliability

1. **Handle failures gracefully**
1. **Implement retry logic** for network calls
1. **Validate inputs** before calling MCP tools
1. **Log errors** for debugging

---

## Part 10: Advanced Use Cases

### Use Case 1: Automated Code Review Pipeline

**MCP Servers:** Filesystem + GitHub + Brave Search

```txt
System: When a PR is created:
1. [Filesystem] Read changed files
1. [Brave Search] Check for known vulnerabilities in dependencies
1. [GitHub] Compare with similar PRs in other repos
1. [Filesystem] Generate review comments
1. [GitHub] Post review comments
```

### Use Case 2: Documentation Generator

**MCP Servers:** Filesystem + Brave Search + GitHub

```txt
System: Generate comprehensive docs:
1. [Filesystem] Read all source files
1. [Brave Search] Find best documentation practices
1. [GitHub] Check how similar projects document
1. [Filesystem] Generate markdown docs
1. [Filesystem] Create navigation structure
```

### Use Case 3: Database Migration Assistant

**MCP Servers:** PostgreSQL + Filesystem + Brave Search

```txt
System: Assist with database migrations:
1. [PostgreSQL] Analyze current schema
1. [Brave Search] Research best migration practices
1. [Filesystem] Generate migration files
1. [PostgreSQL] Validate migration (dry run)
1. [Filesystem] Create rollback scripts
```

### Use Case 4: Competitive Analysis

**MCP Servers:** Brave Search + GitHub + Puppeteer

```txt
System: Research competitors:
1. [Brave Search] Find competitor websites
1. [Puppeteer] Extract features from competitor sites
1. [GitHub] Find competitor open-source projects
1. [Filesystem] Generate comparison report
```

---

## Part 11: MCP Ecosystem Resources

### Official Resources

- **MCP Specification:** [link](https://spec.modelcontextprotocol.io/)
- **MCP SDK:** [link](https://github.com/modelcontextprotocol/sdk)
- **Official Servers:** [link](https://github.com/modelcontextprotocol/servers)

### Community Resources

- **Awesome MCP:** List of community MCP servers
- **MCP Discord:** Community support and discussion
- **Example Implementations:** Various language implementations

### Popular Community MCP Servers

1. **Docker MCP** - Container management
1. **AWS MCP** - AWS service integration
1. **Redis MCP** - Redis operations
1. **Elasticsearch MCP** - Search operations
1. **Stripe MCP** - Payment processing
1. **SendGrid MCP** - Email sending
1. **Twilio MCP** - SMS/Voice operations
1. **Google Calendar MCP** - Calendar integration

---

## Success Criteria

After completing this exercise, you should be able to:

- [ ] Configure multiple MCP servers
- [ ] Obtain and securely store API keys
- [ ] Use filesystem MCP for local file operations
- [ ] Perform web searches through Brave Search MCP
- [ ] Interact with GitHub repositories via MCP
- [ ] Query databases using PostgreSQL MCP
- [ ] Combine multiple MCP servers for complex tasks
- [ ] Troubleshoot common MCP issues
- [ ] Follow security best practices
- [ ] Understand when to use each type of MCP server

## Real-World Projects

Try these complete projects using MCP:

1. **Project Documentation Generator**
    - Use Filesystem to read code
    - Use Brave Search for documentation standards
    - Generate comprehensive docs

1. **Database Health Monitor**
    - Use PostgreSQL MCP to query metrics
    - Use Filesystem to log results
    - Generate alerts for anomalies

1. **GitHub Repository Analyzer**
    - Use GitHub MCP to fetch repo data
    - Use Brave Search for similar projects
    - Generate comparison report

1. **Automated Bug Report System**
    - Use Filesystem to detect errors
    - Use Brave Search to find known solutions
    - Use GitHub to create issues

1. **Code Migration Assistant**
    - Use Filesystem to read old code
    - Use Brave Search for migration guides
    - Generate updated code

---

## Further Learning

- Explore creating custom MCP servers
- Integrate MCP with CI/CD pipelines
- Build MCP-powered automation workflows
- Contribute to MCP ecosystem
- Share your MCP configurations with team

Remember: MCP servers are tools that extend your AI assistant's capabilities. Choose the right tools for your specific needs and always follow security best practices!
