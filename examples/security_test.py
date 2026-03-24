# WARNING: This file is INTENTIONALLY insecure for demonstration and testing purposes only.
# NEVER use this pattern in production code.
# The code below is vulnerable to command injection.

import subprocess
import os

def insecure_execute(cmd):
    # DANGER: shell=True is vulnerable to command injection
    return subprocess.run(cmd, shell=True)

def safer_execute(cmd):
    import shlex
    return subprocess.run(shlex.split(cmd))
