# Python MCP Server

A complete Model Context Protocol (MCP) server built with Python, demonstrating all core MCP capabilities including resources, tools, and prompts.

## Features

### 📄 Resources
- **Static README**: Access to project documentation
- **Dynamic User Profiles**: Parameterized user information resources

### 🔧 Tools
- **Calculator**: Perform basic mathematical operations (add, subtract, multiply, divide)
- **System Information**: Get current time, platform details, and memory usage
- **Data Generator**: Create mock data for testing (users, products, orders)
- **MySQL Query**: Execute SELECT queries against MySQL databases safely
- **SQLite Query**: Local database operations with sample data initialization

### 📝 Prompts
- **Concept Explanation**: Generate detailed explanations for technical concepts
- **Code Review**: Perform comprehensive code reviews with customizable focus areas
- **Project Planning**: Assist with project planning and structure

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip

### Installation

1. **Create virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   # or .venv\Scripts\activate  # Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Test the server:**
   ```bash
   python3 src/server.py
   ```

### Development

- **Run with virtual environment:**
  ```bash
  .venv/bin/python src/server.py
  ```

- **Run tests:**
  ```bash
  python3 test_server.py
  ```

- **Test SQLite functionality:**
  ```bash
  python3 test_sqlite.py
  ```

## Usage with MCP Clients

### VS Code Configuration

Add to your `.vscode/mcp.json`:

```json
{
  "servers": {
    "example-mcp-server-python": {
      "type": "stdio",
      "command": "python3",
      "args": [
        "/path/to/python-server/src/server.py"
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
      "command": "python3",
      "args": ["/path/to/python-server/src/server.py"]
    }
  }
}
```

## Project Structure

```
python-server/
├── src/
│   ├── __init__.py         # Package initialization
│   └── server.py           # Main server implementation
├── .venv/                  # Virtual environment
├── requirements.txt        # Python dependencies
├── setup.py               # Python setup script
├── pyproject.toml         # Modern Python packaging
├── test_server.py         # Test script
└── README.md              # This file
```

## Dependencies

- `mcp` - MCP Python SDK
- `mysql-connector-python` - MySQL database connectivity
- `psutil` - System information utilities
- `pydantic` - Data validation (if needed)

## Security Features

- **MySQL Safety**: Only SELECT queries allowed
- **Connection Management**: Automatic connection cleanup
- **Input Validation**: Proper parameter validation for all tools
- **Error Isolation**: Comprehensive error handling

## Development Notes

- Server uses stdio transport for communication
- All tools include proper error handling and validation
- Resources support both static and dynamic content
- Prompts include parameterized templates for flexible use
- Uses Python's asyncio for asynchronous operations

## Testing

The included test script (`test_server.py`) verifies:
- Server module imports correctly
- All tools are registered and functional
- Resources are accessible
- Prompts are available
- Basic calculator functionality works

### SQLite Database Testing

The `test_sqlite.py` script demonstrates:
- Database initialization with sample data
- Creating tables for users, products, and orders
- Inserting and querying data
- JOIN operations across tables
- Statistical queries and aggregations

Run: `python3 test_sqlite.py`

## SQLite Tool Features

The SQLite tool provides:
- **Local database storage** without external dependencies
- **Sample data initialization** for quick testing
- **Full SQL support** for CREATE, INSERT, UPDATE, DELETE, SELECT
- **Automatic LIMIT clauses** for SELECT queries (safety)
- **Structured JSON responses** with metadata
- **Error handling** for SQLite exceptions

See [`SQLITE_TOOL.md`](SQLITE_TOOL.md) for detailed documentation.
