import time
import logging
import numpy as np

class Utils:
    @staticmethod
    def print_time(before):
        logging.info(time.time() - before)
        return time.time()

    @staticmethod
    def linewidth_from_data_units(linewidth, axis, reference="y"):
        fig = axis.get_figure()
        if reference == "x":
            length = fig.bbox_inches.width * axis.get_position().width
            value_range = np.diff(axis.get_xlim())[0]
        elif reference == "y":
            length = fig.bbox_inches.height * axis.get_position().height
            value_range = np.diff(axis.get_ylim())[0]
        # Convert length to points
        length *= 72
        # Scale linewidth to value range
        return linewidth * (length / value_range)

    @staticmethod
    def add_walls_and_source_to_ax(ax, colors, S, scatter_size):
        s_mat = np.array(S)
        M, N = s_mat.shape[0], s_mat.shape[1]

        scatter_dict = {"color_item_-1_x_y": []}
        for iter in range(np.sum(np.unique(s_mat) > 0)):
            scatter_dict[f"color_item_{iter+1}_x_y"] = []

        for i in range(M):
            for j in range(N):
                if S[i][j] != 0:
                    scatter_dict[f"color_item_{S[i][j]}_x_y"].append([j, i])
                    
        for key in scatter_dict:
            color_item = int(key.split("_")[2])
            mat = np.array(scatter_dict[key]).T
            if len(mat) == 0:
                continue
            j = mat[0].tolist()
            i = mat[1].tolist()
            ax.scatter(
                j,
                i,
                s=scatter_size * 2,
                color=colors[color_item] if color_item != 0 else "black",
                marker="x" if color_item < 0 else None,
            )
