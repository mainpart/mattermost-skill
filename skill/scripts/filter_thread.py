#!/usr/bin/env python3
"""Filter thread from stdin: hoist channel_id/root_id, strip duplicates."""
import json
import sys


def compact_thread(data):
    if not isinstance(data, dict) or "order" not in data or "posts" not in data:
        return data
    posts = []
    for pid in data["order"]:
        p = data["posts"].get(pid, {})
        post = {
            "id": p.get("id"),
            "user_id": p.get("user_id"),
            "message": p.get("message"),
            "create_at": p.get("create_at"),
        }
        if p.get("reply_count"):
            post["reply_count"] = p["reply_count"]
        meta_files = p.get("metadata", {}).get("files")
        if meta_files:
            post["files"] = [{k: f[k] for k in ("id", "name", "size") if k in f} for f in meta_files]
        elif p.get("file_ids"):
            post["file_ids"] = p["file_ids"]
        post = {k: v for k, v in post.items() if v is not None}
        posts.append(post)

    channel_id = None
    root_id = None
    if posts:
        root = data["posts"].get(data["order"][0], {})
        channel_id = root.get("channel_id")
        root_id = root.get("id")

    return {"channel_id": channel_id, "root_id": root_id, "posts": posts, "total": len(posts)}


data = json.load(sys.stdin)
print(json.dumps(compact_thread(data), ensure_ascii=False, indent=2))
