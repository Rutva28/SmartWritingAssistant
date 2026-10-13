
import json
from pathlib import Path

import spacy

# Smart Reading & Writing Assistant
# Stage 3A: Semantic Analysis

PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

MODEL_NAME = "en_core_web_sm"


def load_nlp_model():
    """Load the spaCy English model."""
    try:
        return spacy.load(MODEL_NAME)
    except OSError as error:
        raise RuntimeError(
            "spaCy English model is missing. Run:\n"
            "python -m spacy download en_core_web_sm"
        ) from error


def extract_semantic_roles(sentence):
    """Extract basic who-did-what-to-whom information."""
    subject = None
    action = None
    objects = []
    indirect_objects = []
    locations = []

    # Find the main action and its subject.
    for token in sentence:
        if token.dep_ in {"ROOT", "conj"} and token.pos_ in {
            "VERB", "AUX"
        }:
            if action is None or token.dep_ == "ROOT":
                action = token.lemma_

        if token.dep_ in {"nsubj", "nsubjpass", "csubj"}:
            subject = token.text

        if token.dep_ in {"obj", "dobj", "attr", "oprd"}:
            objects.append(token.text)

        if token.dep_ in {"iobj", "dative"}:
            indirect_objects.append(token.text)

    # Extract prepositional phrases, such as "at the library".
    for token in sentence:
        if token.dep_ == "prep":
            phrase = " ".join(
                child.text
                for child in token.subtree
            )
            if phrase:
                locations.append(phrase)

    return {
        "sentence": sentence.text.strip(),
        "who": subject,
        "action": action,
        "what_or_whom": objects,
        "indirect_objects": indirect_objects,
        "prepositional_phrases": locations,
    }


def analyze_text(text, nlp):
    """Extract entities and semantic roles from the input."""
    doc = nlp(text)

    entities = [
        {
            "text": entity.text,
            "label": entity.label_,
            "description": spacy.explain(entity.label_)
            or entity.label_,
        }
        for entity in doc.ents
    ]

    semantic_frames = [
        extract_semantic_roles(sentence)
        for sentence in doc.sents
    ]

    return {
        "input_text": text,
        "named_entities": entities,
        "semantic_frames": semantic_frames,
    }


def main():
    nlp = load_nlp_model()

    sample_text = (
        "Rutva reads a book at the library. "
        "The teacher sends the report to the student."
    )

    result = analyze_text(sample_text, nlp)

    print("=" * 65)
    print("SMART READING & WRITING ASSISTANT")
    print("STAGE 3A: SEMANTIC ANALYSIS")
    print("=" * 65)

    print("\nInput text:")
    print(result["input_text"])

    print("\nNamed entities:")
    if result["named_entities"]:
        for entity in result["named_entities"]:
            print(
                f"- {entity['text']}: "
                f"{entity['description']}"
            )
    else:
        print("- No named entities detected.")

    print("\nSemantic frames:")
    for number, frame in enumerate(
        result["semantic_frames"], start=1
    ):
        print(f"\nSentence {number}: {frame['sentence']}")
        print(f"Who: {frame['who']}")
        print(f"Action: {frame['action']}")
        print(f"What or whom: {frame['what_or_whom']}")
        print(f"Indirect objects: {frame['indirect_objects']}")
        print(
            "Prepositional phrases: "
            f"{frame['prepositional_phrases']}"
        )

    output_path = OUTPUT_DIR / "semantic_results.json"
    output_path.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\nJSON results saved to:")
    print(output_path)


if __name__ == "__main__":
    main()
