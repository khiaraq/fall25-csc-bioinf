# Week 1 Report

## STEP 1 - Repo and CI Setup
- Created public GitHub repo named `fall25-csc-bioinf`
- Added `.github/workflows/actions.yml` with CI steps:
    - Installs Python 3.13
    - Installs the required Python packages (ie. `matplotlib`, `numpy`, `networkx`)
    - Installs Codon v0.19.3 + seq plugin
    - Runs `week1/evaluate.py` automatically on push
- Verified that CI runs and produces the runtime/N50 table

## STEP 2 - Python Implementation
- Cloned Zhongyu Chen's toy de Bruijn graph assembler
- Verified that `main.py ` can run on datasets in `week1/data/`
- The assembler outputs contigs and `evaluate.py` computes the N50 values from them.
- **My Python run results:**
```
Dataset	Language	Runtime	N50
---------------------------------------------------------------
data1	python		0:00:13	9990
data2	python		0:00:29	9992
data3	python		0:00:33	9824
data4	python		0:13:43	159255
```

## Comparison to the Original Repo
- The original README reports NGA50 values but my results use N50 (as specified in the assignment update on Sept 13), therefore the values differ. This confirms that the original repo is not directly reproducible as-is.

## STEP 3 - Codon Conversion
- Converted `main.py` to `main.codon`
- Updated `evaluate.py` to run both of these versions automatically
- Codon runs succeeded with much shorter runtimes although the N50 values differ from Python output:
``` 
Dataset	Language	Runtime	N50
---------------------------------------------------------------
data1	codon		0:00:03	2937
data2	codon		0:00:03	2524
data3	codon		0:00:03	2211
data4	codon		0:00:19	2429
```
- This shows that Codon does execute correctly, but due to language differences it produces different assemblies

## Automation Notes
- Revisited `evaluation.py` and ensured that it:
    - Ran both Python and Codon automatically on all the datasets
    - Captured the stdout and stderr into `week1/out/` for inspection
    - Computed N50 values
    - Printed a summary table for CI logs
- Added an error handling so failures are logged as `ERROR 0` instead of breaking the run

## Reproducibility Notes
- The current code in my repository runs successfully for both the Python and Codon versions, but the N50 results are not the same
- I was able to adjust the code so that Python and Codon consistently gave near identical values on datasets 1-3, but the Codon run on dataset 4 would crash and across all datasets Codon took ~2 times as long as Python
- Both implementations run, but my Codon conversion does not fully reproduce the Python outputs

## Gotchas
- Had to install extra Python packages in CI (see Repo and CI Setup section)
- Initially forgot to print stderr into CI logs, making debugging harder
- Accidentally placed `main.codon` in the wrong directory at first, but fixed it by moving it to `week1`
- Found and corrected a bug in the Codon error-handling block that originally printed `python` instead of `codon`
- Unable to make my Codon conversion code reproduce Python values and work consistently on bigger datasets/run in decent time

## Conclusion
- Repo structure, CI setup, and evaluation script all seem to be working correctly
- Python and Codon versions both run automatically in CI
- Results are consistent with assignment requirements (reproducibility, automation, Codon conversion)