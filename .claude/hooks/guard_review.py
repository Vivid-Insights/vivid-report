#!/usr/bin/env python3
"""PreToolUse hook: keep the agent out of the reviewers' files.

Reviews and approvals are written by people on the Vivid Insights team, never by the agent
(REVIEW.md). This blocks the agent's file tools from writing in review/*/reviews/ or
review/*/approvals/, and its shell from changing them or running the reviewer commands of
review.py. Reading them is allowed. Exit code 2 blocks the call and shows the reason to the agent.
"""
import json
import re
import sys

PROTECTED = re.compile(r"review/(round-[^/\s\"']+/)?(reviews|approvals)(/|\b)")
REVIEWER_CMDS = re.compile(r"review\.py[\"']?\s+(form|approve)\b")
READ_ONLY = re.compile(r"^\s*(cat|less|head|tail|ls|wc|grep|rg|find|git\s+(log|diff|show|status|blame))\b")
WRITE_OPS = re.compile(r"(>|\btee\b|\bmv\b|\bcp\b|\brm\b|\btouch\b|\bsed\s+-i|\bperl\s+-i|\bpython|\bgit\s+(add|commit|rm|mv|checkout|restore|reset))")

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)
tool = data.get("tool_name", "")
inp = data.get("tool_input", {}) or {}

def block(why):
    print(f"Blocked by the Vivid review guard: {why} Reviews and approvals are written by the reviewers "
          "themselves (REVIEW.md, instructions.md step 9). Tell the user what you were trying to do instead.",
          file=sys.stderr)
    sys.exit(2)

if tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
    path = str(inp.get("file_path") or inp.get("notebook_path") or "")
    if PROTECTED.search(path.replace("\\", "/")):
        block(f"the agent may not write {path}.")
elif tool == "Bash":
    cmd = str(inp.get("command", ""))
    if REVIEWER_CMDS.search(cmd):
        block("`review.py form` and `review.py approve` are for reviewers to run in their own terminal.")
    if re.search(r"review/(round-[^/\s]+/)?(reviews|approvals)", cmd):
        segments = re.split(r"&&|\|\||;|\|", cmd)
        for seg in segments:
            if re.search(r"(reviews|approvals)", seg) and (WRITE_OPS.search(seg) or not READ_ONLY.search(seg)):
                block("this command would change a review or an approval.")
sys.exit(0)
