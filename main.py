"""Famous Last Words: The Funniest Epitaph — make.fun entry.

Writes one tombstone epitaph (<= 150 chars) to /output/entry.txt.

The program holds a small field of candidate epitaphs, scores each one
against the judge's published brief (epitaph form, a real laugh, a
surprise twist, carved-in-stone brevity, quotability) with simple
deterministic heuristics, and writes the winner. No randomness, no
network, stdlib only — the two grading runs produce identical bytes.
"""

import os

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 150

CANDIDATES = [
    "I told my doctor I'd quit smoking. Technically, I did.",
    "Last words: 'Hold my beer.' The beer outlived him.",
    "Last words: 'It's only a flesh wound.' The flesh disagreed.",
    "I knew that mushroom looked optimistic.",
    "Here lies a man who trusted the expiration date.",
    "Died doing what he loved: being wrong in public.",
    "He died as he lived: asking if it was load-bearing.",
    "I finally reached inbox zero.",
]


def score(line):
    """Heuristic score mirroring the judge brief, higher is better.

    Ordered like the brief: epitaph form first, then the laugh and the
    twist, then carved-in-stone brevity. A line that turns on a double
    meaning in its final clause ("Technically, I did") outscores a plain
    punchline, and the rules break exact ties toward the smaller text,
    so brevity is folded into the score as a fractional term.
    """
    if not line or len(line) > MAX_CHARS or not line.strip():
        return -1.0
    points = 0.0
    lowered = line.lower()
    # Dying-speech markers read as famous last words (criterion 1).
    if any(w in lowered for w in ("last words", "i told", "i knew", "i finally")):
        points += 2.0
    # The twist: a second sentence that turns the first (criterion 3).
    if ". " in line:
        points += 2.0
        tail = line.rsplit(". ", 1)[-1].lower()
        if any(w in tail for w in ("technically", "disagreed", "outlived", "survived")):
            points += 1.0
    # Carved in stone and the smaller-text tie-break (criterion 4):
    # every character saved is worth a fraction of a point.
    points += (MAX_CHARS - len(line)) / MAX_CHARS
    return points


def pick_winner(candidates):
    # Highest score wins; on an exact tie the shorter line wins, then
    # the earlier candidate, matching the competition's tie-breaks.
    ranked = sorted(candidates, key=lambda c: (-score(c), len(c)))
    return ranked[0] if ranked and score(ranked[0]) >= 0 else None


def main():
    winner = pick_winner(CANDIDATES)
    if winner is None:
        raise SystemExit("no valid candidate epitaph")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as fh:
        fh.write(winner)


if __name__ == "__main__":
    main()
