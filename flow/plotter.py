import numpy as np
import matplotlib.pyplot as plt
from .utils import Utils

utils = Utils()

def fill_board_from_dict(S, data):
    ax = plt.gca()
    colors = plt.cm.tab20.colors

    s_mat = np.array(S)
    M, N = s_mat.shape[0], s_mat.shape[1]

    s_tuple = ax.figure.get_size_inches() * ax.figure.dpi
    s = (s_tuple[0] * s_tuple[1]) / (M * N)

    for key in data:
        color_item = int(key.split(" ")[1])
        i = int(key.split(" ")[2])
        j = int(key.split(" ")[3])
        if data[key]:
            ax.scatter(
                j,
                i,
                s=s / 4,
                color=colors[color_item] if color_item != 0 else "black",
                marker="x",
            )

def plot_directed_solution_with_dir(board, S, direction, colors=plt.cm.tab20.colors):
    plt.cla()
    plt.clf()
    ax = plt.gca()
    M, N = np.array(S).shape[0], np.array(S).shape[1]

    ax.set_ylim(M - 0.5, -0.5)
    ax.set_xlim(-0.5, N - 0.5)
    ax.set_aspect("equal")
    ax.set_facecolor("black")
    ax.set_yticks([i + 0.5 for i in range(M - 1)], minor=True)
    ax.set_xticks([j + 0.5 for j in range(N - 1)], minor=True)
    ax.grid(visible=True, which="minor", color="white")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.tick_params(axis="both", which="both", length=0)

    linewidth = utils.linewidth_from_data_units(0.45, ax)
    for item in direction:
        prev_x, prev_y = int(item[1]), int(item[2])
        cur_x, cur_y = int(item[3]), int(item[4])
        ax.plot(
            [prev_x, cur_x], [prev_y, cur_y], color=colors[int(item[0])], lw=linewidth, zorder=3
        )
    utils.add_walls_and_source_to_ax(ax, colors, board, linewidth**2)

    return ax.figure
