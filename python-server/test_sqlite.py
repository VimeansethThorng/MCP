#!/usr/bin/env python3
"""
SQLite Tool Test Script

This script demonstrates the SQLite functionality of the Python MCP server.
"""

import sys
import os
import asyncio
import json

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from server import handle_call_tool

async def test_sqlite_tool():
    """Test all SQLite tool functionality."""
    
    print("🗄️  Testing SQLite Tool Functionality")
    print("=" * 50)
    
    # Test 1: Initialize database
    print("\n1. Initializing database with sample data...")
    result = await handle_call_tool('sqlite-query', {
        'action': 'init',
        'database': 'demo.db',
        'query': 'CREATE SAMPLE DATABASE'
    })
    print("✅", result[0].text)
    
    # Test 2: Query users
    print("\n2. Querying users...")
    result = await handle_call_tool('sqlite-query', {
        'query': 'SELECT name, email, country FROM users ORDER BY name',
        'database': 'demo.db'
    })
    data = json.loads(result[0].text)
    print(f"✅ Found {data['rowCount']} users:")
    for user in data['data']:
        print(f"   - {user['name']} ({user['email']}) from {user['country']}")
    
    # Test 3: Query products by category
    print("\n3. Querying products in Electronics category...")
    result = await handle_call_tool('sqlite-query', {
        'query': "SELECT name, price FROM products WHERE category = 'Electronics' ORDER BY price DESC",
        'database': 'demo.db'
    })
    data = json.loads(result[0].text)
    print(f"✅ Found {data['rowCount']} electronics:")
    for product in data['data']:
        print(f"   - {product['name']}: ${product['price']}")
    
    # Test 4: Add new user
    print("\n4. Adding new user...")
    result = await handle_call_tool('sqlite-query', {
        'query': "INSERT INTO users (name, email, age, country) VALUES ('Test User', 'test@example.com', 25, 'JP')",
        'database': 'demo.db'
    })
    data = json.loads(result[0].text)
    print(f"✅ Inserted user with ID: {data['lastInsertId']}")
    
    # Test 5: Order statistics
    print("\n5. Getting order statistics...")
    result = await handle_call_tool('sqlite-query', {
        'query': "SELECT status, COUNT(*) as count, AVG(total) as avg_total FROM orders GROUP BY status ORDER BY count DESC",
        'database': 'demo.db'
    })
    data = json.loads(result[0].text)
    print(f"✅ Order statistics:")
    for stat in data['data']:
        print(f"   - {stat['status']}: {stat['count']} orders (avg: ${stat['avg_total']:.2f})")
    
    # Test 6: Join query
    print("\n6. Getting user orders with product details...")
    result = await handle_call_tool('sqlite-query', {
        'query': """
        SELECT u.name as user_name, p.name as product_name, o.quantity, o.total, o.status
        FROM orders o 
        JOIN users u ON o.user_id = u.id 
        JOIN products p ON o.product_id = p.id 
        ORDER BY o.total DESC
        LIMIT 3
        """,
        'database': 'demo.db'
    })
    data = json.loads(result[0].text)
    print(f"✅ Top {data['rowCount']} orders:")
    for order in data['data']:
        print(f"   - {order['user_name']} bought {order['quantity']}x {order['product_name']} for ${order['total']} ({order['status']})")
    
    print("\n" + "=" * 50)
    print("🎉 All SQLite tests completed successfully!")
    print("\n📝 Database file: demo.db")
    print("🔧 Available actions: query, init, drop")
    print("📊 Tables: users, products, orders")

if __name__ == "__main__":
    asyncio.run(test_sqlite_tool())
