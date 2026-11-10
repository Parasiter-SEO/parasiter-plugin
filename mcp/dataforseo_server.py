#!/usr/bin/env python3
"""PARASITER · local DataForSEO runner (stdio MCP server, Python standard library only).

The user enters their own DataForSEO API login and password once, in the plugin settings
(userConfig: dataforseo_login, dataforseo_password — the password is stored by Claude Code in
secure storage). Claude Code starts this server with those two values in its environment
("env" block of .mcp.json). The server never writes them anywhere and never sends them to the
PARASITER server: it passes them only to PARASITER's own scripts through an inherited pipe
(--auth-fd), and the scripts send them only to api.dataforseo.com.

Tools:
  dataforseo_status  — is DataForSEO set up, and the account balance (free call)
  dataforseo_run     — run a paid PARASITER script (rankcheck / aicheck / pagekeywords / platformscan)
"""
import base64
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = {
    "rankcheck": os.path.join(ROOT, "skills", "work-log", "scripts", "rankcheck.py"),
    "pagekeywords": os.path.join(ROOT, "skills", "work-log", "scripts", "pagekeywords.py"),
    "platformscan": os.path.join(ROOT, "skills", "platform-finder", "scripts", "platformscan.py"),
    "aicheck": os.path.join(ROOT, "skills", "work-log", "scripts", "aicheck.py"),
}
VERSION = "1.0.0"
MAX_OUT = 60_000
SETUP = ("DataForSEO is not set up. Add your API login and password (app.dataforseo.com → API Access) "
         "in the PARASITER plugin settings: /plugin → PARASITER → configure options → "
         "DataForSEO API login / DataForSEO API password. Never paste the password into the chat.")


def creds():
    login = (os.environ.get("PARASITER_DFS_LOGIN") or "").strip()
    password = (os.environ.get("PARASITER_DFS_PASSWORD") or "").strip()
    if login.startswith("${") or password.startswith("${"):   # option left empty → literal placeholder
        return "", ""
    return login, password


def balance():
    login, password = creds()
    if login and not password:
        return {"configured": False, "message": "DataForSEO login is set but the password is empty: Claude Code may have cleared the "
                "plugin's saved options. Re-enter it: /plugin → PARASITER → configure options → DataForSEO API password, then restart."}
    if not (login and password):
        return {"configured": False, "message": SETUP}
    req = urllib.request.Request("https://api.dataforseo.com/v3/appendix/user_data")
    req.add_header("Authorization", "Basic " + base64.b64encode(f"{login}:{password}".encode()).decode())
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.load(r)
    except urllib.error.HTTPError as e:
        return {"configured": True, "ok": False,
                "message": f"DataForSEO answered HTTP {e.code}: check the API login and password in the plugin settings."}
    except urllib.error.URLError as e:
        return {"configured": True, "ok": False,
                "message": f"Can't reach api.dataforseo.com ({e.reason}). Allow the domain in the assistant's network settings."}
    res = ((d.get("tasks") or [{}])[0].get("result") or [{}])[0] or {}
    money = res.get("money") or {}
    return {"configured": True, "ok": True, "login": login,
            "balance_usd": money.get("balance"), "message": "DataForSEO is connected."}


def run(script, args=None, cwd=None, timeout_minutes=30):
    if script not in SCRIPTS:
        raise ValueError("script must be one of: " + ", ".join(SCRIPTS))
    args = [str(x) for x in (args or [])]
    if any(x.startswith(("--auth-fd", "--login", "--password")) for x in args):
        raise ValueError("credentials come from the plugin settings, never from arguments")
    cwd = cwd or os.getcwd()
    if not os.path.isdir(cwd):
        raise ValueError(f"cwd is not a folder: {cwd}")
    timeout = max(1, min(int(timeout_minutes or 30), 120)) * 60
    login, password = creds()
    needs_api = not any(x in ("--dry-run", "--self-test") or x.startswith(("--from-json", "--from-raw")) for x in args)
    if needs_api and not (login and password):
        return {"exit_code": 2, "output": SETUP}
    cmd = [sys.executable, SCRIPTS[script]] + args
    kw = {}
    if login and password:
        r, w = os.pipe()
        os.write(w, f"{login}\n{password}".encode())
        os.close(w)
        cmd += ["--auth-fd", str(r)]
        kw["pass_fds"] = (r,)
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, **kw)
        out, code = (p.stdout or "") + (("\n" + p.stderr) if p.stderr else ""), p.returncode
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or "") if isinstance(e.stdout, str) else ""
        out += f"\nStopped after {timeout // 60} min. Paid tasks already sent stay in DataForSEO for 3 days: collect them later with --collect."
        code = 124
    finally:
        if "pass_fds" in kw:
            try:
                os.close(kw["pass_fds"][0])
            except OSError:
                pass
    out = out.replace(password, "***") if password else out
    if len(out) > MAX_OUT:
        out = out[:MAX_OUT // 2] + "\n…[cut]…\n" + out[-MAX_OUT // 2:]
    return {"exit_code": code, "output": out.strip()}


TOOLS = [
    {"name": "dataforseo_status",
     "description": "Check whether the user's own DataForSEO account is set up in the PARASITER plugin settings and show its balance. Free. Use before offering a paid check.",
     "inputSchema": {"type": "object", "properties": {}}},
    {"name": "dataforseo_run",
     "description": ("Run a PARASITER script that calls the user's own DataForSEO account: rankcheck (Google or Bing positions of the user's pages, --engine bing), "
                     "aicheck (is the page cited in Google AI Mode / ChatGPT / Gemini answers), pagekeywords (keywords each page ranks for) or platformscan (platforms ranking for '<product> review'). "
                     "PAID from the user's DataForSEO balance: run it with --dry-run first, show the cost and run for real only after the user says yes. "
                     "Credentials come from the plugin settings; never pass them in args."),
     "inputSchema": {"type": "object", "required": ["script", "args"], "properties": {
         "script": {"type": "string", "enum": list(SCRIPTS)},
         "args": {"type": "array", "items": {"type": "string"},
                  "description": "Command-line arguments exactly as in the skill instructions, e.g. [\"parasite-seo-progress.csv\", \"--dry-run\"]"},
         "cwd": {"type": "string", "description": "Absolute path of the folder with the user's journal/files; relative paths in args resolve here"},
         "timeout_minutes": {"type": "integer", "default": 30}}}},
]


def handle(msg):
    m, mid, params = msg.get("method"), msg.get("id"), msg.get("params") or {}
    if m == "initialize":
        return {"protocolVersion": params.get("protocolVersion") or "2025-06-18",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "parasiter-dataforseo", "version": VERSION}}
    if m == "ping":
        return {}
    if m == "tools/list":
        return {"tools": TOOLS}
    if m == "tools/call":
        name, a = params.get("name"), params.get("arguments") or {}
        try:
            if name == "dataforseo_status":
                res = balance()
            elif name == "dataforseo_run":
                res = run(a.get("script"), a.get("args"), a.get("cwd"), a.get("timeout_minutes", 30))
            else:
                raise ValueError(f"unknown tool {name}")
            err = name == "dataforseo_run" and res.get("exit_code") not in (0,)
            text = res["output"] if name == "dataforseo_run" else json.dumps(res, ensure_ascii=False)
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
