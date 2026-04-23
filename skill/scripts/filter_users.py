#!/usr/bin/env python3
"""Filter user(s) from stdin: extract compact fields."""
import json
import sys

FIELDS = ("id", "username", "first_name", "last_name", "nickname", "email", "position", "roles")


def compact(user):
    return {k: user[k] for k in FIELDS if user.get(k)}


data = json.load(sys.stdin)
if isinstance(data, list):
    print(json.dumps([compact(u) for u in data], ensure_ascii=False, indent=2))
elif isinstance(data, dict):
    print(json.dumps(compact(data), ensure_ascii=False, indent=2))
else:
    print(json.dumps(data, ensure_ascii=False, indent=2))
