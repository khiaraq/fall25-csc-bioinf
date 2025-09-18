# Week 1 AI Use

## ChatGPT (OpenAI GPT-5, September 2025)
- Helped me understand the assignment instructions
    - ie. "Here are the main points of this assignment: 
    [Assignment Description with sensitive information removed]
    Can you split this into different steps so that I can clearly see what needs to be done?" 
- Assisted in converting assembler from Python to Codon
    -ie. "Here is my Python code: [Python code]. Can you help me rewrite this in Codon so that it complies and produces the same output?"
- Provided guidance for setting up `evaluate.py`to run both Python and Codon automatically 
    - ie. "Can you help me start writing a Python script that will:
    1. run my assembler in Python
    2. run my assembler in Codon
    3. capture stdout/stderr to files
    4. compute N50 from contig lengths
    5. print a table of dataset/language/runtime/n50"
- Suggested edits to `evaluate.py` so stderr would print directly into CI logs
    - ie. "My GitHub Actions log only shows 'ERROR 0' when a command fails. Instead can I have it print the first ~50 lines of stderr to the CI log when a command crashes to make it easier to debug?"
- Translation of Zhongyu's Chen's original repository (Mandarin to English)
- At times, posted error messages to for guidance in what went wrong
    - ie. "Here is my error message: [error message]. What could be causing this?"
- Altogether, used for explaination, debugging help, and writing support
- All code in repo was run and tested by me to ensure it worked as required
- Final decisions on what to include in code and CI were made by me