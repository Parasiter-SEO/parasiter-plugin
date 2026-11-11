#!/usr/bin/env python3
"""PARASITER · local SerpApi runner (stdio MCP server, Python standard library only).

The user enters their own SerpApi API key once, in the plugin settings (userConfig: serpapi_key,
stored by Claude Code in secure storage). Claude Code starts this server with it in the environment
("env" block of .mcp.json). The server never writes the key anywhere and never sends it to the
PARASITER server: it passes it only to PARASITER's own script through an inherited pipe (--auth-fd),
and the script sends it only to serpapi.com.

An alternative to DataForSEO for position checks: SerpApi's free plan gives 250 searches a month.

Tools:
  serpapi_status — is SerpApi set up, the plan and the searches left this month (free, uses no search)
  serpapi_run    — run the position check (rankcheck) or the offer scan (offerscan) on the user's SerpApi account
"""
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = {
    "rankcheck": os.path.join(ROOT, "skills", "work-log", "scripts", "rankcheck.py"),
    "offerscan": os.path.join(ROOT, "skills", "affiliate-finder", "scripts", "offerscan.py"),
}
VERSION = "1.0.0"
MAX_OUT = 60_000
SIGNUP = "https://serpapi.com/users/sign_up"
SETUP = ("SerpApi is not set up. Create a free account (" + SIGNUP + ", 250 searches a month), copy your API key "
         "from serpapi.com/manage-api-key and add it in the PARASITER plugin settings: /plugin → PARASITER → "
         "configure options → SerpApi API key. Never paste the key into the chat.")


def key():
    k = (os.environ.get("PARASITER_SERPAPI_KEY") or "").strip()
    return "" if k.startswith("${") else k   # option left empty → literal placeholder


def status():
    k = key()
    if not k:
        return {"configured": False, "message": SETUP}
    url = "https://serpapi.com/account.json?" + urllib.parse.urlencode({"api_key": k})
    try:
        with urllib.request.urlopen(urllib.request.Request(url), timeout=30) as r:
            d = json.load(r)
    except urllib.error.HTTPError as e:
        return {"configured": True, "ok": False,
                "message": f"SerpApi answered HTTP {e.code}: check the API key in the plugin settings."}
    except urllib.error.URLError as e:
        return {"configured": True, "ok": False,
                "message": f"Can't reach serpapi.com ({e.reason}). Allow the domain in the assistant's network settings."}
    if d.get("error"):
        return {"configured": True, "ok": False, "message": f"SerpApi: {d['error']}"}
    return {"configured": True, "ok": True, "plan": d.get("plan_name"),
            "searches_per_month": d.get("searches_per_month"),
            "searches_left": d.get("total_searches_left", d.get("plan_searches_left")),
            "used_this_month": d.get("this_month_usage"),
            "hourly_limit": d.get("account_rate_limit_per_hour"),
            "message": "SerpApi is connected."}


def run(script, args=None, cwd=None, timeout_minutes=30):
    if script not in SCRIPTS:
        raise ValueError("script must be one of: " + ", ".join(SCRIPTS))
    args = [str(x) for x in (args or [])]
    if any(x.startswith(("--auth-fd", "--api-key", "--key", "--provider")) for x in args):
        raise ValueError("the key comes from the plugin settings and the provider is set by this tool; don't pass them in args")
    cwd = cwd or os.getcwd()
    if not os.path.isdir(cwd):
        raise ValueError(f"cwd is not a folder: {cwd}")
    timeout = max(1, min(int(timeout_minutes or 30), 120)) * 60
    k = key()
    needs_api = not any(x in ("--dry-run", "--self-test") or x.startswith(("--from-json", "--urls")) for x in args)
    if needs_api and not k:
        return {"exit_code": 2, "output": SETUP}
    cmd = [sys.executable, SCRIPTS[script]] + args + ["--provider", "serpapi"]
    kw = {}
    if k:
        r, w = os.pipe()
        os.write(w, k.encode())
        os.close(w)
        cmd += ["--auth-fd", str(r)]
        kw["pass_fds"] = (r,)
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, **kw)
        out, code = (p.stdout or "") + (("\n" + p.stderr) if p.stderr else ""), p.returncode
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or "") if isinstance(e.stdout, str) else ""
        out += f"\nStopped after {timeout // 60} min. Searches already made are counted by SerpApi."
        code = 124
    finally:
        if "pass_fds" in kw:
            try:
                os.close(kw["pass_fds"][0])
            except OSError:
                pass
    out = out.replace(k, "***") if k else out
    if len(out) > MAX_OUT:
        out = out[:MAX_OUT // 2] + "\n…[cut]…\n" + out[-MAX_OUT // 2:]
    return {"exit_code": code, "output": out.strip()}


TOOLS = [
    {"name": "serpapi_status",
     "description": "Check whether the user's own SerpApi account is set up in the PARASITER plugin settings, its plan and the searches left this month. Free, uses no search. Use before offering a SerpApi position check.",
     "inputSchema": {"type": "object", "properties": {}}},
    {"name": "serpapi_run",
     "description": ("Run PARASITER's position check (rankcheck: Google or Bing positions of the user's pages, --engine bing) or the offer scan (offerscan: which affiliate products and programs the top pages push) on the user's own SerpApi account — "
                     "the alternative to dataforseo_run. Uses the user's SerpApi searches (free plan: 250 a month; Google: 1 search per 10 results per query, "
                     "so top 30 = 3 searches per query). Run it with --dry-run first, show how many searches it takes and how many are left (serpapi_status), "
                     "and run for real only after the user says yes. The key comes from the plugin settings; never pass it, or --provider, in args."),
     "inputSchema": {"type": "object", "required": ["script", "args"], "properties": {
         "script": {"type": "string", "enum": list(SCRIPTS)},
         "args": {"type": "array", "items": {"type": "string"},
                  "description": "Command-line arguments exactly as in the skill instructions, e.g. [\"parasite-seo-progress.csv\", \"--depth\", \"10\", \"--dry-run\"]"},
         "cwd": {"type": "string", "description": "Absolute path of the folder with the user's journal/files; relative paths in args resolve here"},
         "timeout_minutes": {"type": "integer", "default": 30}}}},
]


def handle(msg):
    m, params = msg.get("method"), msg.get("params") or {}
    if m == "initialize":
        return {"protocolVersion": params.get("protocolVersion") or "2025-06-18",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "parasiter-serpapi", "version": VERSION}}
    if m == "ping":
        return {}
    if m == "tools/list":
        return {"tools": TOOLS}
    if m == "tools/call":
        name, a = params.get("name"), params.get("arguments") or {}
        try:
            if name == "serpapi_status":
                res = status()
            elif name == "serpapi_run":
                res = run(a.get("script"), a.get("args"), a.get("cwd"), a.get("timeout_minutes", 30))
            else:
                raise ValueError(f"unknown tool {name}")
            err = name == "serpapi_run" and res.get("exit_code") not in (0,)
            text = res["output"] if name == "serpapi_run" else json.dumps(res, ensure_ascii=False)
            return {"content": [{"type": "text", "text": text or "(no output)"}], "isError": bool(err)}
        except Exception as e:  # noqa: BLE001 — returned to the client as a tool error
            return {"content": [{"type": "text", "text": str(e)}], "isError": True}
    raise LookupError(m)


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        if "id" not in msg:          # notification (initialized, cancelled…)
            continue
        try:
            reply = {"jsonrpc": "2.0", "id": msg["id"], "result": handle(msg)}
        except LookupError:
            reply = {"jsonrpc": "2.0", "id": msg["id"], "error": {"code": -32601, "message": "Method not found"}}
        sys.stdout.write(json.dumps(reply, ensure_ascii=False) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
