"""Shared HTTP client for Mattermost API scripts.

Loads .env from the script directory, parses CLI params, provides get/post helpers.
"""

import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error


def _load_env():
    """Load first .env found: scripts dir → skill dir → project cwd."""
    scripts_dir = os.path.dirname(os.path.abspath(__file__))

    for d in (scripts_dir, os.path.dirname(scripts_dir), os.getcwd()):
        path = os.path.join(d, ".env")
        if not os.path.exists(path):
            continue
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    os.environ.setdefault(k.strip(), v.strip())
        return


_load_env()

_REQUIRED = ("MATTERMOST_URL", "MATTERMOST_TOKEN", "MATTERMOST_TEAM_ID")
_missing = [k for k in _REQUIRED if not os.environ.get(k)]
if _missing:
    print(json.dumps({
        "error": f"Missing config: {', '.join(_missing)}",
        "hint": "Put .env in scripts/, skill/, or project dir, or set env vars",
    }), file=sys.stderr)
    sys.exit(1)

BASE_URL = os.environ["MATTERMOST_URL"].rstrip("/") + "/api/v4"
TOKEN = os.environ["MATTERMOST_TOKEN"]
TEAM_ID = os.environ["MATTERMOST_TEAM_ID"]


def parse_params(argv: list[str]) -> dict:
    """Parse CLI arguments into a dict.

    Supports two forms:
      1. JSON object as first arg: '{"channel_id":"abc","per_page":30}'
      2. --key:value pairs: --channel_id:abc --per_page:30
    """
    if not argv:
        return {}
    if argv[0].startswith("{"):
        return json.loads(argv[0])
    params = {}
    for arg in argv:
        if not arg.startswith("--") or ":" not in arg:
            continue
        key, _, value = arg[2:].partition(":")
        # Auto-cast integers
        try:
            value = int(value)
        except (ValueError, TypeError):
            pass
        params[key] = value
    return params


def get(path: str, params: dict | None = None) -> dict | list:
    """HTTP GET request. params go to query string."""
    url = BASE_URL + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        print(json.dumps({"error": f"HTTP {e.code}", "detail": body}), file=sys.stderr)
        sys.exit(1)


def post(path: str, json_data: dict | list) -> dict | list:
    """HTTP POST request. json_data goes to JSON body."""
    url = BASE_URL + path
    data = json.dumps(json_data).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST", headers={
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        print(json.dumps({"error": f"HTTP {e.code}", "detail": body}), file=sys.stderr)
        sys.exit(1)


def put(path: str, json_data: dict) -> dict | list:
    """HTTP PUT request. json_data goes to JSON body."""
    url = BASE_URL + path
    data = json.dumps(json_data).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="PUT", headers={
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read()
            return json.loads(body) if body else {"ok": True}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        print(json.dumps({"error": f"HTTP {e.code}", "detail": body}), file=sys.stderr)
        sys.exit(1)


def delete(path: str) -> dict:
    """HTTP DELETE request."""
    url = BASE_URL + path
    req = urllib.request.Request(url, method="DELETE", headers={
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read()
            return json.loads(body) if body else {"ok": True}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        print(json.dumps({"error": f"HTTP {e.code}", "detail": body}), file=sys.stderr)
        sys.exit(1)


def get_raw(path: str) -> bytes:
    """HTTP GET returning raw bytes."""
    url = BASE_URL + path
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {TOKEN}",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        print(json.dumps({"error": f"HTTP {e.code}", "detail": body}), file=sys.stderr)
        sys.exit(1)


def output_json(data):
    """Pretty-print JSON to stdout."""
    print(json.dumps(data, ensure_ascii=False, indent=2))
