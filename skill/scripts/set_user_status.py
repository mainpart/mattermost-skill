#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import _client

params = _client.parse_params(sys.argv[1:])
user_id = params.get("user_id")
status = params.get("status")
if not user_id or not status:
    _client.output_json({"error": "Provide --user_id:X --status:online|away|dnd|offline"})
    sys.exit(1)
result = _client.put(f"/users/{user_id}/status", {"user_id": user_id, "status": status})
_client.output_json(result)
