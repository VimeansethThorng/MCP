#!/usr/bin/env node

/**
 * Example MCP Server built with TypeScript
 * 
 * This server demonstrates the core Model Context Protocol capabilities:
 * - Resources: Expose data and content
 * - Tools: Execute functions that the LLM can call
 * - Prom  ({ concept, audience }) => {
    const targetAudience = audience || "intermediate";
    return {
    messages: [{
      role: "user",
      content: {
        type: "text",
        text: `Please explain the concept of "${concept}" for a ${targetAudience} audience. Include:

1. A clear definition
2. Key characteristics or components
3. Real-world examples or use cases
4. Common misconceptions (if any)
5. Related concepts

Make the explanation accessible and engaging for the target audience level.`
      }
    }]
  };
  }le templates
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import mysql from 'mysql2/promise';

/**
 * Create the MCP server instance
 */
const server = new McpServer({
  name: "example-mcp-server",
  version: "1.0.0",
});

/**
 * Add example resources
 * Resources provide data/content that can be read by the client
 */

// Static resource - provides fixed content
server.registerResource(
  "readme",
  "file://README.md",
  {
    title: "README File",
    description: "Project documentation and setup instructions",
    mimeType: "text/markdown"
  },
  async (uri) => ({
    contents: [{
      uri: uri.href,
      text: `# Example MCP Server

This is an example Model Context Protocol server built with TypeScript.

## Features
- Resource sharing
- Tool execution
- Prompt templates
- Full MCP specification compliance

## Usage
Connect this server to any MCP-compatible client to start using its capabilities.
`
    }]
  })
);

// Dynamic resource with parameters - generates content based on input
server.registerResource(
  "user-info",
  new ResourceTemplate("user://{userId}/profile", { list: undefined }),
  {
    title: "User Profile",
    description: "User profile information",
    mimeType: "application/json"
  },
  async (uri, { userId }) => ({
    contents: [{
      uri: uri.href,
      text: JSON.stringify({
        id: userId,
        name: `User ${userId}`,
        email: `user${userId}@example.com`,
        created: new Date().toISOString(),
        status: "active"
      }, null, 2),
      mimeType: "application/json"
    }]
  })
);

/**
 * Add example tools
 * Tools are functions that the LLM can execute to perform actions
 */

// Simple calculation tool
server.registerTool(
  "calculate",
  {
    title: "Calculator",
    description: "Perform basic mathematical calculations",
    inputSchema: {
      operation: z.enum(["add", "subtract", "multiply", "divide"]).describe("Mathematical operation to perform"),
      a: z.number().describe("First number"),
      b: z.number().describe("Second number")
    }
  },
  async ({ operation, a, b }) => {
    let result: number;
    
    switch (operation) {
      case "add":
        result = a + b;
        break;
      case "subtract":
        result = a - b;
        break;
      case "multiply":
        result = a * b;
        break;
      case "divide":
        if (b === 0) {
          return {
            content: [{
              type: "text",
              text: "Error: Division by zero is not allowed"
            }],
            isError: true
          };
        }
        result = a / b;
        break;
    }
    
    return {
      content: [{
        type: "text",
        text: `${a} ${operation} ${b} = ${result}`
      }]
    };
  }
);

// System information tool
server.registerTool(
  "get-system-info",
  {
    title: "System Information",
    description: "Get information about the current system",
    inputSchema: {
      type: z.enum(["time", "platform", "memory"]).describe("Type of system information to retrieve")
    }
  },
  async ({ type }) => {
    let info: string;
    
    switch (type) {
      case "time":
        info = `Current time: ${new Date().toISOString()}`;
        break;
      case "platform":
        info = `Platform: ${process.platform}, Node.js: ${process.version}`;
        break;
      case "memory":
        const memUsage = process.memoryUsage();
        info = `Memory usage:\n` +
               `- RSS: ${Math.round(memUsage.rss / 1024 / 1024)}MB\n` +
               `- Heap Used: ${Math.round(memUsage.heapUsed / 1024 / 1024)}MB\n` +
               `- Heap Total: ${Math.round(memUsage.heapTotal / 1024 / 1024)}MB`;
        break;
    }
    
    return {
      content: [{
        type: "text",
        text: info
      }]
    };
  }
);

// Mock data generation tool
server.registerTool(
  "generate-data",
  {
    title: "Data Generator", 
    description: "Generate mock data for testing purposes",
    inputSchema: {
      type: z.enum(["user", "product", "order"]).describe("Type of data to generate"),
      count: z.number().min(1).max(10).default(1).describe("Number of items to generate")
    }
  },
  async ({ type, count }) => {
    const generateUser = (id: number) => ({
      id,
      name: `User ${id}`,
      email: `user${id}@example.com`,
      age: Math.floor(Math.random() * 50) + 18,
      country: ["US", "UK", "CA", "AU", "DE"][Math.floor(Math.random() * 5)]
    });
    
    const generateProduct = (id: number) => ({
      id,
      name: `Product ${id}`,
      price: +(Math.random() * 100).toFixed(2),
      category: ["Electronics", "Clothing", "Books", "Home", "Sports"][Math.floor(Math.random() * 5)],
      inStock: Math.random() > 0.2
    });
    
    const generateOrder = (id: number) => ({
      id,
      userId: Math.floor(Math.random() * 100) + 1,
      productId: Math.floor(Math.random() * 50) + 1,
      quantity: Math.floor(Math.random() * 5) + 1,
      total: +(Math.random() * 500).toFixed(2),
      status: ["pending", "confirmed", "shipped", "delivered"][Math.floor(Math.random() * 4)]
    });
    
    let data: any[];
    
    switch (type) {
      case "user":
        data = Array.from({ length: count }, (_, i) => generateUser(i + 1));
        break;
      case "product":
        data = Array.from({ length: count }, (_, i) => generateProduct(i + 1));
        break;
      case "order":
        data = Array.from({ length: count }, (_, i) => generateOrder(i + 1));
        break;
    }
    
    return {
      content: [{
        type: "text",
        text: JSON.stringify(data, null, 2)
      }]
    };
  }
);

// MySQL data retrieval tool
server.registerTool(
  "mysql-query",
  {
    title: "MySQL Query",
    description: "Execute MySQL queries and retrieve data",
    inputSchema: {
      host: z.string().describe("MySQL host (e.g., localhost)"),
      port: z.number().default(3306).describe("MySQL port"),
      user: z.string().describe("MySQL username"),
      password: z.string().describe("MySQL password"),
      database: z.string().describe("Database name"),
      query: z.string().describe("SQL query to execute"),
      limit: z.number().min(1).max(1000).default(100).describe("Maximum number of rows to return")
    }
  },
  async ({ host, port, user, password, database, query, limit }) => {
    let connection;
    
    try {
      // Create MySQL connection
      connection = await mysql.createConnection({
        host,
        port,
        user,
        password,
        database,
        connectTimeout: 10000
      });

      // Validate query type (only allow SELECT queries for safety)
      const trimmedQuery = query.trim().toLowerCase();
      if (!trimmedQuery.startsWith('select')) {
        return {
          content: [{
            type: "text",
            text: "Error: Only SELECT queries are allowed for security reasons"
          }],
          isError: true
        };
      }

      // Add LIMIT clause if not already present
      let finalQuery = query;
      if (!trimmedQuery.includes('limit')) {
        finalQuery += ` LIMIT ${limit}`;
      }

      // Execute query
      const [rows, fields] = await connection.execute(finalQuery);
      
      // Format results
      const results = {
        query: finalQuery,
        rowCount: Array.isArray(rows) ? rows.length : 0,
        data: rows,
        fields: fields?.map(field => ({
          name: field.name,
          type: field.type,
          table: field.table
        }))
      };

      return {
        content: [{
          type: "text",
          text: JSON.stringify(results, null, 2)
        }]
      };

    } catch (error) {
      return {
        content: [{
          type: "text",
          text: `MySQL Error: ${error instanceof Error ? error.message : 'Unknown error occurred'}`
        }],
        isError: true
      };
    } finally {
      // Close connection
      if (connection) {
        await connection.end();
      }
    }
  }
);

/**
 * Add example prompts
 * Prompts are reusable templates that help structure LLM interactions
 */

server.registerPrompt(
  "explain-concept",
  {
    title: "Concept Explanation",
    description: "Generate a detailed explanation of a technical concept",
    argsSchema: {
      concept: z.string().describe("The concept to explain"),
      audience: z.enum(["beginner", "intermediate", "advanced"]).optional().describe("Target audience level")
    }
  },
  ({ concept, audience }) => {
    const targetAudience = audience || "intermediate";
    return {
    messages: [{
      role: "user",
      content: {
        type: "text",
        text: `Please explain the concept of "${concept}" for a ${targetAudience} audience. Include:

1. A clear definition
2. Key characteristics or components
3. Real-world examples or use cases
4. Common misconceptions (if any)
5. Related concepts

Make the explanation accessible and engaging for the target audience level.`
      }
    }]
  };
  }
);

server.registerPrompt(
  "code-review",
  {
    title: "Code Review",
    description: "Perform a comprehensive code review",
    argsSchema: {
      code: z.string().describe("The code to review"),
      language: z.string().describe("Programming language of the code"),
      focus: z.enum(["security", "performance", "maintainability", "all"]).optional().describe("Review focus area")
    }
  },
  ({ code, language, focus }) => {
    const reviewFocus = focus || "all";
    return {
    messages: [{
      role: "user", 
      content: {
        type: "text",
        text: `Please review this ${language} code with a focus on ${reviewFocus}:

\`\`\`${language}
${code}
\`\`\`

Provide feedback on:
${reviewFocus === "all" || reviewFocus === "security" ? "- Security vulnerabilities or concerns" : ""}
${reviewFocus === "all" || reviewFocus === "performance" ? "- Performance optimizations" : ""}
${reviewFocus === "all" || reviewFocus === "maintainability" ? "- Code maintainability and readability" : ""}
${reviewFocus === "all" ? "- Best practices adherence\n- Potential bugs or issues" : ""}

Include specific recommendations for improvement.`
      }
    }]
  };
  }
);

server.registerPrompt(
  "project-planning",
  {
    title: "Project Planning Assistant",
    description: "Help plan and structure a project",
    argsSchema: {
      projectType: z.string().describe("Type of project (e.g., web app, mobile app, API)"),
      requirements: z.string().describe("Project requirements and goals"),
      timeline: z.string().describe("Expected timeline or deadline"),
      teamSize: z.string().describe("Number of team members")
    }
  },
  ({ projectType, requirements, timeline, teamSize }) => ({
    messages: [{
      role: "user",
      content: {
        type: "text", 
        text: `Help me plan a ${projectType} project with the following details:

**Requirements:** ${requirements}
**Timeline:** ${timeline}
**Team Size:** ${teamSize} members

Please provide:
1. Project breakdown and milestones
2. Technology stack recommendations
3. Team role suggestions
4. Risk assessment and mitigation strategies
5. Timeline estimates for key phases
6. Development methodology recommendations

Consider best practices for project management and delivery.`
      }
    }]
  })
);

/**
 * Start the server
 */
async function main() {
  // Use stdio transport for communication
  const transport = new StdioServerTransport();
  
  try {
    await server.connect(transport);
    console.error("Example MCP Server running on stdio");
  } catch (error) {
    console.error("Failed to start server:", error);
    process.exit(1);
  }
}

// Handle graceful shutdown
process.on('SIGINT', async () => {
  console.error("Shutting down server...");
  await server.close();
  process.exit(0);
});

process.on('SIGTERM', async () => {
  console.error("Shutting down server...");
  await server.close();
  process.exit(0);
});

// Start the server
main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
