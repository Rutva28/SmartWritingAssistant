
import re

# Smart Reading & Writing Assistant
# Stage 2B: Custom CFG Parser
# Recursive-descent parser implemented from scratch.

# 15 CFG grammar rules
GRAMMAR_RULES = [
    "S  -> NP VP",
    "NP -> Det N",
    "NP -> Det Adj N",
    "NP -> Det N N",
    "NP -> N N",
    "NP -> Pronoun",
    "NP -> ProperNoun",
    "VP -> Verb",
    "VP -> Verb NP",
    "VP -> Verb PP",
    "VP -> Verb NP PP",
    "PP -> Prep NP",
    "Det -> the | a | an",
    "Pronoun -> i | you | he | she | they | we",
    "N / Adj / Verb / Prep / ProperNoun -> lexical categories",
]

# Vocabulary used by the custom grammar
LEXICON = {
    "det": {"the", "a", "an"},

    "adj": {
        "good", "small", "large", "beautiful", "smart"
    },

    "n": {
        "student", "teacher", "book", "dog", "cat", "apple",
        "computer", "engineering", "school", "library", "report",
        "assignment", "robot", "file", "room"
    },

    "pronoun": {
        "i", "you", "he", "she", "they", "we"
    },

    "verb": {
        "read", "reads", "write", "writes", "like", "likes",
        "see", "sees", "study", "studies", "send", "sends",
        "eat", "eats", "run", "runs", "is", "are", "was",
        "were", "work", "works", "help", "helps"
    },

    "prep": {
        "in", "on", "at", "with", "to", "from", "under"
    },

    "proper": {
        "rutva", "ahmedabad", "india", "john", "mary"
    }
}


def tokenize(sentence):
    """Convert a sentence into lowercase words."""
    return re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", sentence.lower())


class CFGParser:
    def __init__(self, words):
        self.words = words
        self.position = 0

    def current(self):
        if self.position >= len(self.words):
            return None
        return self.words[self.position]

    def match_category(self, category):
        """Match the current word to a lexical category."""
        word = self.current()

        if word is not None and word in LEXICON[category]:
            self.position += 1
            return (category.upper(), word)

        return None

    def parse_np(self):
        """
        NP rules:
        NP -> Det N
        NP -> Det Adj N
        NP -> Det N N
        NP -> N N
        NP -> Pronoun
        NP -> ProperNoun
        """
        start = self.position

        # NP -> Pronoun
        node = self.match_category("pronoun")
        if node:
            return ("NP", node)

        self.position = start

        # NP -> ProperNoun
        node = self.match_category("proper")
        if node:
            return ("NP", node)

        self.position = start

        # NP -> N N, e.g. "computer engineering"
        noun1 = self.match_category("n")

        if noun1:
            after_noun1 = self.position
            noun2 = self.match_category("n")

            if noun2:
                return ("NP", noun1, noun2)

            # This grammar does not allow a bare single noun as NP.
            self.position = start

        # NP -> Det N | Det Adj N | Det N N
        self.position = start
        det = self.match_category("det")

        if det is None:
            self.position = start
            return None

        after_det = self.position

        # Try NP -> Det Adj N
        adj = self.match_category("adj")

        if adj:
            noun = self.match_category("n")

            if noun:
                return ("NP", det, adj, noun)

        # Try NP -> Det N or Det N N
        self.position = after_det
        noun1 = self.match_category("n")

        if noun1:
            after_noun1 = self.position
            noun2 = self.match_category("n")

            if noun2:
                return ("NP", det, noun1, noun2)

            self.position = after_noun1
            return ("NP", det, noun1)

        self.position = start
        return None

    def parse_pp(self):
        """PP -> Prep NP."""
        start = self.position

        prep = self.match_category("prep")

        if prep is None:
            return None

        np = self.parse_np()

        if np is None:
            self.position = start
            return None

        return ("PP", prep, np)

    def parse_vp(self):
        """
        VP rules:
        VP -> Verb
        VP -> Verb NP
        VP -> Verb PP
        VP -> Verb NP PP
        """
        start = self.position
        verb = self.match_category("verb")

        if verb is None:
            return None

        after_verb = self.position

        # Try VP -> Verb NP or Verb NP PP
        np = self.parse_np()

        if np:
            after_np = self.position
            pp = self.parse_pp()

            if pp:
                return ("VP", verb, np, pp)

            self.position = after_np
            return ("VP", verb, np)

        # Try VP -> Verb PP
        self.position = after_verb
        pp = self.parse_pp()

        if pp:
            return ("VP", verb, pp)

        # VP -> Verb
        self.position = after_verb
        return ("VP", verb)

    def parse(self):
        """Parse S -> NP VP and require all words to be consumed."""
        self.position = 0

        np = self.parse_np()

        if np is None:
            return None

        vp = self.parse_vp()

        if vp is None:
            return None

        if self.position != len(self.words):
            return None

        return ("S", np, vp)


def print_tree(node, indent=0):
    """Display the parse tree using indentation."""
    prefix = "  " * indent

    if isinstance(node, tuple):
        print(prefix + str(node[0]))

        for child in node[1:]:
            print_tree(child, indent + 1)
    else:
        print(prefix + str(node))


def main():
    print("=" * 60)
    print("SMART READING & WRITING ASSISTANT")
    print("STAGE 2B: CUSTOM CFG PARSER")
    print("=" * 60)

    print("\nGrammar rules:")

    for number, rule in enumerate(GRAMMAR_RULES, start=1):
        print(f"{number}. {rule}")

    examples = [
        "The student reads the book.",
        "A smart student reads a book.",
        "Rutva studies computer engineering.",
        "The teacher works in the school.",
        "She writes the report.",
    ]

    accepted = 0

    for sentence in examples:
        print("\n" + "-" * 60)
        print("Sentence:", sentence)

        words = tokenize(sentence)
        parser = CFGParser(words)
        tree = parser.parse()

        if tree:
            accepted += 1
            print("Result: Sentence accepted by the custom grammar.")
            print("Parse tree:")
            print_tree(tree)
        else:
            print("Result: Sentence not accepted by the custom grammar.")
            print(
                "This grammar supports a limited vocabulary "
                "and sentence structure."
            )

    print("\n" + "=" * 60)
    print(f"SUMMARY: {accepted}/{len(examples)} sentences accepted")
    print("=" * 60)


if __name__ == "__main__":
    main()
