# Python MCP Server Implementation

This directory contains a complete Python implementation of the MCP server with the same functionality as the TypeScript version.

## Files Structure

```
src/
├── __init__.py          # Package initialization
├── server.py            # Main Python MCP server implementation
└── server_old.py        # Original TypeScript-style implementation (backup)
```

## Python Requirements

- Python 3.8+
- Virtual environment (recommended)

## Dependencies

- `mcp` - Model Context Protocol Python SDK
- `pydantic` - Data validation library
- `mysql-connector-python` - MySQL database connectivity
- `psutil` - System information utilities

## Installation

1. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

### Direct execution:
```bash
python3 src/server.py
```

### Using the virtual environment:
```bash
.venv/bin/python src/server.py
```

## Features Implemented

### 🔧 Tools
- **calculate**: Basic mathematical operations (add, subtract, multiply, divide)
- **get-system-info**: System information (time, platform, memory)
- **generate-data**: Mock data generation (users, products, orders)  
- **mysql-query**: Safe MySQL SELECT query execution

### 📄 Resources
- **README File**: Static project documentation
- **User Profile**: Dynamic user information with parameterized URIs

### 📝 Prompts
- **explain-concept**: Technical concept explanations with audience targeting
- **code-review**: Comprehensive code reviews with focus areas
- **project-planning**: Project planning and structure assistance

## Configuration

The server can be configured in VS Code using `.vscode/mcp.json`:

```json
{
  "servers": {
    "example-mcp-server-python": {
      "type": "stdio",
      "command": "python3",
      "args": [
        "/path/to/your/project/src/server.py"
      ]
    }
  }
}
```

## Testing

Run the test suite:
```bash
python3 test_server.py
```

## Error Handling

The Python implementation includes comprehensive error handling for:
- MySQL connection failures
- Invalid tool arguments
- Resource not found errors
- Tool execution errors
- Prompt parameter validation

## Security Features

- **MySQL Safety**: Only SELECT queries allowed
- **Connection Management**: Automatic connection cleanup
- **Input Validation**: Proper parameter validation for all tools
- **Error Isolation**: Errors don't crash the server

## Differences from TypeScript Version

1. **Type System**: Uses Python's type hints instead of TypeScript's types
2. **Dependencies**: Different package ecosystem (pip vs npm)
3. **Async Handling**: Python's asyncio instead of Node.js event loop
4. **Package Structure**: Python modules instead of ES6 modules

## Development

The Python server maintains full compatibility with the MCP protocol and can be used interchangeably with the TypeScript version.
