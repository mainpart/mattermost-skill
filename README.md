# Mattermost Agent for Claude Code

Claude Code skill for searching and extracting information from Mattermost via REST API v4.

## Features

- 30+ Python scripts covering users, channels, posts, threads, reactions, files
- Pipe-friendly filters for compact output
- Research strategies for deep investigation across conversations
- Zero external dependencies — pure Python stdlib

## Installation

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/mattermost-agent.git
cd mattermost-agent

# Create config
cp .env.example skill/scripts/.env
# Edit skill/scripts/.env with your Mattermost URL, token, and team ID

# Symlink into Claude Code skills
ln -s "$(pwd)/skill" ~/.claude/skills/mattermost-agent
```

The `.env` file is searched in order: `skill/scripts/` → `skill/` → project working directory. 
Alternatively, set environment variables `MATTERMOST_URL`, `MATTERMOST_TOKEN`, `MATTERMOST_TEAM_ID`.

## Structure

```
├── .env.example          # Config template
├── README.md
└── skill/                # Symlinked to ~/.claude/skills/mattermost-agent
    ├── SKILL.md          # API reference: scripts, parameters, examples
    ├── STRATEGY.md       # Research strategies and task templates
    └── scripts/
        ├── _client.py    # Shared HTTP client
        ├── get_posts.py
        ├── search_posts.py
        ├── filter_posts.py
        └── ...
```

## Usage

The skill is invoked automatically by Claude Code when you ask it to search or interact with Mattermost. You can also call scripts directly:

```bash
cd skill/scripts

# Search posts
python search_posts.py --terms:"deployment issue" | python filter_posts.py

# Get a thread
python get_post_thread.py --post_id:abc123 | python filter_thread.py

# Find a user
python search_users.py --term:john | python filter_users.py
```

Parameters can be passed as `--key:value` pairs or as a JSON object.

## Configuration

You need three values for `.env`: `MATTERMOST_URL`, `MATTERMOST_TOKEN`, and `MATTERMOST_TEAM_ID`.

Replace `https://mm.example.com` with your Mattermost server URL in all commands below.

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
  -d '{"description":"claude-code"}' \
  "https://mm.example.com/api/v4/users/$USER_ID/tokens"
```

### Get team ID

```bash
# List teams
curl -s -H "Authorization: Bearer $TOKEN" https://mm.example.com/api/v4/users/me/teams
```


## License

MIT
