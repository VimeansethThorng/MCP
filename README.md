# Example MCP Server

A complete Model Context Protocol (MCP) server available in both **TypeScript** and **Python** implementations, demonstrating all core MCP capabilities including resources, tools, and prompts.

## Project Structure

```
MCP/
├── typescript-server/          # TypeScript implementation
│   ├── src/
│   │   └── index.ts           # Main TypeScript server
│   ├── build/                 # Compiled JavaScript
│   ├── package.json           # Node.js dependencies
│   ├── tsconfig.json          # TypeScript config
│   └── README.md              # TypeScript-specific docs
├── python-server/             # Python implementation
│   ├── src/
│   │   ├── __init__.py        # Package initialization
│   │   └── server.py          # Main Python server
│   ├── .venv/                 # Virtual environment
│   ├── requirements.txt       # Python dependencies
│   ├── pyproject.toml         # Python packaging
│   ├── setup.py               # Python setup script
│   ├── test_server.py         # Python tests
│   ├── PYTHON_SERVER.md       # Python-specific docs
│   ├── MYSQL_TOOL.md          # MySQL tool documentation
│   └── README.md              # Python-specific docs
├── docs/                      # Project documentation
│   ├── MIGRATION_SUMMARY.md   # Migration notes
│   ├── PROJECT_STRUCTURE.md   # Structure details
│   └── REORGANIZATION_SUMMARY.md # Reorganization notes
├── .vscode/
│   └── mcp.json               # VS Code MCP configuration
├── .github/                   # GitHub configuration
├── test-servers.sh            # Test script for both servers
└── README.md                  # This file
```

## Implementations

### 🟦 TypeScript Version
- Built with Node.js and TypeScript
- Uses the MCP TypeScript SDK
- Located in `typescript-server/`

### 🐍 Python Version  
- Built with Python 3.8+
- Uses the MCP Python SDK
- Located in `python-server/`

Both implementations provide identical functionality and can be used interchangeably.

## Features

This MCP server provides:

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

#### For TypeScript:
- Node.js v18.x or higher
- npm or yarn

#### For Python:
- Python 3.8 or higher
- pip

### Installation

#### TypeScript Setup:

1. **Navigate to TypeScript server:**
   ```bash
   cd typescript-server
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Build the project:**
   ```bash
   npm run build
   ```

4. **Test the server:**
   ```bash
   npm start
   ```

#### Python Setup:

1. **Navigate to Python server:**
   ```bash
   cd python-server
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   # or .venv\Scripts\activate  # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Test the server:**
   ```bash
   python3 src/server.py
   ```

### Development

#### TypeScript:
- **Development mode with hot reload:**
  ```bash
  cd typescript-server
  npm run dev
  ```

- **Build only:**
  ```bash
  cd typescript-server
  npm run build
  ```

#### Python:
- **Run with virtual environment:**
  ```bash
  cd python-server
  .venv/bin/python src/server.py
  ```

- **Run tests:**
  ```bash
  cd python-server
  python3 test_server.py
  ```

### Test Both Servers

Run the comprehensive test script to verify both implementations:

```bash
./test-servers.sh
```

This script will:
- Build and test the TypeScript server
- Run the Python server test suite
- Verify both servers start correctly
- Display usage instructions

## Usage with MCP Clients

### VS Code with GitHub Copilot

This project includes a pre-configured `mcp.json` file for VS Code integration:

1. Ensure the project is built (`npm run build`)
2. The server will be available as "example-mcp-server" in VS Code
3. Use GitHub Copilot agent mode to interact with the server

### Claude Desktop

Add to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "example-mcp-server": {
      "command": "node",
      "args": ["/path/to/this/project/build/index.js"]
    }
  }
}
```

### MCP Inspector

Test your server using the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector node build/index.js
```

## Resource Examples

### Static Resource
- **URI**: `file://README.md`
- **Description**: Project documentation and setup instructions

### Dynamic Resource
- **URI Template**: `user://{userId}/profile`
- **Example**: `user://123/profile`
- **Description**: Get user profile information by ID

## Tool Examples

### Calculator Tool
```json
{
  "operation": "add",
  "a": 5,
  "b": 3
}
```

### System Information
```json
{
  "type": "time"
}
```

### Data Generator
```json
{
  "type": "user",
  "count": 3
}
```

## Prompt Examples

### Concept Explanation
```json
{
  "concept": "Model Context Protocol",
  "audience": "intermediate"
}
```

### Code Review
```json
{
  "code": "function hello() { console.log('world'); }",
  "language": "javascript",
  "focus": "maintainability"
}
```

### Project Planning
```json
{
  "projectType": "web application",
  "requirements": "E-commerce platform with user authentication",
  "timeline": "3 months",
  "teamSize": "4"
}
```

## Development

### Project Structure

```
├── src/
│   └── index.ts          # Main server implementation
├── build/                # Compiled JavaScript output
├── .vscode/
│   └── mcp.json         # VS Code MCP configuration
├── package.json         # Project dependencies and scripts
├── tsconfig.json        # TypeScript configuration
└── README.md           # This file
```

### Adding New Features

#### Adding a Resource
```typescript
server.registerResource(
  "my-resource",
  "my-scheme://resource-path",
  {
    title: "My Resource",
    description: "Description of the resource",
    mimeType: "text/plain"
  },
  async (uri) => ({
    contents: [{
      uri: uri.href,
      text: "Resource content here"
    }]
  })
);
```

#### Adding a Tool
```typescript
server.registerTool(
  "my-tool",
  {
    title: "My Tool",
    description: "What this tool does",
    inputSchema: {
      param1: z.string().describe("Parameter description")
    }
  },
  async ({ param1 }) => ({
    content: [{
      type: "text",
      text: `Result: ${param1}`
    }]
  })
);
```

#### Adding a Prompt
```typescript
server.registerPrompt(
  "my-prompt",
  {
    title: "My Prompt",
    description: "What this prompt does",
    argsSchema: {
      input: z.string().describe("Input parameter")
    }
  },
  ({ input }) => ({
    messages: [{
      role: "user",
      content: {
        type: "text",
        text: `Prompt text with ${input}`
      }
    }]
  })
);
```

## Configuration

### MCP Configuration
The `.vscode/mcp.json` file configures the server for VS Code:
- **Server name**: `example-mcp-server`
- **Transport**: stdio
- **Command**: `node`
- **Arguments**: Path to the compiled server

Update the path in `mcp.json` to match your project location.

## Troubleshooting

### Common Issues

1. **"Cannot find module" errors**
   - Ensure dependencies are installed: `npm install`
   - Rebuild the project: `npm run build`

2. **Server not connecting**
   - Check that the path in `mcp.json` is correct
   - Verify the build output exists in `build/index.js`
   - Ensure Node.js is in your PATH

3. **TypeScript compilation errors**
   - Check Node.js version (requires v18+)
   - Clear node_modules and reinstall: `rm -rf node_modules package-lock.json && npm install`

### Debug Mode

To debug the server, you can add logging:

```typescript
console.error("Debug message", data);
```

Note: Use `console.error()` instead of `console.log()` for debugging when using stdio transport.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP Examples](https://github.com/modelcontextprotocol/servers)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)
