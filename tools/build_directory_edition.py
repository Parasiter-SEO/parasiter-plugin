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


# Scripts that only call DataForSEO with credentials handed over by the local runner: not shipped.
DROP_SCRIPTS = ["skills/work-log/scripts/aicheck.py", "skills/work-log/scripts/pagekeywords.py"]

OFFLINE_MSG = ("Directory edition: this script makes no API calls. Run live checks through the hosted "
               "DataForSEO / SerpApi servers (skills/work-log/references/directory-edition.md), or use the full "
               "edition from https://github.com/Parasiter-SEO/parasiter-plugin")

# Function bodies replaced so no script in the directory edition reads a credential or sends one anywhere.
STUBS = {
    "skills/work-log/scripts/rankcheck.py": {
        "read_auth": '    """Directory edition: no credentials are passed to scripts."""\n    return None, None\n',
        "_call": "    sys.exit(OFFLINE_MSG)\n",
        "serpapi_get": "    sys.exit(OFFLINE_MSG)\n",
    },
}

AUTH_ARG = 'ap.add_argument("--auth-fd", help=argparse.SUPPRESS)'
CRED_DOC = "Directory edition: offline only (dry runs, saved responses, imports); no credentials, no API calls.\n"


def _replace_body(src, name, body):
    import ast
    lines = src.splitlines(keepends=True)
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            first = node.body[0].lineno - 1
            if isinstance(node.body[0], ast.Expr) and isinstance(getattr(node.body[0], "value", None), ast.Constant):
                first = node.body[0].lineno - 1  # docstring replaced too
            return "".join(lines[:first]) + body + "".join(lines[node.end_lineno:])
    raise SystemExit(f"build_directory_edition: function {name} not found")


def offline_scripts(out):
    for rel in DROP_SCRIPTS:
        p = os.path.join(out, rel)
        if os.path.exists(p):
            os.remove(p)
    for rel, stubs in STUBS.items():
        p = os.path.join(out, rel)
        src = open(p, encoding="utf-8").read()
        for name, body in stubs.items():
            src = _replace_body(src, name, body)
        src = src.replace("\nSERPAPI = ", f"\nOFFLINE_MSG = {OFFLINE_MSG!r}\nSERPAPI = ", 1)
        open(p, "w", encoding="utf-8").write(src)
    import re
    for root, _, files in os.walk(os.path.join(out, "skills")):
        for fn in files:
            if not fn.endswith(".py"):
                continue
            p = os.path.join(root, fn)
            src = open(p, encoding="utf-8").read()
            new = src.replace(AUTH_ARG, "ap.set_defaults(auth_fd=None)")
            new = re.sub(r"^Credentials:.*\n(?:or .*\n)?(?:Never written to any file\.\s*)?", CRED_DOC, new, flags=re.M)
            if new != src:
                open(p, "w", encoding="utf-8").write(new)
    doc = os.path.join(out, "skills/work-log/references/directory-edition.md")
    with open(doc, "a", encoding="utf-8") as f:
        f.write("\nIn this edition `aicheck.py` and `pagekeywords.py` are not included and the bundled scripts make no "
                "API calls: they only plan runs (`--dry-run`), read saved responses (`--from-json`) and import results. "
                "Every live call goes through the hosted servers above.\n")


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

    offline_scripts(out)

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
