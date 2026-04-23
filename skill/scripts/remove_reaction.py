#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import _client

params = _client.parse_params(sys.argv[1:])
user_id = params.get("user_id")
post_id = params.get("post_id")
emoji_name = params.get("emoji_name")
if not user_id or not post_id or not emoji_name:
    _client.output_json({"error": "Provide --user_id:X --post_id:X --emoji_name:X"})
    sys.exit(1)
result = _client.delete(f"/users/{user_id}/posts/{post_id}/reactions/{emoji_name}")
_client.output_json(result)
