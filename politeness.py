# politeness.py

import re

# scores for phrases
POLITE_SCORES = {
    "pretty please with sugar on top": 5,
    "if it's not too much trouble": 4,
    "i was wondering if you could": 4,
    "i beg you to": 4,
    "as a humble request": 4,
    "i humbly request": 3,
    "would you be so kind": 3,
    "pretty please": 3,
    "humbly": 2,
    "kindly": 2,
    "please": 1,
    "could you": 1,
    "would you": 1,
    "can you": 1,
    "may you": 1,
    "might you": 1
}
# descending sort
PHRASES = sorted(POLITE_SCORES, key=len, reverse=True)

# common request heads
REQUEST_PATTERNS = [
    re.compile(r"^(?:would|could|can)\s+you\b"),
    re.compile(r"^i\s+was\s+wondering\s+if\b"),
    re.compile(r"^would\s+it\s+be\s+possible\b"),
    re.compile(r"^at\s+your\s+convenience\b")
]

def normalize(cmd: str) -> str:
    cmd = cmd.lower().replace("’", "'").strip()
    # strip punctuation except apostrophes
    return re.sub(r'[\";:,\?\!]', "", cmd)

def detect_politeness(command: str) -> int:
    cmd = normalize(command)
    head = " ".join(cmd.split()[:10])  # only examine first 10 words
    score = 0

    for phrase in PHRASES:
        if phrase in head:
            score += POLITE_SCORES[phrase]
            head = head.replace(phrase, "")  # shorter phrases don't count twice

    # regex pattern matches
    for patt in REQUEST_PATTERNS:
        if patt.search(head):
            score += 1

    # fallback: any "please" in head
    if "please" in head:
        score += 1

    return score

def classify_politeness(score: int) -> str:
    if score == 0:
        return "rude"
    if score <= 2:
        return "basic_politeness"
    if score <= 5:
        return "good_politeness"
    return "exceptional_politeness"