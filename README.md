\# Smart Reading \& Writing Assistant



A Natural Language Processing (NLP) project that analyzes and improves text through spell checking, syntactic processing, semantic analysis, and discourse understanding. The system integrates five stages into a single pipeline to process input text and generate structured results.



\## Features



\- \*\*Stage 1 – Spell Checking:\*\* Uses Levenshtein distance, word frequencies, and contextual rules to identify and correct spelling mistakes.

\- \*\*Stage 2 – Syntactic Processing:\*\* Uses spaCy for sentence and dependency analysis and a custom Context-Free Grammar (CFG) parser for parsing sentences.

\- \*\*Stage 3 – Semantic Analysis:\*\* Extracts named entities and semantic roles and performs word-sense disambiguation for ambiguous words such as \*bank\*, \*bat\*, and \*light\*.

\- \*\*Stage 4 – Discourse and Pragmatics:\*\* Identifies discourse relations, estimates coreference links, and detects possible indirect or polite requests.

\- \*\*Stage 5 – Integrated Pipeline:\*\* Combines the previous stages and processes ten sample sentences, producing structured JSON results and a summary.



\## Project Structure



```text

SmartWritingAssistant/

├── main.py

├── pipeline.py

├── requirements.txt

├── README.md

├── stage1\_spellcheck/

│   └── spell\_checker.py

├── stage2\_syntax/

│   ├── syntax\_processor.py

│   └── custom\_parser.py

├── stage3\_semantics/

│   ├── semantic\_analyzer.py

│   └── word\_sense.py

├── stage4\_discourse/

│   └── discourse\_processor.py

├── data/

│   └── test\_samples.json

└── outputs/

&#x20;   ├── pipeline\_results.json

&#x20;   ├── summary\_table.json

&#x20;   ├── syntax\_results.json

&#x20;   ├── semantic\_results.json

&#x20;   ├── word\_sense\_results.json

&#x20;   └── discourse\_results.json

```



\*Note: The files listed inside `outputs/` are generated when the corresponding scripts run. Your local folder may contain additional output files.\*



\## Technologies Used



\- Python

\- spaCy

\- NLTK

\- WordNet

\- Natural Language Processing (NLP)

\- Context-Free Grammar (CFG)

\- JSON



\## Installation



\### 1. Clone the repository



```bash

git clone https://github.com/YOUR-USERNAME/SmartWritingAssistant.git

cd SmartWritingAssistant

```



Replace `YOUR-USERNAME` with your GitHub username.



\### 2. Create a virtual environment



```bash

python -m venv .venv

```



Activate it on Windows PowerShell:



```powershell

.\\.venv\\Scripts\\Activate.ps1

```



\### 3. Install dependencies



```bash

pip install -r requirements.txt

```



\### 4. Download the spaCy English model



```bash

python -m spacy download en\_core\_web\_sm

```



If WordNet data is not already available, run:



```python

import nltk

nltk.download("wordnet")

nltk.download("omw-1.4")

```



Save those three lines in a temporary Python file or run them in a Python interpreter.



\## How to Run



Run the complete five-stage pipeline:



```bash

python pipeline.py

```



Run an individual stage when needed:



```bash

python stage1\_spellcheck/spell\_checker.py

python stage2\_syntax/syntax\_processor.py

python stage3\_semantics/semantic\_analyzer.py

python stage3\_semantics/word\_sense.py

python stage4\_discourse/discourse\_processor.py

```



The custom CFG parser can also be tested separately according to its implementation.



\## Output



The pipeline generates structured results in JSON format, including:



\- Original and corrected text.

\- Spelling correction information.

\- Syntactic analysis results.

\- Named entities and semantic frames.

\- Word-sense disambiguation results.

\- Coreference estimates and discourse relations.

\- A summary of the ten test samples.



Generated files are saved in the `outputs/` directory.



\## Testing



The pipeline has been run on ten sample sentences covering library reading, teacher-student communication, causal and contrastive connectives, polite requests, and the ambiguous words \*bank\*, \*bat\*, and \*light\*.



The current implementation runs through all ten samples. However, word-sense disambiguation and coreference resolution are baseline implementations and may not always produce the correct interpretation. The custom parser and its grammar coverage should be validated against the assignment's required test cases.



\## Limitations



\- Spell correction depends on the vocabulary, frequency scores, and contextual rules implemented in the project.

\- The custom CFG parser supports only the grammar rules and vocabulary defined in its code.

\- Word-sense disambiguation may choose an incorrect meaning in some contexts.

\- Coreference resolution uses heuristics and is not a complete linguistic coreference system.

\- Semantic role extraction depends on the output of the NLP model.



\## Future Improvements



\- Improve context-aware spelling correction.

\- Expand CFG grammar rules and parser coverage.

\- Improve word-sense disambiguation using contextual information.

\- Enhance coreference resolution and semantic role extraction.

\- Add a graphical user interface for interactive text processing.



\## Author



\*\*Rutva Kikani\*\*



\## License



This project was developed for educational and academic purposes. Add a suitable open-source license if you intend to distribute the project for reuse.

