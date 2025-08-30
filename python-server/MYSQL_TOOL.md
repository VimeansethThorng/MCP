# MySQL Data Retrieval Tool

The MCP server now includes a MySQL data retrieval tool that allows you to execute SELECT queries against MySQL databases safely.

## Tool: `mysql-query`

### Description
Execute MySQL queries and retrieve data from a MySQL database.

### Parameters
- `host` (string, required): MySQL host (e.g., "localhost", "192.168.1.100")
- `port` (number, optional): MySQL port (default: 3306)
- `user` (string, required): MySQL username
- `password` (string, required): MySQL password
- `database` (string, required): Database name to connect to
- `query` (string, required): SQL SELECT query to execute
- `limit` (number, optional): Maximum number of rows to return (default: 100, max: 1000)

### Security Features
- **Read-only queries**: Only SELECT statements are allowed for security
- **Connection timeout**: 10-second connection timeout to prevent hanging
- **Row limits**: Automatic LIMIT clause added if not specified
- **Safe connection handling**: Connections are properly closed after each query

### Example Usage

```json
{
  "tool": "mysql-query",
  "parameters": {
    "host": "localhost",
    "port": 3306,
    "user": "myuser",
    "password": "mypassword",
    "database": "mydatabase",
    "query": "SELECT id, name, email FROM users WHERE active = 1",
    "limit": 50
  }
}
```

### Response Format

The tool returns a JSON object with:
- `query`: The actual query executed (with LIMIT added if needed)
- `rowCount`: Number of rows returned
- `data`: Array of result rows
- `fields`: Array of field metadata (name, type, table)

### Error Handling

The tool handles various error scenarios:
- Connection failures
- Invalid queries (non-SELECT statements)
- Database errors
- Timeout errors

### Requirements

To use this tool, you need:
1. A running MySQL server
2. Valid database credentials
3. Network access to the MySQL server
4. Appropriate database permissions for the user

### Notes

- The tool automatically adds a LIMIT clause if your query doesn't have one
- Only SELECT queries are permitted for security reasons
- Connections are created fresh for each query and properly closed
- Field metadata is included to help understand the data structure
