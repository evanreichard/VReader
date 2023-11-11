<p><img align="center" src="https://gitea.va.reichard.io/evan/VReader/raw/branch/master/banner.png"></p>

<p align="center">
    <a href="https://drone.va.reichard.io/evan/VReader" target="_blank">
        <img src="https://drone.va.reichard.io/api/badges/evan/VReader/status.svg">
    </a>
</p>

---

VReader allows you to take videos from YouTube and convert them into articles!

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
