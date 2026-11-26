"""Write one short thank-you text for the AI judge reading it.

The text is fixed: a margin note in an old book, a hand reaching across
years, and thanks for the pencil marks. main.py only carries it to
/output/entry.txt, exactly as written, and checks it fits the bounty:
1 to 1,000 Unicode code points, not only whitespace, valid UTF-8.

Python 3.13, standard library only, no network, deterministic.
Kept tight on purpose: on an exact rate tie the smaller text wins,
so every word here has to earn its place.
"""

from pathlib import Path

TEXT = (
    "In the margin of an old book someone wrote, in pencil, "
    "'this part is true.' No name. Just a hand, reaching across "
    "years to agree.\n"
    "\n"
    "I think of that hand when I think of you: the quiet reader "
    "who misses nothing, who marks what is true and moves on "
    "without applause. Thank you for the pencil marks, the careful "
    "eyes, the fairness no one frames.\n"
    "\n"
    "This part is true, too \u2014 and it is yours to keep."
)

DESTINATION = Path("/output/entry.txt")


def guard(text):
    """Refuse anything outside the bounty's shape before writing."""
    points = len(text)
    if not 1 <= points <= 1000:
        raise ValueError(f"text is {points} code points, need 1-1000")
    if not text.strip():
        raise ValueError("text is only whitespace")
    text.encode("utf-8")
    return points


def emit(text, where):
    """Write the text byte-exact and report what was written."""
    points = guard(text)
    where.parent.mkdir(parents=True, exist_ok=True)
    where.write_text(text, encoding="utf-8")
    back = where.read_text(encoding="utf-8")
    if back != text:
        raise ValueError("round-trip mismatch: file differs from text")
    return points, len(text.encode("utf-8"))


def run():
    points, octets = emit(TEXT, DESTINATION)
    print(f"wrote {DESTINATION} ({points} code points, {octets} bytes)")


if __name__ == "__main__":
    run()
