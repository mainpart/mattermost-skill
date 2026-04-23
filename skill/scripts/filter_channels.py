#!/usr/bin/env python3
"""Filter channel(s) from stdin: extract compact fields."""
import json
import sys

FIELDS = ("id", "type", "display_name", "name", "header", "purpose", "team_id")


def compact(ch):
    return {k: ch[k] for k in FIELDS if ch.get(k)}


data = json.load(sys.stdin)
if isinstance(data, list):
    print(json.dumps([compact(c) for c in data], ensure_ascii=False, indent=2))
elif isinstance(data, dict):
    print(json.dumps(compact(data), ensure_ascii=False, indent=2))
else:
    print(json.dumps(data, ensure_ascii=False, indent=2))
