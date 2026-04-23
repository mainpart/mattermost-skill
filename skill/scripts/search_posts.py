#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import _client

params = _client.parse_params(sys.argv[1:])
team_id = params.get("team_id") or _client.TEAM_ID
body = {
    "terms": params.get("terms", ""),
    "is_or_search": False,
    "page": params.get("page", 0),
    "per_page": params.get("per_page", 60),
}
result = _client.post(f"/teams/{team_id}/posts/search", body)
_client.output_json(result)
