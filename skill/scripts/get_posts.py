#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import _client

params = _client.parse_params(sys.argv[1:])
channel_id = params.pop("channel_id", None)
if not channel_id:
    _client.output_json({"error": "Provide --channel_id:X"})
    sys.exit(1)
params.setdefault("page", 0)
params.setdefault("per_page", 60)
result = _client.get(f"/channels/{channel_id}/posts", params)
_client.output_json(result)
