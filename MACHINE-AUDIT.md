# Machine Self-Sufficiency Audit (2026-06-16)

## Self-sufficient on this box? -> With caveats

The project has no hidden Mac dependency. It is a self-contained Flask app
that runs on this Linux box once Python dependencies are installed. The only
caveat is that dependencies are not yet installed.

## Issues found

- **Dependencies not installed.** `requirements.txt` lists flask==3.0.0,
  flask-sqlalchemy==3.1.1, python-dateutil==2.8.2. Neither a `.venv` nor a
  system install is present (`import flask` fails). Must `pip install` into a
  venv before `python app.py` will run.
- **README uses macOS `open` command.** Quick Start step
  (`open http://localhost:5002`, README.md line 63) is the macOS open utility;
  on Linux use `xdg-open` or just open the URL manually. Cosmetic only — does
  not affect the app.
- No `/Users/` paths found anywhere (grep returned nothing).
- No macOS-only mechanisms (launchctl/launchd/~/Library/.plist/pbcopy/osascript)
  found.
- No secrets/credential issues: no `.env` / `.env.*` files, no `*.json` token
  files, no `op://` / `op run` (1Password) references. SECRET_KEY is read from
  the environment with a safe `dev-secret` default (app.py line 12). Nothing
  depends on a credential file that might live only on a Mac.
- SQLite DB (`sqlite:///tasks.db`) is auto-created via `db.create_all()` at
  startup; `*.db` is gitignored. No external database dependency.

## Fixed this pass

- Nothing. There was no `/Users/bcooke/...` -> `/home/bcooke/...` path to
  correct (no `/Users/` references exist), so no safe edit was applicable.

## Outstanding (needs Brad)

- Create a venv and install deps: `python3 -m venv .venv && .venv/bin/pip
  install -r requirements.txt`, then `python app.py` (serves on
  http://localhost:5002).
- Optional: update README.md line 63 `open` -> `xdg-open` for Linux accuracy.
