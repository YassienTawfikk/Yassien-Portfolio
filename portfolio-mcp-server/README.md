# Yassien Portfolio MCP Server

Read-only MCP server exposing Yassien Tawfik's portfolio data as standardized Resources, plus one safe read Tool for project lookup.

This is not a chatbot, not a frontend, and not an action system. It is the service-provider side of MCP.

## Exposed Resources

- `portfolio://bio` - high-level profile, goals, links, and MSc admission context
- `portfolio://projects` - project catalog with stable IDs, descriptions, stack, highlights, and links
- `portfolio://skills` - skills grouped by category, including evidence project IDs
- `portfolio://education` - education, GPA, key coursework, MSc admission, and credentials

## Exposed Tool

### `get_project_details(id)`

Read-only lookup for one project by stable ID.

Example IDs:

- `neuropathx`
- `breastcancer-xai-evaluation`
- `pulsespy`
- `image-ft-mixer-pro`
- `lifestream`

The tool does not mutate files, call external APIs, send messages, or perform any side effects.

## Requirements

- Python 3.11+
- `mcp>=1.0.0`

## Install

Using the dedicated project venv:

```bash
python3.11 -m venv /Users/yassientawfik/portfolio-mcp-server/.venv
/Users/yassientawfik/portfolio-mcp-server/.venv/bin/python -m pip install mcp
```

## Run Locally

```bash
/Users/yassientawfik/portfolio-mcp-server/.venv/bin/python server.py
```

Most MCP clients launch stdio servers themselves, so you usually do not run this manually except for smoke testing.

## Claude Desktop Setup

Add the server to your Claude Desktop MCP config using the absolute path to `server.py`.

macOS config path:

```text
~/Library/Application Support/Claude/claude_desktop_config.json
```

Example:

```json
{
  "mcpServers": {
    "yassien-portfolio": {
      "command": "/Users/yassientawfik/portfolio-mcp-server/.venv/bin/python",
      "args": [
        "/Users/yassientawfik/Documents/Projects/Software Dev/Portfolio Website/portfolio-mcp-server/server.py"
      ]
    }
  }
}
```

Restart Claude Desktop after editing the config.

## Local Validation

After connecting from an MCP client, verify discovery includes:

```text
portfolio://bio
portfolio://projects
portfolio://skills
portfolio://education
```

Then call:

```text
get_project_details(id="neuropathx")
```

Expected result: the full NeuroPathX project object.

For more manual checks, see `tests/sample_queries.md`.

## Design Constraints

- Read-only Resources
- Read-only Tool only
- Local JSON data source
- No database
- No backend app server
- No contact form or email tools
- No action tools
- No frontend
