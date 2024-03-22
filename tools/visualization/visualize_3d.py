import matplotlib.pyplot as plt
import numpy as np
from tools.utils_io import load_pkl
from tools.links import human_links, spot_links


def visualize(pkl_file: str):
    # NOTE: the optitrack system has Y up
    data: dict = load_pkl(pkl_file)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    for frame_idx, frame_data in data.items():
        ax.cla()
        ax.set_title(f"Frame {frame_idx} / {len(data)}")
        human_joints_3d = np.asarray(frame_data["human_joints_3d"])
        spot_joints_3d = np.asarray(frame_data["spot_joints_3d"])

        ax.scatter(
            human_joints_3d[:, 0],
            human_joints_3d[:, 1],
            human_joints_3d[:, 2],
            color="red",
        )
        for link in human_links:
            ax.plot(
                human_joints_3d[link, 0],
                human_joints_3d[link, 1],
                human_joints_3d[link, 2],
                color="red",
            )

        ax.scatter(
            spot_joints_3d[:, 0],
            spot_joints_3d[:, 1],
            spot_joints_3d[:, 2],
            color="orange",
        )
        for link in spot_links:
            ax.plot(
                spot_joints_3d[link, 0],
                spot_joints_3d[link, 1],
                spot_joints_3d[link, 2],
                color="orange",
            )

        plt.pause(0.01)

    plt.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pkl_file",
        help="Pickle file to visualize",
        default="./data/harper_3d_30/train/avo_act1_30hz.pkl",
        type=str,
    )
    args = parser.parse_args()
    visualize(args.pkl_file)
