#!/usr/bin/env python3
"""Build the Claude directory edition of PARASITER from this repo.

The full edition (branch main, installed from GitHub) keeps the local DataForSEO / SerpApi
runners (mcp/*.py, stdio servers). Anthropic's directory runs no local commands for
organizations that are not Verified, so the directory edition:

  * drops the two stdio servers, mcp/, tools/ and .github/;
  * connects the official hosted MCP servers instead — SerpApi (https://mcp.serpapi.com/mcp,
    Bearer key) and DataForSEO (https://mcp.dataforseo.com/mcp, Basic token) — with the
    user's own credentials from the plugin settings (sensitive userConfig options);
  * keeps every skill, agent and script: position checks run through those servers and the
    results go into the journal with worklog.py import-ranks
    (skills/work-log/references/directory-edition.md).

Usage: python3 tools/build_directory_edition.py OUT_DIR
"""
import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {".git", ".github", "mcp", "tools", ".gitignore"}

MCP = {
    "mcpServers": {
        "parasiter": {
            "type": "http",
            "url": "https://parasiter.affiliatecredo.com/mcp",
            "headers": {"Authorization": "Bearer ${user_config.parasiter_key}"},
        },
        "parasiter-dataforseo": {
            "type": "http",
            "url": "https://mcp.dataforseo.com/mcp",
            "headers": {"Authorization": "Basic ${user_config.dataforseo_token}"},
        },
        "parasiter-serpapi": {
            "type": "http",
            "url": "https://mcp.serpapi.com/mcp",
            "headers": {"Authorization": "Bearer ${user_config.serpapi_key}"},
        },
    }
}

DFS_TOKEN = {
    "type": "string",
    "title": "DataForSEO API token (optional)",
    "description": (
        "Your own DataForSEO account for position checks (pay per request, cost shown before every run). "
        "The token is your API login and API password (app.dataforseo.com → API Access, not the website password) "
        "joined by a colon and Base64-encoded. Make it on your own computer — Windows PowerShell: "
        "[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes('LOGIN:PASSWORD')) · Mac/Linux terminal: "
        "printf 'LOGIN:PASSWORD' | base64 — and paste the result here. Stored in secure storage and sent only to "
        "DataForSEO's official MCP server — never to the PARASITER server or the chat. Leave empty if you don't use DataForSEO."
    ),
    "required": False,
    "sensitive": True,
}


def main(out):
    if os.path.exists(out):
        shutil.rmtree(out)
    shutil.copytree(ROOT, out, ignore=lambda d, names: [n for n in names if d == ROOT and n in SKIP])

    with open(os.path.join(out, ".mcp.json"), "w", encoding="utf-8") as f:
        json.dump(MCP, f, indent=2)
        f.write("\n")

    pj = os.path.join(out, ".claude-plugin", "plugin.json")
    with open(pj, encoding="utf-8") as f:
        meta = json.load(f)
    uc = meta.get("userConfig") or {}
    new_uc = {}
    for k, v in uc.items():
        if k == "dataforseo_login":
            new_uc["dataforseo_token"] = DFS_TOKEN
        elif k == "dataforseo_password":
            continue
        else:
            new_uc[k] = v
    meta["userConfig"] = new_uc
    with open(pj, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
        f.write("\n")

    with open(os.path.join(out, "EDITION.md"), "w", encoding="utf-8") as f:
        f.write(
            "# PARASITER — Claude directory edition\n\n"
            "Built automatically from the main branch by `tools/build_directory_edition.py`. Do not edit this branch by hand.\n\n"
            "Same skills, agents and scripts as the full edition. Position checks use the official hosted MCP servers of "
            "DataForSEO and SerpApi with your own credentials from the plugin settings, and the results go into your journal "
            "(`skills/work-log/references/directory-edition.md`). Batch runs of the bundled scripts on DataForSEO "
            "(big rank checks, AI-answer check, page keywords, platform scans) are in the full edition: "
            "https://github.com/Parasiter-SEO/parasiter-plugin\n"
        )
    print(f"Directory edition built in {out}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(os.path.abspath(sys.argv[1]))
