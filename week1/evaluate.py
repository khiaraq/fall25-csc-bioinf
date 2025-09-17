import sys, time, shutil, subprocess, os
from pathlib import Path

# ----- Path setup that works from any cwd -----
SCRIPT_DIR = Path(__file__).resolve().parent       # .../fall25-csc-bioinf/week1
ROOT = SCRIPT_DIR.parent                           # .../fall25-csc-bioinf
DATA_DIR = ROOT / "week1" / "data"
OUT_DIR  = ROOT / "week1" / "out"
PY_MAIN  = ROOT / "week1" / "code" / "main.py"
CODON_MAIN = ROOT / "week1" / "main.codon"

# ----- Pretty H:MM:SS -----
def fmt_hms(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(round(seconds % 60))
    if s == 60:
        s = 0; m += 1
    if m == 60:
        m = 0; h += 1
    return f"{h}:{m:02d}:{s:02d}"

# ----- Run a command, capture stdout/stderr, save to files -----
def run_and_capture(cmd: list[str], stdout_path: Path) -> tuple[str, str, float]:
    t0 = time.perf_counter()
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    elapsed = time.perf_counter() - t0

    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    stdout_path.write_text(p.stdout)

    stderr_path = stdout_path.with_suffix(stdout_path.suffix + ".stderr.txt")
    if p.stderr:
        stderr_path.write_text(p.stderr)

    if p.returncode != 0:
        raise RuntimeError(f"command failed: {' '.join(cmd)}\n{p.stderr[:500]}")
    return p.stdout, p.stderr, elapsed

# ----- Parse "index length" lines -----
def extract_lengths(text: str) -> list[int]:
    lens: list[int] = []
    for line in text.splitlines():
        parts = line.strip().split()
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            lens.append(int(parts[1]))
    return lens

# ----- N50 -----
def n50(lengths: list[int]) -> int:
    if not lengths:
        return 0
    lengths = sorted(lengths, reverse=True)
    total = sum(lengths)
    acc = 0
    for L in lengths:
        acc += L
        if acc >= total / 2:
            return L
    return 0

def main(argv: list[str]) -> int:
    datasets = argv[1:] if len(argv) > 1 else ["data1", "data2", "data3", "data4"]
    print("Dataset\tLanguage\tRuntime\tN50")
    print("---------------------------------------------------------------")

    py_exe = sys.executable or "python3"

    for ds in datasets:
        ds_path = DATA_DIR / ds

        # -------- Python run --------
        py_out = OUT_DIR / f"{ds}.python.stdout.txt"
        py_cmd = [py_exe, str(PY_MAIN), str(ds_path)]
        try:
            py_stdout, py_stderr, py_elapsed = run_and_capture(py_cmd, py_out)
            py_lengths = extract_lengths(py_stdout)
            py_n50 = n50(py_lengths)
            print(f"{ds}\tpython\t\t{fmt_hms(py_elapsed)}\t{py_n50}")
        except Exception as e:
            print(f"{ds}\tpython\t\tERROR\t0")
            err_path = py_out.with_suffix(py_out.suffix + ".stderr.txt")
            if err_path.exists():
                print(f"(python stderr → {err_path})")
            continue  # important: don't touch py_stdout if the run failed

        # -------- Codon run (optional) --------
        if CODON_MAIN.exists() and shutil.which("codon"):
            cd_out = OUT_DIR / f"{ds}.codon.stdout.txt"
            cd_cmd = ["codon", "run", "-release", str(CODON_MAIN), str(ds_path)]
            try:
                cd_stdout, cd_stderr, cd_elapsed = run_and_capture(cd_cmd, cd_out)
                cd_lengths = extract_lengths(cd_stdout)
                cd_n50 = n50(cd_lengths)
                print(f"{ds}\tcodon\t\t{fmt_hms(cd_elapsed)}\t{cd_n50}")
            except Exception as e:
                print(f"{ds}\tcodon\t\tERROR\t0")
                err_path = cd_out.with_suffix(cd_out.suffix + ".stderr.txt")
                if err_path.exists():
                    print(f"(codon stderr → {err_path})")
                continue

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))