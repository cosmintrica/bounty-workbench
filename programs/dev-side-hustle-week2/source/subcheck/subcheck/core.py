"""SRT validation and word alignment independent of the speech runtime."""
from dataclasses import asdict, dataclass
from collections import Counter
from difflib import SequenceMatcher
import math
import re
import textwrap


@dataclass(frozen=True)
class Cue:
    id: int
    start: float
    end: float
    text: str


@dataclass(frozen=True)
class Word:
    start: float
    end: float
    text: str
    probability: float


STAMP = r"(\d{2,}):([0-5]\d):([0-5]\d)[,.](\d{3})"
TIMING = re.compile(rf"^{STAMP}\s+-->\s+{STAMP}$")
TOKENS = re.compile(r"\w+(?:['’]\w+)*", re.UNICODE)


def seconds(parts):
    h, m, s, ms = map(int, parts)
    return h * 3600 + m * 60 + s + ms / 1000


def parse_srt(text: str) -> list[Cue]:
    text = text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n").strip()
    if not text:
        raise ValueError("The subtitle file is empty.")
    cues, seen = [], set()
    for block in re.split(r"\n[ \t]*\n", text):
        lines = block.splitlines()
        if len(lines) < 3 or not lines[0].strip().isdigit():
            raise ValueError("Each SRT block needs a numeric ID, timing line and text.")
        cue_id = int(lines[0].strip())
        match = TIMING.fullmatch(lines[1].strip())
        if not match or cue_id in seen:
            raise ValueError(f"Invalid timing or duplicate ID in cue {cue_id}.")
        start, end = seconds(match.groups()[:4]), seconds(match.groups()[4:])
        if end <= start:
            raise ValueError(f"Cue {cue_id} must end after it starts.")
        body = "\n".join(lines[2:]).strip()
        if not body:
            raise ValueError(f"Cue {cue_id} has no text.")
        cues.append(Cue(cue_id, start, end, body))
        seen.add(cue_id)
    return cues


def tokens(text: str) -> list[str]:
    # Ignore common subtitle presentation tags, punctuation and letter case.
    clean = re.sub(r"</?(?:b|i|u|font)(?:\s[^>]*)?>", "", text, flags=re.I)
    return [s.casefold().replace("’", "'") for s in TOKENS.findall(clean)]


def analyze(cues: list[Cue], words: list[Word], duration: float,
            max_cps: float = 20, drift: float = .6) -> list[dict]:
    """Return observable format checks and explicitly uncertain ASR comparisons."""
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError("Audio duration must be a finite positive number.")
    if not all(math.isfinite(v) for v in (max_cps, drift)) or max_cps <= 0 or drift < 0:
        raise ValueError("Thresholds must be positive (drift may be zero).")
    previous, previous_end = -1.0, -1.0
    for word in words:
        if (not all(math.isfinite(v) for v in (word.start, word.end, word.probability))
                or word.start < previous or word.end < previous_end or word.end < word.start or word.start < 0
                or not 0 <= word.probability <= 1):
            raise ValueError("Transcript words need ordered, finite times and probabilities in [0, 1].")
        previous = word.start
        previous_end = word.end
    issues = []

    def add(kind, cue, message, expected="", observed="", severity="check", start=None, end=None):
        issues.append(dict(kind=kind, severity=severity, cue_id=cue.id if cue else None,
                           start=cue.start if cue else start, end=cue.end if cue else end,
                           message=message, expected=expected, observed=observed))

    prior_end = -1.0
    for cue in cues:
        if cue.start < prior_end:
            add("overlap", cue, "This cue begins before an earlier cue has ended.")
        prior_end = max(prior_end, cue.end)
        if cue.end > duration + .1:
            add("past_audio_end", cue, "The cue extends beyond the audio duration.")
        chars = len(re.sub(r"<[^>]+>", "", cue.text).replace("\n", " "))
        cps = chars / (cue.end - cue.start)
        if cps > max_cps:
            add("reading_speed", cue, f"{cps:.1f} characters/second exceeds your {max_cps:g} threshold.")

    expected, owner, observed, word_index = [], [], [], []
    for ci, cue in enumerate(cues):
        cue_tokens = tokens(cue.text)
        expected.extend(cue_tokens)
        owner.extend([ci] * len(cue_tokens))
    for wi, word in enumerate(words):
        word_tokens = tokens(word.text)
        observed.extend(word_tokens)
        word_index.extend([wi] * len(word_tokens))
    if not observed:
        add("no_speech", None, "The model returned no speech. Listen to the audio; this is not proof of silence.",
            severity="review", start=0, end=duration)
        return issues

    # Identical repeated cues cannot be located reliably by global text order
    # alone. Expose the uncertainty rather than assigning a missing/timing error
    # to a specific occurrence without acoustic evidence.
    cue_tokens = [tuple(tokens(cue.text)) for cue in cues]
    counts = Counter(cue_tokens)
    ambiguous = {ci for ci, tok in enumerate(cue_tokens) if tok and counts[tok] > 1}
    for ci in sorted(ambiguous):
        add("ambiguous_alignment", cues[ci],
            "This caption repeats elsewhere. Listen to each occurrence; text alignment cannot reliably choose one.",
            cues[ci].text, severity="review")
    matched = {ci: [] for ci in range(len(cues))}
    for tag, a, b, c, d in SequenceMatcher(None, expected, observed, autojunk=False).get_opcodes():
        if tag == "equal":
            for ei, oi in zip(range(a, b), range(c, d)):
                matched[owner[ei]].append(word_index[oi])
        elif tag in ("replace", "delete"):
            affected = sorted(set(owner[a:b]))
            shared = len(affected) > 1 and tag == "replace"
            if shared:
                add("text_difference", None,
                    "A text difference spans multiple cues. This shared recognition span cannot be attributed to each cue separately.",
                    " ".join(expected[a:b]), " ".join(observed[c:d]), "review",
                    cues[affected[0]].start, cues[affected[-1]].end)
                continue
            for ci in affected:
                if ci in ambiguous:
                    continue
                add("text_difference", cues[ci],
                    "This caption fragment differs from speech recognition. Listen before editing; the model may be wrong.",
                    " ".join(expected[ei] for ei in range(a, b) if owner[ei] == ci),
                    " ".join(observed[c:d]) or "No recognized words aligned to this fragment", "review")
        elif tag == "insert":
            wi, wj = word_index[c], word_index[d - 1]
            add("uncovered_speech", None,
                "The model recognized words absent from the captions. Check for an omission or recognition error.",
                "No matching caption text", " ".join(observed[c:d]), "review",
                words[wi].start, words[wj].end)

    for ci, cue in enumerate(cues):
        if ci in ambiguous:
            continue
        indices = matched[ci]
        count = len(tokens(cue.text))
        if len(indices) >= 2 and len(indices) / max(count, 1) >= .6:
            start, end = words[min(indices)].start, words[max(indices)].end
            if abs(cue.start - start) > drift or abs(cue.end - end) > drift:
                add("timing_difference", cue,
                    f"Aligned speech is about {start:.2f}–{end:.2f}s; caption is {cue.start:.2f}–{cue.end:.2f}s. Review synchronization.",
                    cue.text, " ".join(words[i].text.strip() for i in sorted(set(indices))), "review")
        low = [words[i] for i in set(indices) if words[i].probability < .65]
        if low:
            add("uncertain_recognition", cue, "Some aligned words have low model probability. This score is not calibrated accuracy.",
                cue.text, " ".join(w.text.strip() for w in low), "review")
    return sorted(issues, key=lambda x: (x["start"] if x["start"] is not None else 0, x["kind"]))


def timestamp(value: float) -> str:
    ms = max(0, round(value * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def proposed_srt(words: list[Word]) -> str:
    """An editable ASR draft, never silently substituted for the input captions."""
    groups, current = [], []
    for word in words:
        text = " ".join(w.text.strip() for w in current + [word])
        if current and (len(text) > 80 or word.end - current[0].start > 6
                        or word.start - current[-1].end > .8):
            groups.append(current)
            current = []
        current.append(word)
    if current:
        groups.append(current)
    blocks = []
    for i, group in enumerate(groups, 1):
        text = " ".join(w.text.strip() for w in group)
        text = "\n".join(textwrap.wrap(text, width=42, break_long_words=False))
        start, end = group[0].start, max(group[0].start + .1, group[-1].end)
        blocks.append(f"{i}\n{timestamp(start)} --> {timestamp(end)}\n{text}")
    return "\n\n".join(blocks) + ("\n" if blocks else "")


def serialize(items):
    return [asdict(item) for item in items]
