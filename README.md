# VReader

Turn YouTube videos into articles! I banged this one out in a couple of hours, so it's a bit scrappy. Will slowly improve it.

## Running Server

```bash
# Locally (See "Development" Section)
export OPENAI_API_KEY=`cat openai_key`

vreader server run

# Docker Quick Start
docker run \
    -p 5000:5000 \
    -e OPENAI_API_KEY=`cat openai_key` \
    -e DATA_PATH=/data
    -v ./data:/data \
    gitea.va.reichard.io/evan/vreader:latest
```

The server will now be accessible at `http://localhost:5000`

## Configuration

| Environment Variable | Default Value | Description                         |
| -------------------- | ------------- | ----------------------------------- |
| OPENAI_API_KEY       | NONE          | Required OpenAI API Key for ChatGPT |
| DATA_PATH            | NONE          | Where to store the data             |

# Development

```bash
# Initiate
python3 -m venv venv
. ./venv/bin/activate

# Local Development
pip install -e .

# Creds & Other Environment Variables
export OPENAI_API_KEY=`cat openai_key`

# Docker
make docker_build_local
```
