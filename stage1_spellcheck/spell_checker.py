
import re

# ============================================================
# SMART READING & WRITING ASSISTANT
# Stage 1: Spell Checker
# Student: Rutva Kikani
# ============================================================

# Word-frequency dictionary.
# Higher values represent more common words.
WORD_FREQUENCY = {
    "a": 1000, "about": 300, "after": 300, "again": 200,
    "all": 500, "also": 300, "am": 500, "an": 600,
    "and": 1000, "are": 1000, "as": 900, "at": 900,
    "bad": 100, "bank": 150, "bat": 100, "be": 900,
    "because": 500, "been": 500, "before": 300, "best": 200,
    "book": 300, "but": 1000, "by": 900, "can": 900,
    "cannot": 200, "class": 300, "come": 400, "could": 600,
    "correct": 200, "day": 500, "did": 700, "do": 1000,
    "does": 700, "done": 300, "easy": 200, "email": 200,
    "enough": 300, "every": 400, "exam": 500, "file": 300,
    "find": 400, "for": 1000, "from": 900, "get": 800,
    "give": 700, "go": 800, "going": 900, "good": 500,
    "grammar": 200, "great": 300, "had": 800, "has": 900,
    "have": 1000, "he": 1000, "help": 400, "her": 800,
    "here": 500, "him": 800, "his": 900, "home": 300,
    "how": 900, "i": 1000, "if": 900, "in": 1000,
    "information": 400, "is": 1000, "it": 1000, "its": 400,
    "know": 700, "language": 200, "late": 300, "learn": 300,
    "library": 500, "light": 150, "like": 700, "make": 800,
    "many": 600, "me": 900, "misspelled": 50, "more": 900,
    "much": 800, "my": 900, "need": 800, "new": 700,
    "not": 1000, "of": 1000, "on": 1000, "one": 900,
    "or": 1000, "our": 900, "paragraph": 100, "people": 700,
    "please": 500, "project": 400, "read": 600, "reading": 300,
    "right": 600, "said": 800, "school": 400, "send": 500,
    "sentence": 300, "she": 1000, "should": 800, "some": 900,
    "spell": 100, "student": 500, "students": 400, "study": 400,
    "teacher": 500, "text": 500, "than": 800,
    "that": 1000, "the": 1000, "their": 700, "them": 800,
    "then": 800, "there": 900, "these": 800, "they": 1000,
    "thing": 500, "think": 700, "this": 1000, "time": 900,
    "to": 1000, "too": 800, "two": 800, "understand": 400,
    "up": 900, "use": 900, "very": 900, "was": 1000,
    "we": 1000, "welcome": 500, "were": 900, "what": 1000,
    "when": 900, "where": 900, "which": 900, "who": 900,
    "will": 1000, "with": 1000, "word": 700, "work": 700,
    "write": 700, "writing": 500, "wrong": 300, "you": 1000,
    "your": 900, "you're": 500, "they're": 500,
    "assignment": 300, "computer": 300, "today": 500,
    "tomorrow": 300, "finished": 300, "report": 500,
    "meeting": 300, "happy": 300, "went": 500,
    "student's": 100, "beautiful": 200, "important": 400,

    # Words used by the test samples
    "reads": 400, "sends": 400, "studied": 400,
    "hard": 500, "marks": 400, "wanted": 400,
    "deposited": 300, "money": 700, "cricket": 200,
    "player": 400, "hit": 500, "ball": 600,
    "writes": 400, "notes": 500, "reviewed": 300,
    "felt": 500, "prepared": 300, "difficult": 400,
    "question": 500, "explain": 400, "turn": 500,
    "room": 500, "at": 900, "river": 300, "financial": 200,
    "institution": 100, "she": 1000, "he": 1000,
    "they": 1000, "their": 700, "her": 800,
    "his": 900, "it": 1000, "on": 1000,
    "in": 1000, "bank": 150, "bat": 100,
    "cricket": 200, "player": 400, "ball": 600,
}

# Common neighboring-word patterns.
BIGRAM_FREQUENCY = {
    ("in", "the"): 900,
    ("on", "the"): 850,
    ("to", "the"): 800,
    ("for", "the"): 800,
    ("of", "the"): 950,
    ("they", "are"): 800,
    ("there", "is"): 800,
    ("there", "are"): 800,
    ("their", "book"): 500,
    ("their", "work"): 400,
    ("your", "book"): 400,
    ("you", "are"): 800,
    ("you're", "welcome"): 700,
    ("too", "much"): 700,
    ("two", "students"): 400,
    ("a", "book"): 500,
    ("a", "good"): 600,
    ("is", "a"): 900,
    ("it", "is"): 900,
    ("it", "was"): 800,
    ("could", "you"): 800,
    ("please", "send"): 700,
    ("read", "the"): 500,
    ("write", "the"): 500,
    ("the", "student"): 500,
    ("the", "teacher"): 500,
    ("the", "computer"): 400,
}


def levenshtein_distance(word1, word2):
    """Calculate edit distance using dynamic programming."""
    word1 = word1.lower()
    word2 = word2.lower()

    rows = len(word1) + 1
    cols = len(word2) + 1
    matrix = [[0] * cols for _ in range(rows)]

    for i in range(rows):
        matrix[i][0] = i

    for j in range(cols):
        matrix[0][j] = j

    for i in range(1, rows):
        for j in range(1, cols):
            cost = 0 if word1[i - 1] == word2[j - 1] else 1

            matrix[i][j] = min(
                matrix[i - 1][j] + 1,
                matrix[i][j - 1] + 1,
                matrix[i - 1][j - 1] + cost,
            )

    return matrix[-1][-1]


def preserve_case(original, replacement):
    """Preserve the capitalization of the original word."""
    if original.isupper():
        return replacement.upper()

    if original.istitle():
        return replacement.capitalize()

    return replacement


def get_candidates(word, max_distance=2):
    """Find dictionary words with a small edit distance."""
    word = word.lower()
    allowed_distance = 1 if len(word) <= 4 else max_distance
    candidates = []

    for dictionary_word, frequency in WORD_FREQUENCY.items():
        if dictionary_word == word:
            continue

        distance = levenshtein_distance(word, dictionary_word)

        if 0 < distance <= allowed_distance:
            candidates.append({
                "word": dictionary_word,
                "distance": distance,
                "frequency": frequency,
            })

    return candidates


def context_score(candidate, previous_word, next_word):
    """Rank possible corrections using frequency and context."""
    word = candidate["word"]
    score = candidate["frequency"] / 1000.0

    if previous_word:
        score += BIGRAM_FREQUENCY.get(
            (previous_word.lower(), word), 0
        ) / 100.0

    if next_word:
        score += BIGRAM_FREQUENCY.get(
            (word, next_word.lower()), 0
        ) / 100.0

    score -= candidate["distance"] * 0.25
    return score


def suggest_correction(word, previous_word=None, next_word=None):
    """Suggest a correction for a word not in the dictionary."""
    # Never replace a word already recognized by the dictionary.
    if word.lower() in WORD_FREQUENCY:
        return word, None

    candidates = get_candidates(word)

    if not candidates:
        return word, None

    for candidate in candidates:
        candidate["score"] = context_score(
            candidate, previous_word, next_word
        )

    candidates.sort(
        key=lambda item: (
            item["score"],
            item["frequency"],
            -item["distance"],
        ),
        reverse=True,
    )

    best = candidates[0]
    corrected = preserve_case(word, best["word"])

    explanation = (
        f"Edit distance = {best['distance']}; "
        f"frequency = {best['frequency']}; "
        f"context score = {best['score']:.2f}"
    )

    return corrected, explanation


def correct_confusable_words(words):
    """Handle a few common context-dependent word mistakes."""
    changes = []

    for i, word in enumerate(words):
        current = word.lower()
        following = words[i + 1].lower() if i + 1 < len(words) else ""
        replacement = None
        reason = None

        if current == "their" and following in {
            "going", "coming", "working", "playing"
        }:
            replacement = "they're"
            reason = "'They're' means 'they are' in this context."

        elif current == "there" and following in {
            "book", "car", "house", "assignment", "computer", "work"
        }:
            replacement = "their"
            reason = "'Their' indicates possession in this context."

        elif current == "your" and following == "welcome":
            replacement = "you're"
            reason = "'You're welcome' means 'you are welcome'."

        elif current == "to" and following in {"much", "many"}:
            replacement = "too"
            reason = "'Too' means excessively or additionally."

        if replacement:
            changes.append({
                "index": i,
                "original": word,
                "corrected": preserve_case(word, replacement),
                "distance": levenshtein_distance(word, replacement),
                "reason": reason,
            })

    return changes


def process_text(text):
    """Correct a paragraph and report each suggested correction."""
    tokens = re.findall(
        r"[A-Za-z]+(?:'[A-Za-z]+)?|[^A-Za-z]+", text
    )

    word_positions = [
        i for i, token in enumerate(tokens)
        if re.fullmatch(r"[A-Za-z]+(?:'[A-Za-z]+)?", token)
    ]

    original_words = [tokens[i] for i in word_positions]
    contextual_changes = correct_confusable_words(original_words)

    contextual_by_index = {
        item["index"]: item for item in contextual_changes
    }

    changes = []

    for word_index, token_index in enumerate(word_positions):
        original = original_words[word_index]

        if word_index in contextual_by_index:
            item = contextual_by_index[word_index]
            tokens[token_index] = item["corrected"]

            changes.append({
                "original": item["original"],
                "corrected": item["corrected"],
                "edit_distance": item["distance"],
                "reason": item["reason"],
            })
            continue

        previous_word = (
            original_words[word_index - 1]
            if word_index > 0 else None
        )
        next_word = (
            original_words[word_index + 1]
            if word_index + 1 < len(original_words) else None
        )

        corrected, explanation = suggest_correction(
            original, previous_word, next_word
        )

        if corrected.lower() != original.lower():
            tokens[token_index] = corrected

            changes.append({
                "original": original,
                "corrected": corrected,
                "edit_distance": levenshtein_distance(
                    original, corrected
                ),
                "reason": explanation,
            })

    corrected_text = "".join(tokens)

    return {
        "original_text": text,
        "corrected_text": corrected_text,
        "changes": changes,
        "correction_count": len(changes),
    }


if __name__ == "__main__":
    print("=" * 60)
    print("SMART READING & WRITING ASSISTANT")
    print("STAGE 1: SPELL CHECKER")
    print("=" * 60)

    sample = (
        "Their going to the libary. "
        "I need to reed the assigment and send it to the teacher."
    )

    result = process_text(sample)

    print("\nOriginal text:")
    print(result["original_text"])

    print("\nCorrected text:")
    print(result["corrected_text"])

    print("\nChanges made:")

    if result["changes"]:
        for number, change in enumerate(result["changes"], start=1):
            print(
                f"{number}. {change['original']} -> "
                f"{change['corrected']}"
            )
            print(f"   Reason: {change['reason']}")
    else:
        print("No corrections suggested.")

    print(f"\nTotal corrections: {result['correction_count']}")
