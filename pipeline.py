
import json
import inspect
import importlib
from pathlib import Path

import spacy

from stage2_syntax.syntax_processor import process_sentence
from stage3_semantics.semantic_analyzer import analyze_text as analyze_semantics
from stage3_semantics.word_sense import analyze_text as analyze_word_senses
from stage4_discourse.discourse_processor import process_discourse

PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

MODEL_NAME = "en_core_web_sm"


def load_nlp():
    """Load spaCy once and reuse it for every stage."""
    return spacy.load(MODEL_NAME)


def run_spell_checker(text):
    """
    Connect to the existing Stage 1 spell checker.

    Recognized function names:
    correct_text, correct_spelling, spell_check,
    check_text, process_text.
    """
    module = importlib.import_module(
        "stage1_spellcheck.spell_checker"
    )

    function_names = [
        "correct_text",
        "correct_spelling",
        "spell_check",
        "check_text",
        "process_text",
    ]

    for name in function_names:
        function = getattr(module, name, None)

        if callable(function):
            result = function(text)
            return normalize_spell_result(result, text)

    # Try common class-based interfaces.
    for class_name in ["SpellChecker", "SpellCheckerEngine"]:
        checker_class = getattr(module, class_name, None)

        if checker_class is None:
            continue

        checker = checker_class()

        for method_name in [
            "correct_text",
            "correct_spelling",
            "correct",
            "spell_check",
            "check_text",
        ]:
            method = getattr(checker, method_name, None)

            if callable(method):
                result = method(text)
                return normalize_spell_result(result, text)

    raise RuntimeError(
        "Could not find a callable spell-checking function in "
        "stage1_spellcheck/spell_checker.py. "
        "Please share that file's code so the pipeline can use "
        "your exact Stage 1 interface."
    )


def normalize_spell_result(result, original_text):
    """Convert common spell-checker return types to a text string."""
    if isinstance(result, str):
        return result

    if isinstance(result, dict):
        for key in [
            "corrected_text",
            "corrected",
            "text",
            "result",
        ]:
            if isinstance(result.get(key), str):
                return result[key]

    raise TypeError(
        "The spell checker returned an unsupported result type: "
        f"{type(result).__name__}. "
        "Expected corrected text as a string or dictionary."
    )


def process(raw_text, nlp):
    """Run the full reading and writing analysis pipeline."""
    corrected_text = run_spell_checker(raw_text)

    syntax_results = process_sentence(corrected_text, nlp)
    semantic_results = analyze_semantics(corrected_text, nlp)
    word_sense_results = analyze_word_senses(corrected_text)
    discourse_results = process_discourse(corrected_text, nlp)

    return {
        "raw_text": raw_text,
        "corrected_text": corrected_text,
        "syntax_results": syntax_results,
        "semantic_frames": semantic_results["semantic_frames"],
        "named_entities": semantic_results["named_entities"],
        "word_senses": word_sense_results["word_senses"],
        "discourse_relations": discourse_results["discourse_relations"],
        "coreference_chains": (
            discourse_results["coreference"]["coreference_chains"]
        ),
        "indirect_requests": discourse_results["indirect_requests"],
    }


def summarize_result(result):
    """Create one summary row for a processed text."""
    return {
        "corrections": int(
            result["raw_text"] != result["corrected_text"]
        ),
        "entities": len(result["named_entities"]),
        "coreference_chains": len(result["coreference_chains"]),
        "discourse_relations": len(result["discourse_relations"]),
    }


def run_batch():
    """Run the pipeline on the 10 assignment samples."""
    nlp = load_nlp()

    samples_path = PROJECT_DIR / "data" / "test_samples.json"
    samples = json.loads(samples_path.read_text(encoding="utf-8"))

    all_results = []
    summary_rows = []

    for sample in samples:
        print("\n" + "=" * 65)
        print(f"PROCESSING SAMPLE {sample['id']}")
        print("=" * 65)

        result = process(sample["text"], nlp)
        row = {
            "sample_id": sample["id"],
            **summarize_result(result),
        }

        all_results.append({
            "sample_id": sample["id"],
            **result,
        })
        summary_rows.append(row)

        print("Original:", result["raw_text"])
        print("Corrected:", result["corrected_text"])
        print("Named entities:", len(result["named_entities"]))
        print("Semantic frames:", len(result["semantic_frames"]))
        print("Word senses:", len(result["word_senses"]))
        print("Coreference chains:", len(result["coreference_chains"]))
        print("Discourse relations:", len(result["discourse_relations"]))
        print("Indirect requests:", len(result["indirect_requests"]))

    results_path = OUTPUT_DIR / "pipeline_results.json"
    results_path.write_text(
        json.dumps(all_results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    summary_path = OUTPUT_DIR / "summary_table.json"
    summary_path.write_text(
        json.dumps(summary_rows, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\n" + "=" * 90)
    print("10-SAMPLE SUMMARY")
    print("=" * 90)
    print(
        f"{'ID':<6}{'Corrections':<15}{'Entities':<12}"
        f"{'Coreference':<15}{'Relations':<12}"
    )

    for row in summary_rows:
        print(
            f"{row['sample_id']:<6}"
            f"{row['corrections']:<15}"
            f"{row['entities']:<12}"
            f"{row['coreference_chains']:<15}"
            f"{row['discourse_relations']:<12}"
        )

    print("\nFull results saved to:", results_path)
    print("Summary saved to:", summary_path)


if __name__ == "__main__":
    run_batch()
