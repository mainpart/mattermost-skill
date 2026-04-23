#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import _client

params = _client.parse_params(sys.argv[1:])
user_id = params.get("user_id")
if not user_id:
    _client.output_json({"error": "Provide --user_id:X"})
    sys.exit(1)
result = _client.get(f"/users/{user_id}/status")
_client.output_json(result)
