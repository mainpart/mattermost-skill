#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import _client

params = _client.parse_params(sys.argv[1:])
team_id = params.pop("team_id", None) or _client.TEAM_ID
params.setdefault("page", 0)
params.setdefault("per_page", 60)
result = _client.get(f"/teams/{team_id}/channels", params)
_client.output_json(result)
