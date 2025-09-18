import sys, time, shutil, subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
DATA_DIR = ROOT / "week1" / "data"
OUT_DIR  = ROOT / "week1" / "out"
PY_MAIN  = ROOT / "week1" / "code" / "main.py"
CODON_MAIN = ROOT / "week1" / "main.codon"

def format_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(round(seconds % 60))
    if s == 60:
        s = 0; m += 1
    if m == 60:
        m = 0; h += 1
    return f"{h}:{m:02d}:{s:02d}"

def run_and_capture(cmd: list[str], stdout_path: Path) -> tuple[str, str, float]:
    '''runs the commands, measures elapsed time, captures stdout/stderr as text'''
    t0 = time.perf_counter()
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    elapsed = time.perf_counter() - t0

    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    stdout_path.write_text(p.stdout)

    stderr_path = stdout_path.with_suffix(stdout_path.suffix + ".stderr.txt")
    if p.stderr:
        stderr_path.write_text(p.stderr)

    if p.returncode != 0: # print stderr to the CI logs (for debugging)
        print(f"Command failed: {' '.join(cmd)}")
        print("----- stderr (first 50 lines) -----")
        print("\n".join(p.stderr.splitlines()[:50]))
        print("----- end stderr -----")
        raise RuntimeError(f"command failed: {' '.join(cmd)}")
    
    return p.stdout, p.stderr, elapsed


def extract_lengths(text: str) -> list[int]:
    '''parses the contig lengths from the assembler stdout'''
    lens: list[int] = []
    for line in text.splitlines():
        parts = line.strip().split()
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            lens.append(int(parts[1]))
    return lens

def n50(lengths: list[int]) -> int:
    '''computes the N50'''
    if not lengths:
        return 0
    lengths = sorted(lengths, reverse=True)
    total = sum(lengths)
    running_total = 0
    for cur in lengths:
        running_total += cur
        if running_total >= total / 2:
            return cur
    return 0

def main(argv: list[str]) -> int:
    datasets = argv[1:] if len(argv) > 1 else ["data1", "data2", "data3", "data4"]

    print("Dataset\tLanguage\tRuntime\tN50")
    print("---------------------------------------------------------------")

    py_exe = sys.executable or "python3"

    for ds in datasets:
        ds_path = DATA_DIR / ds # get path for each data set

        # python run
        py_out = OUT_DIR / f"{ds}.python.stdout.txt" # where to write python stdout
        py_cmd = [py_exe, str(PY_MAIN), str(ds_path)] # the python command to run 
        try: # gets values and prints in table row
            py_stdout, py_stderr, py_elapsed = run_and_capture(py_cmd, py_out)
            py_lengths = extract_lengths(py_stdout)
            py_n50 = n50(py_lengths)
            print(f"{ds}\tpython\t\t{format_time(py_elapsed)}\t{py_n50}")
        except Exception as e: # prints error in table, points to stderr file, skips codon run for dataset
            print(f"{ds}\tpython\t\tERROR\t0")
            print(f"(python error: {e})")
            err_path = py_out.with_suffix(py_out.suffix + ".stderr.txt")
            if err_path.exists():
                print(f"(python stderr saved to {err_path})")
            continue


        # codon run
        if CODON_MAIN.exists() and shutil.which("codon"):
            cd_out = OUT_DIR / f"{ds}.codon.stdout.txt" # where to write codon stdout
            cd_cmd = ["codon", "run", "-release", str(CODON_MAIN), str(ds_path)] #the codon command to run
            try: # gets values and prints in table row
                cd_stdout, cd_stderr, cd_elapsed = run_and_capture(cd_cmd, cd_out)
                cd_lengths = extract_lengths(cd_stdout)
                cd_n50 = n50(cd_lengths)
                print(f"{ds}\tcodon\t\t{format_time(cd_elapsed)}\t{cd_n50}")
            except Exception as e: #prints error in table, points to stderr file, skips to next datatset
                print(f"{ds}\codon\t\tERROR\t0")
                print(f"(codon error: {e})")
                err_path = cd_out.with_suffix(cd_out.suffix + ".stderr.txt")
                if err_path.exists():
                    print(f"(codon stderr saved to {err_path})")
                continue


    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))