# Mattermost Skill

Portable skill for searching and extracting information from Mattermost via REST API v4. Works with Claude Code and Cursor from a single source of truth.

## Features

- 30+ Python scripts covering users, channels, posts, threads, reactions, files
- Pipe-friendly filters for compact output
- Research strategies for deep investigation across conversations
- Zero external dependencies — pure Python stdlib
- One skill body (`skill/SKILL.md`), mounted into each harness via symlink

## Structure

```
├── .env.example                      # Config template
├── README.md
├── cursor/
│   └── mattermost-skill.mdc          → symlink to ../skill/SKILL.md
└── skill/                            # Source of truth — mount via symlink
    ├── SKILL.md                      # Skill body: API reference, scripts, examples
    ├── references/
    │   └── STRATEGY.md               # Research strategies and task templates
    └── scripts/
        ├── _client.py                # Shared HTTP client
        ├── get_posts.py
        ├── search_posts.py
        ├── filter_posts.py
        └── ...
```

The frontmatter of `skill/SKILL.md` includes fields for both Claude Code (`name`, `allowed-tools`) and Cursor (`globs`, `alwaysApply`). Each harness reads what it understands and ignores the rest.

## Installation

```bash
git clone https://github.com/mainpart/mattermost-skill.git
cd mattermost-skill
cp .env.example skill/scripts/.env
# Edit skill/scripts/.env with MATTERMOST_URL, MATTERMOST_TOKEN, MATTERMOST_TEAM_ID
```

### Mount in Claude Code

```bash
ln -s "$(pwd)/skill" ~/.claude/skills/mattermost-skill
```

Claude Code auto-discovers it on the next session. Check: type `/skills` in Claude Code — `mattermost` should be listed.

### Mount in Cursor

Symlink the `.mdc` into your project's Cursor rules folder:

```bash
# from inside your Cursor project root
mkdir -p .cursor/rules
ln -s ~/Projects/mattermost-skill/cursor/mattermost-skill.mdc .cursor/rules/
```

This creates a symlink-to-symlink chain (`.cursor/rules/mattermost-skill.mdc` → repo's `cursor/mattermost-skill.mdc` → `skill/SKILL.md`). The OS resolves the chain transparently; editing `skill/SKILL.md` updates every mounted rule automatically.

**Don't use `cp -P`** — it copies the symlink verbatim, but the original is a relative link (`../skill/SKILL.md`), and a relative link inside `.cursor/rules/` resolves to the wrong place and breaks. If you need a standalone copy (e.g. to commit into a project without symlinks), use `cp -L` to dereference:

```bash
cp -L ~/Projects/mattermost-skill/cursor/mattermost-skill.mdc .cursor/rules/
```

Alternative — mount the whole skill folder as a Cursor skill (experimental, sometimes flaky on Remote SSH):

```bash
ln -s ~/Projects/mattermost-skill/skill .cursor/skills/mattermost-skill
```

### Mount in Claude Desktop

Same path as Claude Code — `~/.claude/skills/`. If you've already done the Claude Code mount, Claude Desktop picks it up too.

## Running scripts

Inside any harness, the agent runs scripts from the skill's own directory. Manually:

```bash
cd ~/Projects/mattermost-skill/skill/scripts

# Search posts
python search_posts.py --terms:"deployment issue" | python filter_posts.py

# Get a thread
python get_post_thread.py --post_id:abc123 | python filter_thread.py

# Find a user
python search_users.py --term:john | python filter_users.py
```

Parameters accept both `--key:value` pairs and a JSON object: `python get_posts.py '{"channel_id":"abc123","per_page":30}'`.

`.env` is loaded from `skill/scripts/.env` → `skill/.env` → current working directory, in that order. Alternatively, export `MATTERMOST_URL`, `MATTERMOST_TOKEN`, `MATTERMOST_TEAM_ID` in your shell.

## Configuration

You need three values in `.env`: `MATTERMOST_URL`, `MATTERMOST_TOKEN`, `MATTERMOST_TEAM_ID`.

Replace `https://mm.example.com` below with your Mattermost server URL.

### Option A: Personal Access Token

**Profile → Security → Personal Access Tokens** → create → copy to `.env`.

### Option B: Via API

```bash
# Login → session token is in the Token: response header
curl -si -X POST https://mm.example.com/api/v4/users/login \
  -H 'Content-Type: application/json' \
  -d '{"login_id":"username","password":"password"}'

# Create a PAT
curl -s -X POST -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"description":"mattermost-skill"}' \
  "https://mm.example.com/api/v4/users/$USER_ID/tokens"
```

### Get team ID

```bash
curl -s -H "Authorization: Bearer $TOKEN" https://mm.example.com/api/v4/users/me/teams
```

## Updating

The skill body is edited in one place: `skill/SKILL.md`. Every mounted location (Claude Code, Cursor, Desktop) follows the symlink, so `git pull` in the repo propagates changes everywhere.

## License

MIT
