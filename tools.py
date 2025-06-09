"""Utility functions for various server features.

This module provides simple wrappers around common operations such as
running Python code, interacting with the filesystem, executing shell
commands, basic git operations and making HTTP requests.  The goal is to
have lightweight tools that can be reused by the server and other
scripts without pulling in heavy dependencies.
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests


@dataclass
class ExecResult:
    """Return type for command execution helpers."""

    stdout: str
    stderr: str
    return_code: int


# ---------------------------------------------------------------------------
# Code execution & filesystem tools
# ---------------------------------------------------------------------------

def run_python(code: str) -> ExecResult:
    """Execute a Python snippet and return the result."""
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tmp:
        tmp.write(code)
        tmp_path = tmp.name
    try:
        proc = subprocess.run(
            ["python", tmp_path], capture_output=True, text=True, check=False
        )
        return ExecResult(proc.stdout, proc.stderr, proc.returncode)
    finally:
        os.unlink(tmp_path)


def list_files(path: str) -> List[str]:
    """Return a list of files for the given path."""
    return [str(p) for p in Path(path).iterdir()]


def read_file(path: str) -> str:
    """Read a file and return its contents."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path: str, content: str) -> None:
    """Write *content* to *path*, creating parent directories if needed."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ---------------------------------------------------------------------------
# Shell & git helpers
# ---------------------------------------------------------------------------

def run_cmd(command: str, cwd: Optional[str] = None) -> ExecResult:
    """Execute an arbitrary shell command."""
    proc = subprocess.run(
        command, shell=True, capture_output=True, text=True, cwd=cwd, check=False
    )
    return ExecResult(proc.stdout, proc.stderr, proc.returncode)


def clone(repo_url: str, dest: str) -> ExecResult:
    """Clone a git repository."""
    return run_cmd(f"git clone {repo_url} {dest}")


def status(cwd: str) -> str:
    """Return `git status --short` output for *cwd*."""
    result = run_cmd("git status --short", cwd=cwd)
    return result.stdout


def commit(cwd: str, message: str) -> ExecResult:
    """Create a git commit with the given message."""
    return run_cmd(f"git commit -am {json.dumps(message)}", cwd=cwd)


def push(cwd: str, remote: str, branch: str) -> ExecResult:
    """Push to the specified remote and branch."""
    return run_cmd(f"git push {remote} {branch}", cwd=cwd)


# ---------------------------------------------------------------------------
# HTTP client & simple OpenAPI helpers
# ---------------------------------------------------------------------------

def request(method: str, url: str, headers: Optional[Dict[str, str]] = None, body: str | None = None) -> Dict[str, Any]:
    """Perform an HTTP request and return a simplified response."""
    resp = requests.request(method, url, headers=headers, data=body)
    return {"status": resp.status_code, "headers": dict(resp.headers), "body": resp.text}


def generate_spec(endpoints: List[Dict[str, Any]]) -> str:
    """Generate a minimal OpenAPI-like spec from endpoint definitions."""
    return json.dumps({"openapi": "3.0.0", "endpoints": endpoints}, indent=2)


def validate_request(spec: str, request_info: Dict[str, Any]) -> bool:
    """Very small helper to check if request_info matches any endpoint in *spec*.

    This is **not** a full OpenAPI validation, just a convenience function.
    """
    data = json.loads(spec)
    for ep in data.get("endpoints", []):
        if ep.get("method") == request_info.get("method") and ep.get("path") == request_info.get("path"):
            return True
    return False


# ---------------------------------------------------------------------------
# Database helpers (SQLite + optional MongoDB)
# ---------------------------------------------------------------------------

def execute_sql(conn_params: Dict[str, Any], query: str) -> List[tuple]:
    """Execute an SQL query using sqlite3."""
    import sqlite3

    conn = sqlite3.connect(conn_params.get("database", ":memory:"))
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows


def run_migration(migration_script: str, conn_params: Dict[str, Any]) -> None:
    """Run an SQL migration script using sqlite3."""
    import sqlite3

    conn = sqlite3.connect(conn_params.get("database", ":memory:"))
    cur = conn.cursor()
    cur.executescript(migration_script)
    conn.commit()
    conn.close()


def mongo_find(conn_params: Dict[str, Any], collection: str, filter: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Run a simple MongoDB find operation. Requires `pymongo`."""
    from pymongo import MongoClient

    client = MongoClient(conn_params["uri"])
    db = client[conn_params["db"]]
    results = list(db[collection].find(filter))
    client.close()
    return results


# ---------------------------------------------------------------------------
# Simple HTML parsing using BeautifulSoup
# ---------------------------------------------------------------------------

def extract_with_css(html: str, selector: str) -> List[str]:
    """Extract text from *html* using a CSS selector."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    return [elem.get_text() for elem in soup.select(selector)]


# ---------------------------------------------------------------------------
# Basic auth helpers using JWT
# ---------------------------------------------------------------------------

def generate_jwt(payload: Dict[str, Any], secret: str) -> str:
    """Generate a JSON Web Token."""
    import jwt

    return jwt.encode(payload, secret, algorithm="HS256")


def verify_jwt(token: str, secret: str) -> bool:
    """Verify a JSON Web Token."""
    import jwt

    try:
        jwt.decode(token, secret, algorithms=["HS256"])
        return True
    except jwt.PyJWTError:
        return False


