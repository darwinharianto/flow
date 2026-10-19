import sys
import time
import math
import logging
import collections
import numpy as np
import matplotlib.pyplot as plt
from ortools.sat.python import cp_model
from .plotter import plot_directed_solution_with_dir

def validate_board_and_count_colors(board):
    assert isinstance(board, list)
    assert all(isinstance(row, list) for row in board)
    assert len(set(map(len, board))) == 1
    colors = collections.Counter(square for row in board for square in row)
    del colors[0]
    neg_counter = 0
    for color in list(colors.keys()):
        if color < 0:
            neg_counter += 1
            del colors[color]
    assert all(count == 2 for count in colors.values())
    num_colors = len(colors)
    assert set(colors.keys()) == set(range(1, num_colors + 1))

    num_walls = len([x for sublist in board for x in sublist if x < 0])
    return num_colors, num_walls

def initiate_model_with_param(
    board,
    num_colors,
    num_wall=0,
    fill=1.0,
    area_matrix=None,
    min_length=0,
    max_length=sys.maxsize,
):
    model = cp_model.CpModel()

    solution = [
        [square or model.NewIntVar(0, num_colors, "") for (j, square) in enumerate(row)]
        for (i, row) in enumerate(board)
    ]
    edge = {}
    all_turn = {}
    true = model.NewBoolVar("")
    model.AddBoolOr([true])

    board_size = len(board) * len(board[0])
    cus_board_size = board_size * num_colors
    at_least_filled = math.floor((board_size - num_wall) * fill)

    not_filled = 0
    turns = 0
    path_length = np.zeros(num_colors).tolist()

    test = model.NewIntVar(-1000, 10000, "")

    for color in range(1, num_colors + 1):
        endpoints = []
        arcs = []
        for i, row in enumerate(board):
            for j, square in enumerate(row):
                if square == color:
                    endpoints.append((i, j))
                else:
                    arcs.append(((i, j), (i, j)))
                if i < len(board) - 1:
                    if area_matrix is None:
                        if board[i + 1][j] != -1:
                            arcs.append(((i, j), (i + 1, j)))
                    else:
                        if area_matrix[i + 1][j] == color or area_matrix[i + 1][j] == 0:
                            arcs.append(((i, j), (i + 1, j)))
                if j < len(row) - 1:
                    if area_matrix is None:
                        if board[i][j + 1] != -1:
                            arcs.append(((i, j), (i, j + 1)))
                    else:
                        if area_matrix[i][j + 1] == color or area_matrix[i][j + 1] == 0:
                            arcs.append(((i, j), (i, j + 1)))

        (i1, j1), (i2, j2) = endpoints
        k1 = i1 * len(row) + j1
        k2 = i2 * len(row) + j2
        arc_variables = [(k2, k1, true)]

        path_length[color - 1] = 0

        for (i1, j1), (i2, j2) in arcs:
            k1 = i1 * len(row) + j1
            k2 = i2 * len(row) + j2
            edge_name = f"color_i1_j1_i2_j2 {color} {i1} {j1} {i2} {j2}"
            edge[edge_name] = model.NewIntVar(0, 1, edge_name)
            if k1 == k2:
                model.Add(solution[i1][j1] != color).OnlyEnforceIf(edge[edge_name])
                arc_variables.append((k1, k1, edge[edge_name]))
                not_filled += edge[edge_name]
            else:
                model.Add(solution[i1][j1] == color).OnlyEnforceIf(edge[edge_name])
                model.Add(solution[i2][j2] == color).OnlyEnforceIf(edge[edge_name])
                forward = model.NewIntVar(0, 1, "")
                backward = model.NewIntVar(0, 1, "")

                model.AddBoolOr([edge[edge_name], forward.Not()])
                model.AddBoolOr([edge[edge_name], backward.Not()])
                model.AddBoolOr([edge[edge_name].Not(), forward, backward])
                model.AddBoolOr([forward.Not(), backward.Not()])

                arc_variables.append((k1, k2, forward))
                arc_variables.append((k2, k1, backward))
                path_length[color - 1] += forward + backward

        for i, row in enumerate(board):
            for j, square in enumerate(row):
                bottom = f"color_i1_j1_i2_j2 {color} {i} {j} {i+1} {j}"
                top = f"color_i1_j1_i2_j2 {color} {i-1} {j} {i} {j}"
                right = f"color_i1_j1_i2_j2 {color} {i} {j} {i} {j+1}"
                left = f"color_i1_j1_i2_j2 {color} {i} {j-1} {i} {j}"

                turn_bool = model.NewIntVar(0, 1, "color_i1_j1_i2_j2")
                all_turn[f"color_i1_j1_i2_j2 {color} {i} {j} {i} {j}"] = turn_bool

                left_value = edge[left] if left in edge else true.Not()
                right_value = edge[right] if right in edge else true.Not()
                top_value = edge[top] if top in edge else true.Not()
                bottom_value = edge[bottom] if bottom in edge else true.Not()

                model.AddBoolOr([left_value, right_value.Not(), bottom_value, top_value.Not(), turn_bool])
                model.AddBoolOr([left_value, right_value.Not(), bottom_value.Not(), top_value, turn_bool])
                model.AddBoolOr([left_value.Not(), right_value, bottom_value, top_value.Not(), turn_bool])
                model.AddBoolOr([left_value.Not(), right_value, bottom_value.Not(), top_value, turn_bool])
                model.AddBoolOr([left_value, right_value, turn_bool.Not()])
                model.AddBoolOr([bottom_value, top_value, turn_bool.Not()])
                model.AddBoolOr([bottom_value.Not(), top_value.Not(), turn_bool.Not()])
                model.AddBoolOr([left_value.Not(), right_value.Not(), turn_bool.Not()])

                turns += turn_bool

        model.Add(path_length[color - 1] < max_length)
        model.Add(path_length[color - 1] >= min_length)
        model.AddCircuit(arc_variables)

    model.Minimize(turns + not_filled)
    model.Add((cus_board_size - not_filled) >= at_least_filled)
    model.Add(test == (cus_board_size - not_filled))

    return model, solution, edge

def solve_model(
    model, board, solution, edge, limit=None, image=None, colors=plt.cm.tab20.colors
) -> plt.Axes:
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = limit

    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        solved = []
        direction = []
        for v in solution:
            solved.append([solver.Value(x) for x in v])
        for v in edge:
            color_x_y_x_y = v.split(" ")[1:]
            color, y_prev, x_prev, y_cur, x_cur = color_x_y_x_y
            if (x_prev != x_cur or y_prev != y_cur) and solver.Value(edge[v]):
                direction.append([color, x_prev, y_prev, x_cur, y_cur])

        _ = plot_directed_solution_with_dir(board, np.array(solved), direction, colors)
        ax = plt.gca()
        if image:
            img = plt.imread(image)
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()
            ax.imshow(img, extent=[xlim[0], xlim[1], ylim[0], ylim[1]])
        return ax
    else:
        return None
