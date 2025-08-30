#!/usr/bin/env python3

"""
Example MCP Server built with Python

This server demonstrates the core Model Context Protocol capabilities:
- Resources: Expose data and content
- Tools: Execute functions that the LLM can call
- Prompts: Reusable templates
"""

import asyncio
import json
import logging
import sys
import datetime
import platform
import random
from typing import Any, Dict, List, Optional

import mysql.connector
from mysql.connector import Error as MySQLError
import psutil

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the MCP server instance
server = Server("example-mcp-server")


@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """List available resources."""
    return [
        types.Resource(
            uri="file://README.md",
            name="README File",
            description="Project documentation and setup instructions",
            mimeType="text/markdown"
        ),
        types.Resource(
            uri="user://profile/{userId}",
            name="User Profile", 
            description="User profile information",
            mimeType="application/json"
        )
    ]


@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Read a specific resource."""
    if uri == "file://README.md":
        return """# Example MCP Server

This is an example Model Context Protocol server built with Python.

## Features
- Resource sharing
- Tool execution
- Prompt templates
- Full MCP specification compliance

## Usage
Connect this server to any MCP-compatible client to start using its capabilities.
"""
    
    elif uri.startswith("user://profile/"):
        user_id = uri.split("/")[-1]
        user_data = {
            "id": user_id,
            "name": f"User {user_id}",
            "email": f"user{user_id}@example.com",
            "created": "2024-01-01T00:00:00Z",
            "status": "active"
        }
        return json.dumps(user_data, indent=2)
    
    else:
        raise ValueError(f"Unknown resource: {uri}")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="calculate",
            description="Perform basic mathematical calculations",
            inputSchema={
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["add", "subtract", "multiply", "divide"],
                        "description": "Mathematical operation to perform"
                    },
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number"
                    }
                },
                "required": ["operation", "a", "b"]
            }
        ),
        types.Tool(
            name="get-system-info",
            description="Get information about the current system",
            inputSchema={
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": ["time", "platform", "memory"],
                        "description": "Type of system information to retrieve"
                    }
                },
                "required": ["type"]
            }
        ),
        types.Tool(
            name="generate-data",
            description="Generate mock data for testing purposes",
            inputSchema={
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": ["user", "product", "order"],
                        "description": "Type of data to generate"
                    },
                    "count": {
                        "type": "number",
                        "minimum": 1,
                        "maximum": 10,
                        "default": 1,
                        "description": "Number of items to generate"
                    }
                },
                "required": ["type"]
            }
        ),
        types.Tool(
            name="mysql-query",
            description="Execute MySQL queries and retrieve data",
            inputSchema={
                "type": "object",
                "properties": {
                    "host": {
                        "type": "string",
                        "description": "MySQL host"
                    },
                    "port": {
                        "type": "number",
                        "default": 3306,
                        "description": "MySQL port"
                    },
                    "user": {
                        "type": "string",
                        "description": "MySQL username"
                    },
                    "password": {
                        "type": "string",
                        "description": "MySQL password"
                    },
                    "database": {
                        "type": "string",
                        "description": "Database name"
                    },
                    "query": {
                        "type": "string",
                        "description": "SQL query to execute"
                    },
                    "limit": {
                        "type": "number",
                        "minimum": 1,
                        "maximum": 1000,
                        "default": 100,
                        "description": "Maximum number of rows to return"
                    }
                },
                "required": ["host", "user", "password", "database", "query"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Execute a tool with the given arguments."""
    
    if name == "calculate":
        operation = arguments.get("operation")
        a = arguments.get("a")
        b = arguments.get("b")
        
        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        elif operation == "divide":
            if b == 0:
                return [types.TextContent(
                    type="text",
                    text="Error: Division by zero is not allowed"
                )]
            result = a / b
        else:
            return [types.TextContent(
                type="text",
                text=f"Error: Unknown operation {operation}"
            )]
        
        return [types.TextContent(
            type="text",
            text=f"{a} {operation} {b} = {result}"
        )]
    
    elif name == "get-system-info":
        info_type = arguments.get("type")
        
        if info_type == "time":
            info = f"Current time: {datetime.datetime.now().isoformat()}"
        elif info_type == "platform":
            info = f"Platform: {platform.system()} {platform.release()}, Python: {platform.python_version()}"
        elif info_type == "memory":
            memory = psutil.virtual_memory()
            info = f"Memory usage:\n- Total: {memory.total // 1024 // 1024}MB\n- Available: {memory.available // 1024 // 1024}MB\n- Used: {memory.used // 1024 // 1024}MB"
        else:
            return [types.TextContent(
                type="text",
                text=f"Error: Unknown info type {info_type}"
            )]
        
        return [types.TextContent(
            type="text",
            text=info
        )]
    
    elif name == "generate-data":
        data_type = arguments.get("type")
        count = arguments.get("count", 1)
        
        def generate_user(id: int) -> Dict[str, Any]:
            return {
                "id": id,
                "name": f"User {id}",
                "email": f"user{id}@example.com",
                "age": random.randint(18, 67),
                "country": random.choice(["US", "UK", "CA", "AU", "DE"])
            }
        
        def generate_product(id: int) -> Dict[str, Any]:
            return {
                "id": id,
                "name": f"Product {id}",
                "price": round(random.uniform(1, 100), 2),
                "category": random.choice(["Electronics", "Clothing", "Books", "Home", "Sports"]),
                "inStock": random.random() > 0.2
            }
        
        def generate_order(id: int) -> Dict[str, Any]:
            return {
                "id": id,
                "userId": random.randint(1, 100),
                "productId": random.randint(1, 50),
                "quantity": random.randint(1, 5),
                "total": round(random.uniform(10, 500), 2),
                "status": random.choice(["pending", "confirmed", "shipped", "delivered"])
            }
        
        if data_type == "user":
            data = [generate_user(i + 1) for i in range(count)]
        elif data_type == "product":
            data = [generate_product(i + 1) for i in range(count)]
        elif data_type == "order":
            data = [generate_order(i + 1) for i in range(count)]
        else:
            return [types.TextContent(
                type="text",
                text=f"Error: Unknown data type {data_type}"
            )]
        
        return [types.TextContent(
            type="text",
            text=json.dumps(data, indent=2)
        )]
    
    elif name == "mysql-query":
        host = arguments.get("host")
        port = arguments.get("port", 3306)
        user = arguments.get("user")
        password = arguments.get("password")
        database = arguments.get("database")
        query = arguments.get("query")
        limit = arguments.get("limit", 100)
        
        try:
            # Validate query type (only allow SELECT queries for safety)
            trimmed_query = query.strip().lower()
            if not trimmed_query.startswith('select'):
                return [types.TextContent(
                    type="text",
                    text="Error: Only SELECT queries are allowed for security reasons"
                )]
            
            # Add LIMIT clause if not already present
            final_query = query
            if 'limit' not in trimmed_query:
                final_query += f" LIMIT {limit}"
            
            # Create MySQL connection
            connection = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                connection_timeout=10
            )
            
            cursor = connection.cursor(dictionary=True)
            cursor.execute(final_query)
            
            rows = cursor.fetchall()
            field_names = [desc[0] for desc in cursor.description] if cursor.description else []
            
            results = {
                "query": final_query,
                "rowCount": len(rows),
                "data": rows,
                "fields": field_names
            }
            
            cursor.close()
            connection.close()
            
            return [types.TextContent(
                type="text",
                text=json.dumps(results, indent=2, default=str)
            )]
            
        except MySQLError as e:
            return [types.TextContent(
                type="text",
                text=f"MySQL Error: {str(e)}"
            )]
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error: {str(e)}"
            )]
    
    else:
        return [types.TextContent(
            type="text",
            text=f"Error: Unknown tool {name}"
        )]


@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """List available prompts."""
    return [
        types.Prompt(
            name="explain-concept",
            description="Generate a detailed explanation of a technical concept",
            arguments=[
                types.PromptArgument(
                    name="concept",
                    description="The concept to explain",
                    required=True
                ),
                types.PromptArgument(
                    name="audience",
                    description="Target audience level",
                    required=False
                )
            ]
        ),
        types.Prompt(
            name="code-review",
            description="Perform a comprehensive code review",
            arguments=[
                types.PromptArgument(
                    name="code",
                    description="The code to review",
                    required=True
                ),
                types.PromptArgument(
                    name="language",
                    description="Programming language of the code",
                    required=True
                ),
                types.PromptArgument(
                    name="focus",
                    description="Review focus area",
                    required=False
                )
            ]
        ),
        types.Prompt(
            name="project-planning",
            description="Help plan and structure a project",
            arguments=[
                types.PromptArgument(
                    name="projectType",
                    description="Type of project",
                    required=True
                ),
                types.PromptArgument(
                    name="requirements",
                    description="Project requirements and goals",
                    required=True
                ),
                types.PromptArgument(
                    name="timeline",
                    description="Expected timeline or deadline",
                    required=True
                ),
                types.PromptArgument(
                    name="teamSize",
                    description="Number of team members",
                    required=True
                )
            ]
        )
    ]


@server.get_prompt()
async def handle_get_prompt(name: str, arguments: dict) -> types.GetPromptResult:
    """Get a specific prompt with the given arguments."""
    
    if name == "explain-concept":
        concept = arguments.get("concept")
        audience = arguments.get("audience", "intermediate")
        
        return types.GetPromptResult(
            description=f"Explanation of {concept} for {audience} audience",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"""Please explain the concept of "{concept}" for a {audience} audience. Include:

1. A clear definition
2. Key characteristics or components
3. Real-world examples or use cases
4. Common misconceptions (if any)
5. Related concepts

Make the explanation accessible and engaging for the target audience level."""
                    )
                )
            ]
        )
    
    elif name == "code-review":
        code = arguments.get("code")
        language = arguments.get("language")
        focus = arguments.get("focus", "all")
        
        focus_areas = []
        if focus == "all" or focus == "security":
            focus_areas.append("- Security vulnerabilities or concerns")
        if focus == "all" or focus == "performance":
            focus_areas.append("- Performance optimizations")
        if focus == "all" or focus == "maintainability":
            focus_areas.append("- Code maintainability and readability")
        if focus == "all":
            focus_areas.extend([
                "- Best practices adherence",
                "- Potential bugs or issues"
            ])
        
        return types.GetPromptResult(
            description=f"Code review for {language} code with {focus} focus",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"""Please review this {language} code with a focus on {focus}:

```{language}
{code}
```

Provide feedback on:
{chr(10).join(focus_areas)}

Include specific recommendations for improvement."""
                    )
                )
            ]
        )
    
    elif name == "project-planning":
        project_type = arguments.get("projectType")
        requirements = arguments.get("requirements")
        timeline = arguments.get("timeline")
        team_size = arguments.get("teamSize")
        
        return types.GetPromptResult(
            description=f"Project planning for {project_type}",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"""Help me plan a {project_type} project with the following details:

**Requirements:** {requirements}
**Timeline:** {timeline}
**Team Size:** {team_size} members

Please provide:
1. Project breakdown and milestones
2. Technology stack recommendations
3. Team role suggestions
4. Risk assessment and mitigation strategies
5. Timeline estimates for key phases
6. Development methodology recommendations

Consider best practices for project management and delivery."""
                    )
                )
            ]
        )
    
    else:
        raise ValueError(f"Unknown prompt: {name}")


async def main():
    """Main function to run the MCP server."""
    try:
        # Run the server using stdio transport
        # Log a short startup message to stderr so it's visible when running manually.
        # This does not interfere with the MCP stdio transport because logging
        # writes to stderr while the protocol uses stdout.
        logger.info("Example MCP Server starting (stdio transport)")

        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="example-mcp-server",
                    server_version="1.0.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
