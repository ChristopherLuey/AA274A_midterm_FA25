#!/usr/bin/env python3
"""
Utility script to extract the Problem 1a dynamics implementation from the
`CS237A_F25_Midterm_P1.ipynb` notebook and write it to a standalone Python
file that can be included verbatim in the LaTeX appendix.
"""

from __future__ import annotations

import nbformat
from pathlib import Path

NOTEBOOK_PATH = Path("CS237A_F25_Midterm_P1.ipynb")
OUTPUT_PATH = Path("output/problem1a_dynamics.py")


def extract_dynamics_cell() -> str:
    """Return the source code of the notebook cell containing f_continuous."""
    notebook = nbformat.read(NOTEBOOK_PATH, as_version=4)
    for cell in notebook.cells:
        if cell.cell_type == "code" and "def f_continuous" in cell.source:
            return cell.source.strip() + "\n"
    raise RuntimeError("Could not locate the f_continuous cell in the notebook.")


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    snippet = extract_dynamics_cell()
    OUTPUT_PATH.write_text(snippet, encoding="utf-8")
    print(f"Wrote Problem 1a dynamics snippet to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
