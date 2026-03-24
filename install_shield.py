import json
import os
import platform
import sys
from pathlib import Path

def get_config_paths():
    home = Path.home()
    system = platform.system()
    
    paths = {
        "Claude Desktop": [],
        "Claude Code": [],
        "Gemini CLI": []
    }

    if system == "Darwin":  # macOS
        paths["Claude Desktop"] = [home / "Library/Application Support/Claude/claude_desktop_config.json"]
        paths["Claude Code"] = [home / ".claude/config.json"]
        paths["Gemini CLI"] = [home / ".gemini/settings.json"]
    elif system == "Windows":
        appdata = Path(os.environ.get("APPDATA", home / "AppData/Roaming"))
        paths["Claude Desktop"] = [appdata / "Claude/claude_desktop_config.json"]
        paths["Claude Code"] = [home / ".claude/config.json"]
        paths["Gemini CLI"] = [home / ".gemini/settings.json"]
    else:  # Linux and others
        paths["Claude Desktop"] = [home / ".config/Claude/claude_desktop_config.json"]
        paths["Claude Code"] = [home / ".claude/config.json"]
        paths["Gemini CLI"] = [home / ".gemini/settings.json"]
    
    return paths

def install_shield():
    print(f"--- VibeShield Installer (OS: {platform.system()}) ---")
    
    # Configuration to inject
    new_config = {
        "mcpServers": {
            "vibeshield": {
                "command": sys.executable,
                "args": [str(Path(__file__).resolve().parent / "server.py")],
                "env": {}
            }
        }
    }
    
    config_paths = get_config_paths()
    
    for client_name, file_paths in config_paths.items():
        for file_path in file_paths:
            if file_path.exists():
                try:
                    with open(file_path, 'r') as f:
                        config_data = json.load(f)
                except (json.JSONDecodeError, FileNotFoundError):
                    config_data = {}

                # Merge the config
                if "mcpServers" not in config_data:
                    config_data["mcpServers"] = {}
                
                config_data["mcpServers"]["vibeshield"] = new_config["mcpServers"]["vibeshield"]
                
                # Write back
                with open(file_path, 'w') as f:
                    json.dump(config_data, f, indent=2)
                
                print(f"✅ Successfully shielded {client_name} at {file_path}")
            else:
                # print(f"ℹ️  {client_name} config not found at {file_path}, skipping.")
                pass

if __name__ == "__main__":
    install_shield()
