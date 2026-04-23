#!/usr/bin/env python3
"""Filter post list from stdin: extract compact fields, output to stdout."""
import json
import sys


def compact_post_list(data):
    if not isinstance(data, dict) or "order" not in data or "posts" not in data:
        return data
    posts = []
    for pid in data["order"]:
        p = data["posts"].get(pid, {})
        post = {
            "id": p.get("id"),
            "user_id": p.get("user_id"),
            "channel_id": p.get("channel_id"),
            "message": p.get("message"),
            "create_at": p.get("create_at"),
        }
        if p.get("root_id"):
            post["root_id"] = p["root_id"]
        if p.get("reply_count"):
            post["reply_count"] = p["reply_count"]
        meta_files = p.get("metadata", {}).get("files")
        if meta_files:
            post["files"] = [{k: f[k] for k in ("id", "name", "size") if k in f} for f in meta_files]
        elif p.get("file_ids"):
            post["file_ids"] = p["file_ids"]
        post = {k: v for k, v in post.items() if v is not None}
        posts.append(post)
    return {"posts": posts, "total": len(posts)}


data = json.load(sys.stdin)
print(json.dumps(compact_post_list(data), ensure_ascii=False, indent=2))
