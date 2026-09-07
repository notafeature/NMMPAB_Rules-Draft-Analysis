#!/usr/bin/env python3
"""Run tools/check-site.py for every Part that has pages. Non-zero exit if any fails."""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import partlib

rc = 0
for part in partlib.PARTS:
    print(f"== Part {part}")
    r = subprocess.run([sys.executable, os.path.join(HERE, "check-site.py"), "--part", part])
    rc = rc or r.returncode
sys.exit(rc)
