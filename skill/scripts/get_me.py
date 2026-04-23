#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import _client

result = _client.get("/users/me")
_client.output_json(result)
