<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# MCP Server Project

This is a complete Model Context Protocol (MCP) server available in both TypeScript and Python implementations that demonstrates all core MCP capabilities.

## Project Structure

### TypeScript Implementation
- **Language**: TypeScript
- **Runtime**: Node.js
- **Framework**: MCP TypeScript SDK
- **Main File**: `src/index.ts`
- **Transport**: stdio (Standard Input/Output)

### Python Implementation
- **Language**: Python 3.8+
- **Framework**: MCP Python SDK
- **Main File**: `src/server.py`
- **Transport**: stdio (Standard Input/Output)

## Features Implemented
✅ **Resources**: Static and dynamic data sources  
✅ **Tools**: Executable functions for LLM interactions (including MySQL query tool)
✅ **Prompts**: Reusable interaction templates  
✅ **Full MCP Compliance**: Complete protocol implementation in both languages

## Development Commands

### TypeScript:
- `npm run build` - Compile TypeScript to JavaScript
- `npm run dev` - Development mode with tsx
- `npm start` - Run the compiled server
- `npm run prepare` - Build project (runs automatically on install)

### Python:
- `python3 src/server.py` - Run the Python server
- `python3 test_server.py` - Run server tests
- `pip install -r requirements.txt` - Install Python dependencies

## Usage

### TypeScript:
1. Build the project: `npm run build`
2. Run the server: `npm start`

### Python:
1. Install dependencies: `pip install -r requirements.txt`
2. Run the server: `python3 src/server.py`

Both servers are ready to connect via MCP-compatible clients and have configuration available in `.vscode/mcp.json` for VS Code integration.

## SDK and Documentation References
- MCP GitHub Repository: https://github.com/modelcontextprotocol
- MCP TypeScript SDK: https://github.com/modelcontextprotocol/typescript-sdk
- MCP Python SDK: https://github.com/modelcontextprotocol/python-sdk
- MCP Documentation: https://modelcontextprotocol.io/

## Project Completion Status
- [x] Verify that the copilot-instructions.md file in the .github directory is created.
- [x] Clarify Project Requirements
- [x] Scaffold the Project
- [x] Customize the Project
- [x] Install Required Extensions
- [x] Compile the Project
- [x] Create and Run Task
- [x] Launch the Project
- [x] Ensure Documentation is Complete
