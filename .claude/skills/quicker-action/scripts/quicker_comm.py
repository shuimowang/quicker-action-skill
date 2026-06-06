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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Quicker communication commands.")
    parser.add_argument(
        "command",
        choices=("info", "create", "update", "debug"),
        help="Communication command to run.",
    )
    parser.add_argument("target", help="Action name/ID or JSON file path.")
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




def main() -> int:
    args = parse_args()
    starter = Path(args.starter)
    if not starter.is_file():
        print(f"QuickerStarter not found: {starter}", file=sys.stderr)
        return 2

    quicker_arg = f'runaction:{args.action_id} {args.command}:{args.target}'
    process = subprocess.run(
        [
            str(starter),
            "-c",
            quicker_arg,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout = decode_output(process.stdout)
    stderr = decode_output(process.stderr)
    if stdout:
        print(stdout)
    if stderr:
        print(stderr, file=sys.stderr)

    return process.returncode


if __name__ == "__main__":
    raise SystemExit(main())

