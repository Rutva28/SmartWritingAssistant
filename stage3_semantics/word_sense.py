
import json
import re
from pathlib import Path

import nltk
from nltk.corpus import wordnet as wn

# Smart Reading & Writing Assistant
# Stage 3B: Word-Sense Disambiguation (WSD)

PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

TARGET_WORDS = {"bank", "bat", "light"}


def tokenize(text):
    """Convert text into a set of lowercase words."""
    return set(re.findall(r"[a-z]+", text.lower()))


def ensure_wordnet():
    """Check whether the WordNet corpus is available."""
    try:
        wn.synsets("bank")
    except LookupError:
        print("WordNet data is missing.")
        print("Run these commands in PowerShell:")
        print('python -c "import nltk; nltk.download(\'wordnet\')"')
        print('python -c "import nltk; nltk.download(\'omw-1.4\')"')
        raise SystemExit(1)


def lesk_disambiguate(sentence, target_word):
    """Choose the WordNet sense with the highest context overlap."""
    context_words = tokenize(sentence)
    context_words.discard(target_word.lower())

    synsets = wn.synsets(target_word)

    if not synsets:
        return {
            "word": target_word,
            "sentence": sentence,
            "selected_sense": None,
            "definition": "No WordNet senses found.",
            "overlap_score": 0,
        }

    best_synset = None
    best_score = -1

    for synset in synsets:
        # Use the definition and example sentences as context.
        gloss = synset.definition()
        gloss += " " + " ".join(synset.examples())

        gloss_words = tokenize(gloss)
        score = len(context_words.intersection(gloss_words))

        if score > best_score:
            best_score = score
            best_synset = synset

    return {
        "word": target_word,
        "sentence": sentence,
        "selected_sense": (
            best_synset.name() if best_synset else None
        ),
        "definition": (
            best_synset.definition() if best_synset else None
        ),
        "example_sentences": (
            list(best_synset.examples()) if best_synset else []
        ),
        "overlap_score": max(best_score, 0),
    }


def analyze_text(text):
    """Disambiguate occurrences of bank, bat, and light."""
    ensure_wordnet()

    results = []

    for sentence in re.split(r"(?<=[.!?])\s+", text.strip()):
        if not sentence:
            continue

        words = tokenize(sentence)

        for target in sorted(TARGET_WORDS.intersection(words)):
            results.append(
                lesk_disambiguate(sentence, target)
            )

    return {
        "input_text": text,
        "method": "Simplified Lesk-style WordNet gloss overlap",
        "word_senses": results,
    }


def main():
    sample_texts = [
        "She deposited money at the bank.",
        "They sat on the river bank.",
        "The cricket player hit the ball with a bat.",
        "A bat flew out of the cave at night.",
        "Please turn on the light in the room.",
        "This bag is very light to carry.",
    ]

    combined_results = []

    print("=" * 65)
    print("SMART READING & WRITING ASSISTANT")
    print("STAGE 3B: WORD-SENSE DISAMBIGUATION")
    print("=" * 65)

    for sentence in sample_texts:
        result = analyze_text(sentence)
        combined_results.extend(result["word_senses"])

        print("\nSentence:", sentence)

        for sense in result["word_senses"]:
            print("Word:", sense["word"])
            print("Selected sense:", sense["selected_sense"])
            print("Definition:", sense["definition"])
            print("Overlap score:", sense["overlap_score"])

    output = {
        "method": "Simplified Lesk-style WordNet gloss overlap",
        "results": combined_results,
    }

    output_path = OUTPUT_DIR / "word_sense_results.json"
    output_path.write_text(
        json.dumps(output, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\nJSON results saved to:")
    print(output_path)


if __name__ == "__main__":
    main()
