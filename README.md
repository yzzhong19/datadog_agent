# Google ADK Datadog Agent

## Description

Example agent implemented using Google ADK. This agent has access to Datadog via an MCP server.

## Setup

1. Get Datadog MCP server running: https://github.com/winor30/mcp-server-datadog.git

2. Create your .env file:

```bash
cp .env.example .env
```

3. Create virtual environment:

```bash
python3 -m venv .venv
```

4. Start virtual environment:

```bash
source .venv/bin/activate
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Change into app directory:

```bash
cd app
```

7. Run Google ADK web server:

```bash
adk web
```

8. Open the ADK web UI:

```bash
open http://localhost:8000
```

9. Ask the agent to fetch some Datadog logs!

Sample input:

```
Use the search logs tool to find recent logs for the service named “agi-house-hackathon-sample-server”
```
