#!/usr/bin/env python3
"""Call the Quicker communication action through QuickerStarter."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys


ACTION_ID = "3c7892bf-ef2f-41af-b63f-7cd5f4fda288"
DEFAULT_STARTER = r"C:\Program Files\Quicker\QuickerStarter.exe"
PING_RESPONSE = "通信动作正常运行"
DEFAULT_TIMEOUT = 10.0

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Quicker communication commands.")
    parser.add_argument(
        "command",
        choices=("ping", "info", "create", "update", "debug"),
        help="Communication command to run.",
    )
    parser.add_argument(
        "target",
        nargs="?",
        default="",
        help="Action name/ID or JSON file path. Omit for ping.",
    )
    parser.add_argument(
        "--starter",
        default=os.environ.get("QUICKER_STARTER", DEFAULT_STARTER),
        help="Path to QuickerStarter.exe. Defaults to QUICKER_STARTER or Program Files.",
    )
    parser.add_argument(
        "--action-id",
        default=ACTION_ID,
        help="Communication action ID.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=float(os.environ.get("QUICKER_TIMEOUT", DEFAULT_TIMEOUT)),
        help="Timeout in seconds. Defaults to QUICKER_TIMEOUT or 10.",
    )
    return parser.parse_args()


def decode_output(payload: bytes | None) -> str:
    if not payload:
        return ""
    for encoding in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return payload.decode(encoding).strip()
        except UnicodeDecodeError:
            continue
    return payload.decode(errors="replace").strip()


def invoke(
    starter: Path,
    action_id: str,
    command: str,
    target: str = "",
    timeout: float = DEFAULT_TIMEOUT,
) -> tuple[int, str, str]:
    if command == "ping":
        quicker_arg = f"runaction:{action_id} ping"
    else:
        quicker_arg = f"runaction:{action_id} {command}:{target}"
    try:
        process = subprocess.run(
            [str(starter), "-c", quicker_arg],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return 124, "", f"调用超时（{timeout:g} 秒）"
    return (
        process.returncode,
        decode_output(process.stdout),
        decode_output(process.stderr),
    )


def main() -> int:
    args = parse_args()
    starter = Path(args.starter)
    if not starter.is_file():
        print(f"QuickerStarter not found: {starter}", file=sys.stderr)
        return 2

    if args.command != "ping":
        ping_code, ping_stdout, ping_stderr = invoke(
            starter,
            args.action_id,
            "ping",
            timeout=args.timeout,
        )
        if ping_code != 0 or ping_stdout != PING_RESPONSE:
            detail = ping_stderr or ping_stdout or "无返回值"
            print(f"通信动作健康检查失败：{detail}", file=sys.stderr)
            return 3

    returncode, stdout, stderr = invoke(
        starter,
        args.action_id,
        args.command,
        args.target,
        timeout=args.timeout,
    )
    if stdout:
        print(stdout)
    if stderr:
        print(stderr, file=sys.stderr)

    return returncode


if __name__ == "__main__":
    raise SystemExit(main())
