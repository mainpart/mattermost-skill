#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import _client

params = _client.parse_params(sys.argv[1:])
if params.get("user_id"):
    result = _client.get(f"/users/{params['user_id']}")
elif params.get("username"):
    result = _client.get(f"/users/username/{params['username']}")
else:
    result = {"error": "Provide --user_id:X or --username:X"}
_client.output_json(result)
