## Setup

1. Get Datadog MCP server running: https://github.com/winor30/mcp-server-datadog.git

2. Change into app directory:

```bash
cd app
```

3. Create your .env file:

```bash
cp .env.example .env
```

4. Create virtual environment:

```bash
python3 -m venv .venv
```

5. Start virtual environment:

```bash
source .venv/bin/activate
```

6. Install dependencies:

```bash
pip install google-adk
```

7. Run app:

```bash
adk web
```
