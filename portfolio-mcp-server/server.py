"""Read-only MCP server for Yassien Tawfik's portfolio data."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def _get_port() -> int:
    return int(os.environ.get("PORT", "8000"))


mcp = FastMCP("yassien-portfolio", host="0.0.0.0", port=_get_port())


def _load_json(filename: str) -> dict[str, Any]:
    path = DATA_DIR / filename
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _json_response(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2)


@mcp.resource("portfolio://bio")
def read_bio() -> str:
    """Return Yassien Tawfik's high-level profile and links."""
    return _json_response(_load_json("bio.json"))


@mcp.resource("portfolio://projects")
def read_projects() -> str:
    """Return Yassien Tawfik's portfolio project catalog."""
    return _json_response(_load_json("projects.json"))


@mcp.resource("portfolio://skills")
def read_skills() -> str:
    """Return Yassien Tawfik's skills grouped by category."""
    return _json_response(_load_json("skills.json"))


@mcp.resource("portfolio://education")
def read_education() -> str:
    """Return Yassien Tawfik's education, MSc admission, and credentials."""
    return _json_response(_load_json("education.json"))


@mcp.tool()
def get_project_details(id: str) -> str:
    """Return the full project object for a stable project ID."""
    projects = _load_json("projects.json").get("projects", [])
    for project in projects:
        if project.get("id") == id:
            return _json_response(project)

    return _json_response(
        {
            "error": "project_not_found",
            "message": f"No project found with id '{id}'.",
            "available_ids": [project.get("id") for project in projects],
        }
    )


def main() -> None:
    transport = os.environ.get("MCP_TRANSPORT", "stdio").lower()
    if transport == "http":
        mcp.run(transport="sse")
        return

    mcp.run()


if __name__ == "__main__":
    main()
