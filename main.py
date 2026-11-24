#!/usr/bin/env python3
"""oneline-best-line entry: write the one line to /output/entry.txt.

The line is embedded here (the graded program runs with no network and only
the standard library), and this program writes it to the grader's output
directory, validating it against the gate first so an over-long or empty
line fails loudly instead of being submitted silently.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import hashlib
import os
import sys
import tempfile

LINE = "I told my AI assistant I was lonely, so it booked a meeting with myself \u2014 and then no-showed."
MAX_CHARS = 240
OUTPUT_NAME = "entry.txt"


def main():
    if not LINE.strip():
        print("error: line is empty", file=sys.stderr)
        return 1
    if len(LINE) > MAX_CHARS:
        print(f"error: line is {len(LINE)} chars, over the {MAX_CHARS} limit",
              file=sys.stderr)
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    target = os.path.join(output_dir, OUTPUT_NAME)
    os.makedirs(output_dir, exist_ok=True)
    # Write atomically: a temp file in the output dir, then rename, so the
    # grader never sees a half-written file and both runs write the same
    # bytes. No trailing newline: the gate counts characters, and the
    # tie-break favours the smaller text.
    fd, tmp_path = tempfile.mkstemp(prefix=".entry-", dir=output_dir)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as out:
            out.write(LINE)
        os.replace(tmp_path, target)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise

    print(f"wrote {target} ({len(LINE)} chars, "
          f"{len(LINE.encode('utf-8'))} bytes, "
          f"sha256 {hashlib.sha256(LINE.encode('utf-8')).hexdigest()[:12]})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
