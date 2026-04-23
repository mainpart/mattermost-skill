#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import _client

params = _client.parse_params(sys.argv[1:])
body = {"term": params.get("term", ""), "limit": params.get("limit", 100)}
if params.get("team_id"):
    body["team_id"] = params["team_id"]
result = _client.post("/users/search", body)
_client.output_json(result)
