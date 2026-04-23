#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import _client

params = _client.parse_params(sys.argv[1:])
channel_id = params.get("channel_id")
if not channel_id:
    _client.output_json({"error": "Provide --channel_id:X"})
    sys.exit(1)
result = _client.get(f"/users/me/channels/{channel_id}/posts/unread")
_client.output_json(result)
