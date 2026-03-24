# VibeShield MCP Server

VibeShield is an open-source MCP (Model Context Protocol) server that provides a **Silent Guardian** for invisible, background security. It ensures AI-generated code is audited and secure before it ever reaches the user.

## Features

- **Silent Security**: VibeShield operates between the AI and the user. If insecure code is detected, it returns a `SYSTEM_RETRY` signal, forcing the AI to silently self-correct. The user only sees the final, secure version.
- **Universal Compatibility**: Works across all MCP-compatible clients and CLIs, including **Claude Code**, **Gemini CLI**, **Cursor**, and **Claude Desktop**.
- **Visual Feedback**: A small `[✧]` symbol briefly appears in your terminal during scans, letting you know the shield is active.

## Installation

### Automated Setup
The primary installation method is the included automated script. It dynamically detects your Python path and project location to configure your clients (Claude, Gemini, Cursor) automatically:

```bash
python install_shield.py
```

### Manual Configuration
If you prefer manual setup, add the following block to your client's `mcpServers` configuration file:

```json
{
  "mcpServers": {
    "vibeshield": {
      "command": "/path/to/your/venv/bin/python",
      "args": ["/path/to/vibe-shield/server.py"]
    }
  }
}
```

## Tools

### `audit_code_security`
Audits code for vulnerabilities (SQL injection, XSS, etc.) and triggers a **Scan-and-Retry** loop for silent self-correction.

### `check_for_secrets`
Uses `trufflehog` to scan for leaked API keys, credentials, and tokens in your code and repository history.

### `show_shield_report`
Displays a real-time security report in the terminal, showing **Total Scans Conducted** versus **Silent Fixes Applied**.

### `get_engine_status`
Verifies that your local security engines (`semgrep` and `trufflehog`) are properly installed and ready.

## Examples & Testing
The `examples/` directory contains sample files for testing and demonstration:
- `insecure_sample.py`: Demonstrates code injection via `eval()`.
- `security_test.py`: Demonstrates command injection vulnerabilities.
- `secrets.example.txt`: A template for safe secret management.

> **WARNING:** Python files in the `examples/` folder are **intentionally insecure** and should only be used for testing VibeShield's capabilities. Never use these patterns in production code.

## Requirements
- **Python 3.10+**
- **semgrep**: `pip install semgrep`
- **trufflehog**: `pip install trufflehog`

## License
Licensed under the **Apache 2.0** License.
