#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import _client

params = _client.parse_params(sys.argv[1:])
channel_name = params.get("channel_name")
if not channel_name:
    _client.output_json({"error": "Provide --channel_name:X"})
    sys.exit(1)
team_id = params.get("team_id") or _client.TEAM_ID
result = _client.get(f"/teams/{team_id}/channels/name/{channel_name}")
_client.output_json(result)
