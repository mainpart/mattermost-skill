#!/usr/bin/env python3
import sys, os, json
import urllib.request
sys.path.insert(0, os.path.dirname(__file__))
import _client

params = _client.parse_params(sys.argv[1:])
channel_id = params.get("channel_id")
file_path = params.get("file_path")
if not channel_id or not file_path:
    _client.output_json({"error": "Provide --channel_id:X --file_path:X [--filename:X]"})
    sys.exit(1)

filename = params.get("filename") or os.path.basename(file_path)
file_path = os.path.abspath(file_path)

with open(file_path, "rb") as f:
    file_bytes = f.read()

# Multipart form upload via urllib
import uuid
boundary = uuid.uuid4().hex
body_parts = []
# channel_id field
body_parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"channel_id\"\r\n\r\n{channel_id}".encode())
# file field
body_parts.append(
    f"--{boundary}\r\nContent-Disposition: form-data; name=\"files\"; filename=\"{filename}\"\r\nContent-Type: application/octet-stream\r\n\r\n".encode()
    + file_bytes
)
body_parts.append(f"--{boundary}--\r\n".encode())
body_data = b"\r\n".join(body_parts)

req = urllib.request.Request(
    _client.BASE_URL + "/files",
    data=body_data,
    method="POST",
    headers={
        "Authorization": f"Bearer {_client.TOKEN}",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    },
)
try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        _client.output_json(json.loads(resp.read()))
except urllib.error.HTTPError as e:
    err = e.read().decode("utf-8", errors="replace")[:500]
    _client.output_json({"error": f"HTTP {e.code}", "detail": err})
    sys.exit(1)
