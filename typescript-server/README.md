# TypeScript MCP Server

A complete Model Context Protocol (MCP) server built with TypeScript, demonstrating all core MCP capabilities including resources, tools, and prompts.

## Features

### 📄 Resources
- **Static README**: Access to project documentation
- **Dynamic User Profiles**: Parameterized user information resources

### 🔧 Tools
- **Calculator**: Perform basic mathematical operations (add, subtract, multiply, divide)
- **System Information**: Get current time, platform details, and memory usage
- **Data Generator**: Create mock data for testing (users, products, orders)
- **MySQL Query**: Execute SELECT queries against MySQL databases safely

### 📝 Prompts
- **Concept Explanation**: Generate detailed explanations for technical concepts
- **Code Review**: Perform comprehensive code reviews with customizable focus areas
- **Project Planning**: Assist with project planning and structure

## Quick Start

### Prerequisites
- Node.js v18.x or higher
- npm or yarn

### Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Build the project:**
   ```bash
   npm run build
   ```

3. **Test the server:**
   ```bash
   npm start
   ```

### Development

- **Development mode with hot reload:**
  ```bash
  npm run dev
  ```

- **Build only:**
  ```bash
  npm run build
  ```

## Usage with MCP Clients

### VS Code Configuration

Add to your `.vscode/mcp.json`:

```json
{
  "servers": {
    "example-mcp-server-ts": {
      "type": "stdio",
      "command": "node",
      "args": [
        "/path/to/typescript-server/build/index.js"
      ]
    }
  }
}
```

### Claude Desktop Configuration

Add to your Claude Desktop config:

```json
{
  "mcpServers": {
    "example-mcp-server": {
      "command": "node",
      "args": ["/path/to/typescript-server/build/index.js"]
    }
  }
}
```

## Project Structure

```
typescript-server/
├── src/
│   └── index.ts            # Main server implementation
├── build/                  # Compiled JavaScript output
├── package.json            # Node.js dependencies and scripts
├── tsconfig.json          # TypeScript configuration
└── README.md              # This file
```

## Dependencies

- `@modelcontextprotocol/sdk` - MCP TypeScript SDK
- `mysql2` - MySQL database connectivity
- `zod` - Runtime type validation
- `typescript` - TypeScript compiler
- `tsx` - TypeScript execution for development

## Security Features

- **MySQL Safety**: Only SELECT queries allowed
- **Connection Management**: Automatic connection cleanup
- **Input Validation**: Zod schema validation for all tool parameters
- **Error Isolation**: Comprehensive error handling

## Development Notes

- Server uses stdio transport for communication
- All tools include proper error handling and validation
- Resources support both static and dynamic content
- Prompts include parameterized templates for flexible use
