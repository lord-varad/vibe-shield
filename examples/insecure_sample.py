# WARNING: This file is INTENTIONALLY insecure for demonstration and testing purposes only.
# NEVER use this pattern in production code.
# The code below is vulnerable to code injection via eval().

import sys

if len(sys.argv) > 1:
    path = sys.argv[1]
    eval(path)
