#!/usr/bin/env python3
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import _client

params = _client.parse_params(sys.argv[1:])
post_id = params.get("post_id")
if not post_id:
    _client.output_json({"error": "Provide --post_id:X [--message:X] [--file_ids:X] [--props:X]"})
    sys.exit(1)
body = {}
if params.get("message"):
    body["message"] = params["message"]
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
if not body:
    _client.output_json({"error": "No fields to update"})
    sys.exit(1)
result = _client.put(f"/posts/{post_id}/patch", body)
_client.output_json(result)
