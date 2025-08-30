#!/usr/bin/env python3

"""
Test script for the MCP Python server
"""

import asyncio
import json
import sys
from typing import Any, Dict

async def test_server():
    """Test the server by importing and checking basic functionality."""
    try:
        # Import the server module
        sys.path.insert(0, '/Users/vimeanseththorng/Documents/MCP/python-server/src')
        from server import server, handle_list_tools, handle_call_tool, handle_list_resources, handle_list_prompts
        
        print("✅ Server module imported successfully")
        print("✅ Server instance created")
        
        # Test tool registration
        tools_result = await handle_list_tools()
        print(f"✅ Found {len(tools_result)} tools:")
        for tool in tools_result:
            print(f"   - {tool.name}: {tool.description}")
        
        # Test resource registration
        resources_result = await handle_list_resources()
        print(f"✅ Found {len(resources_result)} resources:")
        for resource in resources_result:
            print(f"   - {resource.name}: {resource.description}")
        
        # Test prompt registration
        prompts_result = await handle_list_prompts()
        print(f"✅ Found {len(prompts_result)} prompts:")
        for prompt in prompts_result:
            print(f"   - {prompt.name}: {prompt.description}")
        
        # Test a simple tool call
        calc_result = await handle_call_tool("calculate", {
            "operation": "add",
            "a": 5,
            "b": 3
        })
        print(f"✅ Calculator test: {calc_result[0].text}")
        
        print("\n🎉 All tests passed! The Python MCP server is working correctly.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_server())
    sys.exit(0 if success else 1)
