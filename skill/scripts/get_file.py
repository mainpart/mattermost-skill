#!/usr/bin/env python3
import json
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
import _client

params = _client.parse_params(sys.argv[1:])
file_id = params.get("file_id")
if not file_id:
    _client.output_json({"error": "Provide --file_id:X"})
    sys.exit(1)

data = _client.get_raw(f"/files/{file_id}")
save_path = params.get("save_path")

if save_path:
    save_path = os.path.abspath(save_path)
    os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(data)
    _client.output_json({"saved": save_path, "size": len(data)})
else:
    try:
        print(data.decode("utf-8"))
    except UnicodeDecodeError:
        _client.output_json({"binary": True, "size": len(data), "hint": "Use --save_path:./file.ext to save"})
