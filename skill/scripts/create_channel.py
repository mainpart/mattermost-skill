#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import _client

params = _client.parse_params(sys.argv[1:])
display_name = params.get("display_name")
name = params.get("name")
if not display_name or not name:
    _client.output_json({"error": "Provide --display_name:X --name:X [--type:O|P] [--purpose:X] [--header:X]"})
    sys.exit(1)
team_id = params.get("team_id") or _client.TEAM_ID
body = {"team_id": team_id, "name": name, "display_name": display_name, "type": params.get("type", "O")}
if params.get("purpose"):
    body["purpose"] = params["purpose"]
if params.get("header"):
    body["header"] = params["header"]
result = _client.post("/channels", body)
_client.output_json(result)
