import matplotlib.pyplot as plt
import numpy as np
from flow_solver.solver import validate_board_and_count_colors, initiate_model_with_param, solve_model

def run_demo():
    # Define a 5x5 board with 3 colors and a wall (-1)
    # 0 represents empty space; matching positive integers represent connection pairs.
    board = [
        [1,  0,  0,  0,  2],
        [0, -1,  0,  0,  0],
        [3,  0,  0,  0,  0],
        [0,  0,  1,  2,  0],
        [3,  0,  0,  0,  0]
    ]

    print("Validating grid dimensions and colors...")
    num_colors, num_walls = validate_board_and_count_colors(board)
    print(f"Found {num_colors} colors and {num_walls} walls.")

    print("Initializing CP-SAT Solver model constraints...")
    model, solution, edge = initiate_model_with_param(
        board=board,
        num_colors=num_colors,
        num_wall=num_walls,
        fill=1.0  # Require 100% of non-wall cells to be filled
    )

    print("Solving with turn minimization (max time limit 15 seconds)...")
    ax = solve_model(model, board, solution, edge, limit=15)

    if ax:
        print("Solution found successfully! Displaying grid visual...")
        plt.title("Turn-Minimized Flow Solution")
        plt.show()
    else:
        print("No feasible solution could be found satisfying constraints.")

if __name__ == '__main__':
    run_demo()
