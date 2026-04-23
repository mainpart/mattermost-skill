#!/usr/bin/env python3
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import _client

params = _client.parse_params(sys.argv[1:])
user_ids = params.get("user_ids")
if not user_ids:
    _client.output_json({"error": 'Provide --user_ids:\'["id1","id2"]\' or via JSON arg'})
    sys.exit(1)
if isinstance(user_ids, str):
    user_ids = json.loads(user_ids)
if len(user_ids) >= 3:
    result = _client.post("/channels/group", user_ids)
else:
    result = _client.post("/channels/direct", user_ids)
_client.output_json(result)
