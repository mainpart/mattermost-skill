#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import _client

params = _client.parse_params(sys.argv[1:])
file_id = params.get("file_id")
if not file_id:
    _client.output_json({"error": "Provide --file_id:X"})
    sys.exit(1)
result = _client.get(f"/files/{file_id}/info")
_client.output_json(result)
