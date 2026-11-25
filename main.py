"""Excuse generator for make.fun's "The Excuse That Almost Works" bounty.

Writes one line of plain text to /output/entry.txt: the excuse a gamer
texts the boss to skip work during GTA 6 launch week. Deterministic:
no randomness, no clock, no network, no input files.

The excuse leans on a boring, specific workplace detail (fire alarm
testing right above the desk) instead of a cliche sick day, so a tired
manager would almost believe it.
"""

import os
import sys

# The excuse, kept as two halves so the line reads like one hurried text.
SETUP = "Fire alarm testing all morning and my desk's right under the speaker,"
ASK = "can I work from home today?"

MAX_WORDS = 20
MAX_CHARS = 140

# Angles the judge already dismisses: dead relatives, flat tyres, fevers.
CLICHE_WORDS = ("grandma", "grandmother", "tyre", "tire", "fever", "funeral")


def build_entry():
    """Join the setup and the ask into a single line."""
    return " ".join([SETUP, ASK])


def output_path():
    if len(sys.argv) > 1:
        return os.path.join(sys.argv[1], "entry.txt")
    return os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.txt")


def validate(text):
    """Enforce the gate: 1-140 chars, one line, at most 20 words, no cliche."""
    words = text.split()
    problems = []
    if text != text.strip():
        problems.append("leading/trailing whitespace")
    if "\n" in text or "\r" in text:
        problems.append("more than one line")
    if not 1 <= len(text) <= MAX_CHARS:
        problems.append("length outside 1-140 characters")
    if len(words) > MAX_WORDS:
        problems.append("more than 20 words")
    lowered = text.lower()
    for cliche in CLICHE_WORDS:
        if cliche in lowered:
            problems.append(f"uses cliche word: {cliche}")
    if problems:
        raise ValueError("invalid entry: " + "; ".join(problems))
    return len(words)


def write_entry(path, text):
    """Write the entry and read it back to prove it landed byte for byte."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != text + "\n":
        raise RuntimeError("round-trip check failed: file differs from entry")
    return written


def main():
    path = output_path()
    text = build_entry()
    word_count = validate(text)
    write_entry(path, text)
    print(f"wrote {len(text)} chars, {word_count} words -> {path}")


if __name__ == "__main__":
    main()
