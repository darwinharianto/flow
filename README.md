[![Build Status](https://github.com/darwinharianto/flow/actions/workflows/codecov.yml/badge.svg)](https://github.com/darwinharianto/flow/actions)
[![codecov](https://codecov.io/gh/darwinharianto/flow/graph/badge.svg)](https://codecov.io/gh/darwinharianto/flow)
[![Python Version Support](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://github.com/darwinharianto/flow)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Flow Free Constraint Programming Solver

An elegant, optimal solver for Flow Free grid games that routes paths on arbitrary grid dimensions while **minimizing path turns** and maximizing board coverage using Google OR-Tools CP-SAT.

## Features
- **Turn Minimization**: Solves for path layouts with the absolute minimum number of bends.
- **Constraint Satisfaction**: Ensures complete Hamiltonian-style flow connectivity without collisions.
- **Plotting Engine**: Generates clean visual solutions utilizing custom coordinate space conversions in matplotlib.

## Installation
Clone the repository and install it in editable mode:
```bash
git clone https://github.com/darwinharianto/flow.git
cd flow
pip install -e .
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
