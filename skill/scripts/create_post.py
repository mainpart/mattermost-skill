#!/usr/bin/env python3
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import _client

params = _client.parse_params(sys.argv[1:])
channel_id = params.get("channel_id")
message = params.get("message")
if not channel_id or not message:
    _client.output_json({"error": "Provide --channel_id:X --message:X [--root_id:X] [--file_ids:X]"})
    sys.exit(1)
body = {"channel_id": channel_id, "message": message}
if params.get("root_id"):
    body["root_id"] = params["root_id"]
if params.get("file_ids"):
    fids = params["file_ids"]
    if isinstance(fids, str):
        fids = json.loads(fids)
    body["file_ids"] = fids
if params.get("props"):
    props = params["props"]
    if isinstance(props, str):
        props = json.loads(props)
    body["props"] = props
result = _client.post("/posts", body)
_client.output_json(result)
