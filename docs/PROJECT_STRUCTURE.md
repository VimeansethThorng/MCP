# MCP Server Project Structure

This project contains two complete implementations of a Model Context Protocol (MCP) server:

## 📁 Project Layout

```
MCP/
├── 🟦 typescript-server/        # Complete TypeScript implementation
│   ├── src/
│   │   └── index.ts            # Main TypeScript server
│   ├── build/                  # Compiled JavaScript output
│   ├── node_modules/           # Node.js dependencies
│   ├── package.json            # NPM configuration
│   ├── package-lock.json       # Dependency lock file
│   ├── tsconfig.json           # TypeScript configuration
│   └── README.md               # TypeScript setup guide
│
├── 🐍 python-server/           # Complete Python implementation  
│   ├── src/
│   │   ├── __init__.py         # Python package init
│   │   └── server.py           # Main Python server
│   ├── .venv/                  # Python virtual environment
│   ├── requirements.txt        # Python dependencies
│   ├── setup.py               # Python setup script
│   ├── pyproject.toml         # Modern Python packaging
│   ├── test_server.py         # Python test suite
│   ├── PYTHON_SERVER.md       # Python documentation
│   ├── MYSQL_TOOL.md          # MySQL tool documentation
│   └── README.md              # Python setup guide
│
├── .vscode/
│   └── mcp.json               # VS Code MCP configuration for both servers
├── .github/
│   └── copilot-instructions.md # GitHub Copilot instructions
├── .gitignore                 # Git ignore file (covers both languages)
├── README.md                  # Main project documentation
└── MIGRATION_SUMMARY.md       # TypeScript to Python migration notes
```

## 🚀 Quick Start

### TypeScript Server
```bash
cd typescript-server
npm install
npm run build
npm start
```

### Python Server
```bash
cd python-server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 src/server.py
```

## 🔧 VS Code Integration

Both servers are pre-configured in `.vscode/mcp.json`:
- **TypeScript**: `example-mcp-server-ts`
- **Python**: `example-mcp-server-python`

## ✨ Features (Both Implementations)

- **4 Tools**: Calculator, System Info, Data Generator, MySQL Query
- **2 Resources**: Static README, Dynamic User Profiles
- **3 Prompts**: Concept Explanation, Code Review, Project Planning
- **Full MCP Compliance**: Both servers implement the complete MCP protocol
- **Security**: MySQL queries restricted to SELECT only
- **Error Handling**: Comprehensive error management
- **Transport**: stdio for direct client communication

## 📝 Documentation

- **Main README**: Project overview and setup (this level)
- **TypeScript README**: TypeScript-specific setup and usage
- **Python README**: Python-specific setup and usage
- **Migration Summary**: Notes on TypeScript to Python conversion
- **Python Server Docs**: Detailed Python implementation guide
- **MySQL Tool Docs**: MySQL functionality documentation

Both implementations are functionally identical and can be used interchangeably with any MCP-compatible client!
