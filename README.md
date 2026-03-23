# VibeShield MCP Server

VibeShield is an open-source MCP (Model Context Protocol) server built with FastMCP 3.0. It provides tools for automated code security auditing and secret detection.

## Features

- **Audit Code Security**: Uses `semgrep` to scan files or strings of code for security vulnerabilities. Returns concise reports with CWE IDs, Severity, and Suggested Fixes.
- **Check for Secrets**: Uses `trufflehog` to scan the current directory (git repository) for leaked API keys, credentials, and other sensitive information.
- **Health Check**: `get_engine_status` tool to verify the availability of local security engines.

## Prerequisites

- Python 3.10+
- `semgrep` binary installed (`pip install semgrep`)
- `trufflehog` binary installed (`pip install trufflehog`)

## Installation

```bash
pip install -r requirements.txt
```

## Universal Integration

VibeShield is designed to work across all major MCP-compatible clients. You can use the included `install_shield.py` script to automatically configure your clients, or add the configuration manually.

### Automated Setup
```bash
python install_shield.py
```

### Manual Configuration
Add the following block to your client's configuration file:

```json
{
  "mcpServers": {
    "vibeshield": {
      "command": "/home/samartha/vibe-shield/venv/bin/python",
      "args": ["/home/samartha/vibe-shield/server.py"],
      "env": {}
    }
  }
}
```

#### Config Locations:
- **Claude Desktop**: 
  - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
  - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- **Claude Code**: `~/.claude/config.json`
- **Gemini CLI**: `~/.gemini/settings.json`
- **Cursor**: Use the absolute path to `server.py` in the "MCP Servers" section of the Cursor settings.

## Usage

Start the server using stdio transport:

```bash
python server.py
```

## Tools

### `audit_code_security`
- `file_path` (optional): Path to a local file to scan.
- `code` (optional): A string of code to scan directly.

### `check_for_secrets`
- Scans the current directory (must be a git repository) for leaked secrets.

### `get_engine_status`
- Verifies if `semgrep` and `trufflehog` are properly installed and accessible.
