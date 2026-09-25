# Sudoku Solver: CSP Backtracking vs. Simulated Annealing

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![AI](https://img.shields.io/badge/AI-search%20%26%20optimisation-555)

This project compares two AI approaches to Sudoku on generated puzzles at three difficulty levels:

| | **CSP backtracking** (`CSP.py`) | **Simulated annealing** (`SA.py`) |
|---|---|---|
| Formulation | 81 variables with domains 1–9 and row/column/box constraints | Optimisation: minimise duplicate values across rows and columns |
| Search | Depth-first backtracking with **forward checking** | Swap two non-fixed cells inside a box, and accept worse moves with probability e<sup>−Δ/T</sup> |
| Heuristics | **MRV** / **MCV** variable ordering, **LCV** value ordering | Each box starts as a permutation of 1–9, so box constraints always hold; geometric cooling (0.99995) |
| Guarantee | Complete: always finds a solution if one exists | Anytime: returns the best grid found, which may be near-valid |

`Main.py` generates puzzles (easy, medium or hard) by filling a valid grid and removing cells. It runs either solver and records statistics for comparison. Both solvers also handle 16×16 boards.

## Run

```bash
python Main.py
```

```
1. Generate new board
2. Show current board
3. Run CSP algorithm
4. Run SA algorithm
5. Show statistics
```

---

*Team project (2 students), Artificial Intelligence (ENCS3340), Birzeit University, Fall 2025/26. Forked from [MohammadHamo912/SudokoSolverUniversityProject_AICourse](https://github.com/MohammadHamo912/SudokoSolverUniversityProject_AICourse).*
