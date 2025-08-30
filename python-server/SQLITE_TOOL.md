# SQLite Tool Documentation

## Overview
The SQLite tool provides local database functionality for the Python MCP server, allowing you to create, manage, and query SQLite databases without external dependencies.

## Tool: sqlite-query

### Description
Execute SQLite queries and manage local database operations including table creation, data insertion, and querying.

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | Yes | - | SQL query to execute |
| `database` | string | No | "data.db" | Database file path (relative to python-server directory) |
| `action` | string | No | "query" | Action to perform: "query", "init", or "drop" |
| `limit` | number | No | 100 | Maximum rows to return for SELECT queries (1-1000) |

### Actions

#### 1. Query (`action: "query"`)
Execute any SQL statement on the database.

**Examples:**
```json
{
  "query": "SELECT * FROM users WHERE age > 30",
  "database": "myapp.db"
}
```

```json
{
  "query": "INSERT INTO users (name, email, age) VALUES ('John Doe', 'john@example.com', 25)",
  "database": "myapp.db"
}
```

#### 2. Initialize (`action: "init"`)
Create sample database with pre-defined tables and data.

**Example:**
```json
{
  "action": "init",
  "database": "sample.db",
  "query": "CREATE SAMPLE DATABASE"
}
```

**Creates tables:**
- `users`: User information with id, name, email, age, country
- `products`: Product catalog with id, name, price, category, stock status  
- `orders`: Order records with user/product relationships

**Sample data:** 5 users, 5 products, 5 orders

#### 3. Drop (`action: "drop"`)
Delete the entire database file.

**Example:**
```json
{
  "action": "drop",
  "database": "old_data.db",
  "query": "DROP DATABASE"
}
```

### Response Format

#### SELECT Queries
```json
{
  "database": "data.db",
  "query": "SELECT * FROM users LIMIT 100",
  "rowCount": 3,
  "data": [
    {
      "id": 1,
      "name": "Alice Johnson",
      "email": "alice@example.com",
      "age": 28,
      "country": "US",
      "created_at": "2025-08-30 14:13:06"
    }
  ],
  "fields": ["id", "name", "email", "age", "country", "created_at"]
}
```

#### INSERT/UPDATE/DELETE Queries
```json
{
  "database": "data.db",
  "query": "INSERT INTO users (name, email) VALUES ('Test User', 'test@example.com')",
  "rowsAffected": 1,
  "lastInsertId": 6
}
```

### Security Features
- Automatic LIMIT clause addition for SELECT queries
- Database files restricted to python-server directory
- Proper error handling for SQLite exceptions
- No external network dependencies

### Common Use Cases

1. **Local data storage** for development and testing
2. **Caching** API responses or computed results  
3. **Configuration management** with structured data
4. **Prototyping** database schemas
5. **Data analysis** on local datasets

### Error Handling
The tool provides detailed error messages for:
- SQLite syntax errors
- File permission issues
- Database corruption
- Invalid file paths

### Example Workflow

```json
// 1. Initialize database with sample data
{
  "action": "init",
  "database": "myapp.db",
  "query": "CREATE SAMPLE DATABASE"
}

// 2. Query users
{
  "query": "SELECT name, email FROM users WHERE country = 'US'",
  "database": "myapp.db"
}

// 3. Add new user
{
  "query": "INSERT INTO users (name, email, age, country) VALUES ('Jane Doe', 'jane@example.com', 30, 'CA')",
  "database": "myapp.db"
}

// 4. Check order statistics
{
  "query": "SELECT status, COUNT(*) as count FROM orders GROUP BY status",
  "database": "myapp.db"
}
```

### File Location
Database files are created in the `python-server/` directory alongside the source code.
