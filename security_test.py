import subprocess
import os

def insecure_execute(cmd):
    # DANGER: shell=True is vulnerable to command injection
    return subprocess.run(cmd, shell=True)

def safer_execute(cmd):
    import shlex
    return subprocess.run(shlex.split(cmd))
