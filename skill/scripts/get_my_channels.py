#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import _client

params = _client.parse_params(sys.argv[1:])
team_id = params.get("team_id") or _client.TEAM_ID
result = _client.get(f"/users/me/teams/{team_id}/channels")
_client.output_json(result)
