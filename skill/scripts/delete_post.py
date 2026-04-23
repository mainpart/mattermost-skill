#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import _client

params = _client.parse_params(sys.argv[1:])
post_id = params.get("post_id")
if not post_id:
    _client.output_json({"error": "Provide --post_id:X"})
    sys.exit(1)
result = _client.delete(f"/posts/{post_id}")
_client.output_json(result)
