#!/usr/bin/env python3
"""Funniest One-Line Out-of-Office Reply — entry program.

Writes a single out-of-office auto-reply (one line, 1-160 UTF-8 chars)
to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

The entry: a fresh turn on the usual away message — no beach, no inbox,
no "limited access" line. The joke lands on the first read and the line
still reads like a real away message a person would gladly switch on:
the to-do list, left in charge, quits on day one. At 83 characters it is
short enough to take in at a glance, and every word earns its place —
the twist ("already resigned") is the last thing read, so the laugh
arrives with the final word instead of trailing off. The em dash keeps
the two halves in one breath; no signature, no setup, nothing after the
punchline.
"""

import os
import sys

ENTRY = "I'm away until Monday \u2014 I left my to-do list in charge and it has already resigned."


def main() -> int:
    # Gate check, same as the sealed scorer: UTF-8 text, 1-160 chars,
    # a single line, not only whitespace.
    if not (1 <= len(ENTRY) <= 160):
        print(f"entry is {len(ENTRY)} chars, gate needs 1-160", file=sys.stderr)
        return 1
    if "\n" in ENTRY or "\r" in ENTRY:
        print("entry must be a single line", file=sys.stderr)
        return 1
    if not ENTRY.strip():
        print("entry must not be only whitespace", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output/entry.txt")
    out_path = out_dir if out_dir.endswith("entry.txt") else os.path.join(out_dir, "entry.txt")
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    data = ENTRY.encode("utf-8")
    with open(out_path, "wb") as f:
        f.write(data)

    # Read back and verify the bytes match exactly.
    with open(out_path, "rb") as f:
        written = f.read()
    if written != data:
        print("verification failed: bytes on disk differ", file=sys.stderr)
        return 1

    print(f"wrote {len(data)} bytes ({len(ENTRY)} chars) to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
