
import json
from pathlib import Path

PRONOUNS = {
    "he", "him", "his",
    "she", "her", "hers",
    "they", "them", "their",
    "it", "its"
}


def load_nlp_model():
    import spacy
    return spacy.load("en_core_web_sm")


def split_sentences(text, nlp):
    doc = nlp(text)
    return [sentence.text.strip() for sentence in doc.sents]


def resolve_coreferences(text, nlp):
    """
    Simple rule-based coreference resolution.
    Links pronouns to recent compatible mentions where possible.
    This is a heuristic, not a full coreference model.
    """
    doc = nlp(text)
    antecedents = []
    chains = []

    for sentence in doc.sents:
        tokens = list(sentence)

        # Remember proper nouns as possible people.
        for token in tokens:
            if token.pos_ == "PROPN":
                antecedents.append({
                    "text": token.text,
                    "type": "PERSON",
                    "sentence_start": sentence.start
                })

        # Remember named entities that are not people.
        for entity in doc.ents:
            if (
                entity.start >= sentence.start
                and entity.end <= sentence.end
                and entity.label_ != "PERSON"
            ):
                antecedents.append({
                    "text": entity.text,
                    "type": "ENTITY",
                    "sentence_start": sentence.start
                })

        # Try to link pronouns to earlier mentions.
        for token in tokens:
            pronoun = token.text.lower()

            if pronoun not in PRONOUNS:
                continue

            candidate = None

            for antecedent in reversed(antecedents):
                if antecedent["sentence_start"] > sentence.start:
                    continue

                if pronoun in {
                    "he", "him", "his",
                    "she", "her", "hers"
                }:
                    if antecedent["type"] == "PERSON":
                        candidate = antecedent
                        break

                elif pronoun in {"they", "them", "their"}:
                    if antecedent["type"] in {
                        "PERSON", "ENTITY", "NOUN"
                    }:
                        candidate = antecedent
                        break

                elif pronoun in {"it", "its"}:
                    if antecedent["type"] in {"ENTITY", "NOUN"}:
                        candidate = antecedent
                        break

            if candidate:
                chains.append({
                    "antecedent": candidate["text"],
                    "pronoun": token.text,
                    "sentence": sentence.text.strip(),
                    "method": "recent-mention heuristic"
                })

        # Remember common nouns for later sentences.
        for token in tokens:
            if (
                token.pos_ == "NOUN"
                and token.dep_ in {"nsubj", "dobj", "obj", "pobj"}
            ):
                antecedents.append({
                    "text": token.text,
                    "type": "NOUN",
                    "sentence_start": sentence.start
                })

        antecedents = antecedents[-30:]

    return {
        "coreference_chains": chains,
        "note": (
            "Coreference links are heuristic predictions "
            "and may be incorrect."
        )
    }


def detect_connectives(text):
    """Detect common discourse connectives and their relationships."""
    import re

    patterns = [
        (r"\bhowever\b", "contrast"),
        (r"\btherefore\b", "result"),
        (r"\bbecause\b", "reason"),
        (r"\balthough\b", "concession"),
        (r"\bbut\b", "contrast"),
        (r"\bso\b", "result"),
        (r"\bmoreover\b", "addition"),
        (r"\bfurthermore\b", "addition")
    ]

    relations = []

    for pattern, relation_type in patterns:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            relations.append({
                "connective": match.group(0),
                "relation": relation_type,
                "position": match.start()
            })

    relations.sort(key=lambda item: item["position"])

    # Remove the internal position from the public result.
    for relation in relations:
        relation.pop("position", None)

    return relations


def infer_indirect_requests(text):
    """Identify common polite requests using simple text patterns."""
    import re

    patterns = [
        r"\bcould you\b",
        r"\bwould you\b",
        r"\bcan you\b",
        r"\bwould you mind\b",
        r"\bcould you please\b",
        r"\bplease\b"
    ]

    requests = []

    for sentence in re.split(r"(?<=[.!?])\s+", text.strip()):
        if not sentence:
            continue

        lowered = sentence.lower()

        if any(re.search(pattern, lowered) for pattern in patterns):
            requests.append({
                "text": sentence,
                "inferred_intent": "Polite request",
                "method": "rule-based pattern matching"
            })

    return requests


def process_discourse(text, nlp):
    """Run the complete Stage 4 discourse analysis."""
    return {
        "input_text": text,
        "sentences": split_sentences(text, nlp),
        "coreference": resolve_coreferences(text, nlp),
        "discourse_relations": detect_connectives(text),
        "indirect_requests": infer_indirect_requests(text)
    }


def main():
    nlp = load_nlp_model()

    sample_text = (
        "Rutva studied for the exam because she wanted a good result. "
        "However, the exam was difficult. "
        "Therefore, she reviewed her notes. "
        "Could you explain the difficult question?"
    )

    results = process_discourse(sample_text, nlp)

    print("\nSTAGE 4: DISCOURSE AND PRAGMATICS")
    print("=" * 45)
    print(json.dumps(results, indent=4, ensure_ascii=False))

    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "discourse_results.json"
    with output_file.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)

    print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    main()
