#!/usr/bin/env python3
"""The Printer Apology — one-line apology from an office printer.

Three genuinely different candidate lines, each scored 0-5 on the judge's
five criteria in order (see RULES.txt):
  1. Genuinely an apology from a printer to its office, with the printer's
     own gripes in it.
  2. The laugh: a real joke, punch at the end.
  3. Printer truth: a grievance a printer would actually suffer
     (jams, cheap paper, staples, being asked for colour).
  4. Freshness: not the first joke anyone would write about a printer.
  5. Economy: every word earns its place inside 120 characters.

Winner = highest total; ties break by criterion order (criterion 1 first,
then 2, 3, 4, 5). Fully deterministic: no randomness, no clock, no network,
no file reads.
"""

import os

# ---------------------------------------------------------------------------
# Candidates. Each entry: (text, [score_c1, score_c2, score_c3, score_c4,
# score_c5]) with a short reason per score in the comment above it.
# ---------------------------------------------------------------------------

# V1 — ANGLE: blame-shift. The printer apologises for jamming, then turns
# the blame back on the office for feeding it bargain-bin paper.
#   c1=4: clear apology + the printer's own gripe (cheap paper), though the
#         apology is half-hearted by design.
#   c2=4: real joke, punch ("choke on it") lands at the end.
#   c3=5: jams + cheap paper are the two classic printer sufferings.
#   c4=3: "cheap paper made me jam" is a well-worn printer complaint.
#   c5=4: tight, but "in the store" is filler-ish.
V1 = (
    "Sorry I jammed. You feed me the cheapest paper in the store, "
    "then act shocked when I choke on it.",
    [4, 4, 5, 3, 4],
)

# V2 — ANGLE: the staple diet. The printer apologises for eating staples,
# as if the office keeps serving them as lunch.
#   c1=4: apology + gripe (staples), though "my lunch" is a stretch.
#   c2=4: punch ("technically this is on you") is solid but a little dry.
#   c3=5: staples are a real, specific printer torment.
#   c4=4: treating staples as food is a less obvious angle than jams.
#   c5=4: no wasted words; "technically" earns its place as the pivot.
V2 = (
    "Apologies for eating your staples. You keep stapling my lunch, "
    "so technically this is on you.",
    [4, 4, 5, 4, 4],
)

# V3 — ANGLE: the colour request breaks the printer. It apologises for the
# black-and-white output, then confesses it laughed so hard at being asked
# for colour that its cyan ran out.
#   c1=4: apology + gripe (being asked for colour), direct and on-topic.
#   c2=5: the punch ("my cyan ran out") is a real joke and sits last.
#   c3=4: being asked for colour is a real printer gripe; cyan running out
#         is a real printer failure, even if the cause is played for laughs.
#   c4=5: a printer laughing until its ink runs out is not the first joke
#         anyone writes about a printer.
#   c5=4: tight now — "came out" replaces the wordier "I printed your".
V3 = (
    "Sorry your report came out black and white. You asked for "
    "colour; I laughed so hard my cyan ran out.",
    [4, 5, 4, 5, 4],
)

CANDIDATES = [V1, V2, V3]


def pick_winner(candidates):
    """Highest total wins; ties break by criterion order (c1, then c2...)."""
    best = None
    best_key = None
    for text, scores in candidates:
        # Key: total first, then each criterion in judge order, so a tie on
        # the total is settled by the earliest criterion that differs.
        key = (sum(scores),) + tuple(scores)
        if best_key is None or key > best_key:
            best_key = key
            best = (text, scores)
    return best


def main():
    winner_text, winner_scores = pick_winner(CANDIDATES)

    # Gate: 1-120 chars, one line, no trailing whitespace.
    assert 1 <= len(winner_text) <= 120, "winner out of length range"
    assert "\n" not in winner_text and "\r" not in winner_text
    assert winner_text == winner_text.strip()

    out_path = os.environ.get("ENTRY_OUTPUT") or "/output/entry.txt"
    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(winner_text)
    os.chmod(out_path, 0o644)


if __name__ == "__main__":
    main()
