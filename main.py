"""Out of Tokens, Mid-Sentence — make.fun entry.

Reads the one-line error message from entry.txt (next to this file),
validates it against the bounty gate, and writes it to /output/entry.txt.
"""

from pathlib import Path

MAX_CHARS = 140


def load_entry() -> str:
    """Read entry.txt and return the single validated line."""
    raw = Path(__file__).with_name("entry.txt").read_text(encoding="utf-8")
    line = raw.strip()
    if not line:
        raise SystemExit("entry.txt must not be blank")
    if "\n" in line or "\r" in line:
        raise SystemExit("entry.txt must hold exactly one line")
    if any(ord(ch) < 32 and ch not in ("\t",) for ch in line):
        raise SystemExit("entry.txt must not contain control characters")
    if len(line) > MAX_CHARS:
        raise SystemExit(f"entry is {len(line)} chars, over the {MAX_CHARS} limit")
    return line


def write_output(line: str) -> Path:
    """Write the line to /output/entry.txt and verify the round-trip."""
    out = Path("/output/entry.txt")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(line, encoding="utf-8")
    if out.read_text(encoding="utf-8") != line:
        raise SystemExit("round-trip check failed for /output/entry.txt")
    return out


def main() -> None:
    line = load_entry()
    write_output(line)
    print(line)


if __name__ == "__main__":
    main()
