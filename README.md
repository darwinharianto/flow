[![Build Status](https://github.com/darwinharianto/flow/actions/workflows/codecov.yml/badge.svg)](https://github.com/darwinharianto/flow/actions)
[![codecov](https://codecov.io/gh/darwinharianto/flow/graph/badge.svg)](https://codecov.io/gh/darwinharianto/flow)
[![Python Version Support](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://github.com/darwinharianto/flow)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Flow Free Constraint Programming Solver

An elegant, optimal solver for Flow Free grid games that routes paths on arbitrary grid dimensions while **minimizing path turns** and maximizing board coverage using Google OR-Tools CP-SAT.

## Features
- **Turn Minimization**: Solves for path layouts with the absolute minimum number of bends.
- **Constraint Satisfaction**: Ensures complete Hamiltonian-style flow connectivity without collisions.
- **Plotting Engine**: Generates clean visual solutions utilizing custom coordinate space conversions in matplotlib.

## Installation

This repository uses [uv](https://github.com/astral-sh/uv) for fast and reproducible package and environment management.

### Using `uv` (Recommended)
Clone the repository and install all dependencies (including development dependencies):
```bash
git clone https://github.com/darwinharianto/flow.git
cd flow
uv sync
```

Alternatively, install editable into an active environment:
```bash
uv pip install -e .
```

### Using standard `pip`
```bash
pip install -e ".[test]"
```

## Quick Start
```python
from flow.solver import validate_board_and_count_colors, initiate_model_with_param, solve_model
import matplotlib.pyplot as plt

# -1 represents walls, positive integers represent matched endpoint pairs
board = [
    [-1, 1, 0, 0, 0, 0],
    [ 1, 0, 0, 0, 0, 0]
]

num_colors, num_wall = validate_board_and_count_colors(board)
model, solution, edge = initiate_model_with_param(board, num_colors, num_wall, fill=0.1)
ax = solve_model(model, board, solution, edge, limit=10)
plt.show()
```

## Testing & Multi-Python Support

Supported Python versions: **3.10**, **3.11**, **3.12**, and **3.13**.

### Run tests with default environment
```bash
uv run pytest
```

### Run tests across specific Python versions
`uv` automatically downloads and provisions any required Python version on demand:
```bash
uv run --python 3.10 pytest
uv run --python 3.11 pytest
uv run --python 3.12 pytest
uv run --python 3.13 pytest
```

### Run automated matrix test locally
A script is included to test against all supported Python versions in sequence:
```bash
./test_all.sh
```

### Run with Coverage
```bash
uv run pytest --cov=flow --cov-report=term-missing tests/
```
