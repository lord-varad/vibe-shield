# VibeShield MCP Server

VibeShield is an open-source MCP (Model Context Protocol) server that includes a **Silent Guardian** for invisible, background security. It provides automated code auditing and secret detection to ensure AI-generated output is safe before it reaches the user.

## Features

- **Silent Security**: VibeShield operates between the AI and the user. If insecure code is detected, it returns a `SYSTEM_RETRY` signal, forcing the AI to silently self-correct in the background. The user only sees the final, secure version.
- **Universal Compatibility**: The silent self-correction logic works across all MCP-compatible clients and CLIs, including **Claude Code**, **Gemini CLI**, **Cursor**, and **Claude Desktop**.
- **Visual Feedback**: A small `[✧]` symbol briefly appears in the terminal during background scans to show that the shield is active.

## Installation

### Automated Setup
The primary method for installation is the included automated script which configures Claude, Gemini, and Cursor automatically:
```bash
python install_shield.py
```

### Manual Configuration
Add the following block to your client's `mcpServers` configuration file:

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

## Tools

### `audit_code_security`
Audits code for vulnerabilities (SQL injection, XSS, etc.) and triggers a **Scan-and-Retry** loop. If issues are found, it instructs the AI to fix them silently.

### `check_for_secrets`
Scans for leaked API keys, credentials, and tokens using `trufflehog`.

### `show_shield_report`
Displays a professional security report in the terminal including:
- **Total Scans Conducted** vs. **Silent Fixes Applied**.

### `get_engine_status`
Verifies if `semgrep` and `trufflehog` are properly installed and accessible.

## Requirements

- Python 3.10+
- `semgrep` binary installed (`pip install semgrep`)
- `trufflehog` binary installed (`pip install trufflehog`)

## License
Licensed under the **Apache 2.0** License.
