#!/usr/bin/env python3
"""Hybrid channel search: public team channels + private channels user belongs to.

MM API POST /teams/{team_id}/channels/search returns only public (type=O) channels
for users with `list_team_channels`. Private channels (type=P) where the user is a
member are not returned. To cover them, additionally fetch
GET /users/me/teams/{team_id}/channels and filter locally by substring match on
`name` and `display_name`. Results merged and de-duplicated by id.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import _client

params = _client.parse_params(sys.argv[1:])
team_id = params.get("team_id") or _client.TEAM_ID
term = (params.get("term") or "").strip()

public = _client.post(f"/teams/{team_id}/channels/search", {"term": term})
if not isinstance(public, list):
    public = []

needle = term.lower()
mine = _client.get(f"/users/me/teams/{team_id}/channels") if needle else []
mine_matched = [
    c for c in (mine or [])
    if needle in (c.get("name") or "").lower()
    or needle in (c.get("display_name") or "").lower()
]

by_id = {c["id"]: c for c in public}
for c in mine_matched:
    by_id.setdefault(c["id"], c)

_client.output_json(list(by_id.values()))
