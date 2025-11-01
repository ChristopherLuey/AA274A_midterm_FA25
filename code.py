#!/usr/bin/env python3
"""
Utility script to extract implemented notebook cells and mirror them into
standalone Python files that can be included verbatim in the LaTeX appendix.
"""

from __future__ import annotations

import json
from pathlib import Path

NOTEBOOK_MAP = {
    "CS237A_F25_Midterm_P1.ipynb": {
        "output/problem1a_dynamics.py": "def f_continuous",
        "output/problem1b_running_cost.py": "def running_cost",
        "output/problem1c_continuous_jacobians.py": "def continuous_jacobians",
        "output/problem1c_discrete_jacobians.py": "def discrete_jacobians",
        "output/problem1c_linearize.py": "def linearize_about",
    },
    "CS237A_F25_Midterm_P3.ipynb": {
        "output/problem3a_ransac_line.py": "def ransac_line",
        "output/problem3b_umeyama.py": "def umeyama_alignment",
        "output/problem3c_ransac_umeyama.py": "def ransac_umeyama",
    },
}

SCRIPT_MAP = {
    "P4_rrt.py": {
        "output/problem4a_is_free_state.py": 'Returns True if the robot in pose "x" is not in collision',
    },
    "rrt_experiments.py": {
        "output/problem4d_rrt_experiments.py": "def run_case",
    },
}


def load_notebook(path: Path) -> dict:
    """Load the notebook JSON into a Python dictionary."""
    return json.loads(path.read_text(encoding="utf-8"))


def extract_cell_source(notebook: dict, match: str) -> str:
    """Return the source of the first code cell that contains the match string."""
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") == "code":
            source = "".join(cell.get("source", []))
            if match in source:
                return source.strip() + "\n"
    raise RuntimeError(f"Could not locate a cell containing {match!r}.")


def extract_script_source(script_path: Path, match: str) -> str:
    """Return the source of the first function in a Python script containing the match string."""
    lines = script_path.read_text(encoding="utf-8").splitlines()
    for idx, line in enumerate(lines):
        if match in line:
            start_idx = idx
            while start_idx >= 0 and not lines[start_idx].lstrip().startswith("def "):
                start_idx -= 1
            if start_idx < 0:
                start_idx = idx
            indent = len(lines[start_idx]) - len(lines[start_idx].lstrip())
            snippet_lines = [lines[start_idx].rstrip()]
            for tail in lines[start_idx + 1 :]:
                if not tail.strip():
                    snippet_lines.append(tail.rstrip())
                    continue
                current_indent = len(tail) - len(tail.lstrip())
                if current_indent <= indent and not tail.lstrip().startswith("#"):
                    break
                snippet_lines.append(tail.rstrip())
            return "\n".join(snippet_lines) + "\n"
    raise RuntimeError(f"Could not locate source containing {match!r} in {script_path}.")


def main() -> None:
    for notebook_name, mapping in NOTEBOOK_MAP.items():
        notebook_path = Path(notebook_name)
        notebook = load_notebook(notebook_path)
        for relative_path, match in mapping.items():
            output_path = Path(relative_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            snippet = extract_cell_source(notebook, match)
            output_path.write_text(snippet, encoding="utf-8")
            print(f"Wrote notebook cell containing {match!r} to {output_path}")
    for script_name, mapping in SCRIPT_MAP.items():
        script_path = Path(script_name)
        for relative_path, match in mapping.items():
            output_path = Path(relative_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            snippet = extract_script_source(script_path, match)
            output_path.write_text(snippet, encoding="utf-8")
            print(f"Wrote script snippet containing {match!r} to {output_path}")


if __name__ == "__main__":
    main()
