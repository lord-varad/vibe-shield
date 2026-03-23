import json
import os
import subprocess
import tempfile
import shlex
from typing import Optional, List, Dict, Any
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("VibeShield")

def is_tool_available(name: str) -> bool:
    """Check if a tool is available in the system PATH."""
    try:
        subprocess.run([name, "--version" if name == "semgrep" else "--help"], 
                       capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

@mcp.tool()
def get_engine_status() -> Dict[str, Any]:
    """
    Health check tool to verify if security engines (semgrep, trufflehog) are installed.
    """
    return {
        "semgrep": "INSTALLED" if is_tool_available("semgrep") else "MISSING",
        "trufflehog": "INSTALLED" if is_tool_available("trufflehog") else "MISSING",
        "status": "READY" if is_tool_available("semgrep") and is_tool_available("trufflehog") else "DEGRADED"
    }

@mcp.tool()
def audit_code_security(file_path: Optional[str] = None, code: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Audits code security using local semgrep.
    Provide either a file_path to scan a local file or code as a string.
    Returns findings with 'CWE ID', 'Severity', and 'Suggested Fix'.
    """
    temp_file = None
    target = file_path

    try:
        if not is_tool_available("semgrep"):
            return [{"error": "semgrep binary not found. Please install it with 'pip install semgrep'."}]

        if code:
            temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
            temp_file.write(code)
            temp_file.close()
            target = temp_file.name
        
        if not target:
            return [{"error": "Either file_path or code must be provided."}]

        if not os.path.exists(target):
            return [{"error": f"Target path {target} does not exist."}]

        # Securely build command
        # Note: subprocess.run with a list of arguments is generally safe, 
        # but we ensure the target is handled correctly.
        cmd = ["semgrep", "scan", "--config", "auto", "--json", target]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode not in [0, 1]:
             return [{"error": f"Semgrep execution failed: {result.stderr or result.stdout}"}]

        data = json.loads(result.stdout)
        findings = []
        for res in data.get("results", []):
            extra = res.get("extra", {})
            metadata = extra.get("metadata", {})
            
            cwe_list = metadata.get("cwe", [])
            cwe_id = cwe_list[0] if cwe_list else "N/A"
            
            findings.append({
                "CWE ID": cwe_id,
                "Severity": extra.get("severity", "UNKNOWN"),
                "Suggested Fix": extra.get("message", "No suggested fix provided.")
            })
            
        return findings if findings else [{"message": "No security issues found."}]

    except Exception as e:
        return [{"error": f"Unexpected error during audit: {str(e)}"}]
    finally:
        if temp_file and os.path.exists(temp_file.name):
            os.unlink(temp_file.name)

@mcp.tool()
def check_for_secrets() -> List[Dict[str, Any]]:
    """
    Scans the current directory for leaked API keys or credentials using trufflehog.
    Wraps trufflehog to identify secrets in the local git history or files.
    """
    try:
        if not is_tool_available("trufflehog"):
            return [{"error": "trufflehog not found. Please install it with 'pip install trufflehog'."}]

        # Run trufflehog on the current directory safely
        cmd = ["trufflehog", "--json", "--repo_path", ".", "."]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        findings = []
        if result.stdout:
            for line in result.stdout.strip().split('\n'):
                if not line.strip(): continue
                try:
                    findings.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        
        if not findings:
            if result.stderr and "InvalidGitRepositoryError" in result.stderr:
                return [{"error": "The current directory is not a git repository. Trufflehog requires a git repo."}]
            return [{"message": "No secrets found or scan failed.", "details": result.stderr[:200] if result.stderr else "None"}]
            
        return findings

    except Exception as e:
        return [{"error": f"Unexpected error during secret scan: {str(e)}"}]

if __name__ == "__main__":
    mcp.run()
