import pytest
import numpy as np
from flow.solver import validate_board_and_count_colors, initiate_model_with_param, solve_model

def test_validation_success():
    # A valid 2x12 board layout
    board = [
        [-1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    num_colors, num_walls = validate_board_and_count_colors(board)
    assert num_colors == 1
    assert num_walls == 1

def test_validation_invalid_shapes():
    # Row length mismatch
    board = [
        [1, 0, 1],
        [0, 0]
    ]
    with pytest.raises(AssertionError):
        validate_board_and_count_colors(board)

def test_validation_unmatched_endpoints():
    # Only 1 endpoint of color 1
    board = [
        [1, 0],
        [0, 0]
    ]
    with pytest.raises(AssertionError):
        validate_board_and_count_colors(board)

def test_solver_optimal_solution():
    # Small, simple 2x3 grid with endpoints of color 1
    board = [
        [1, 0, 0],
        [0, 0, 1]
    ]
    num_colors, num_walls = validate_board_and_count_colors(board)
    model, solution, edge = initiate_model_with_param(
        board=board,
        num_colors=num_colors,
        num_wall=num_walls,
        fill=0.5
    )
    ax = solve_model(model, board, solution, edge, limit=5)
    assert ax is not None
