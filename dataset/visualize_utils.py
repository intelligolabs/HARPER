import glob
import os
import pickle as pkl
import random
import matplotlib.pyplot as plt
import numpy as np

import glob
import os
import pickle as pkl
import random
import matplotlib.pyplot as plt
import numpy as np


def show_subject(dataset_path, subject_name):
    # manual show without dataloader
    annotations = glob.glob(os.path.join(dataset_path, "**", "*_aligned.pkl"), recursive=True)
    annotations_of_subject = []
    for annotation in annotations:
        annotation_fname = os.path.basename(annotation)
        if annotation_fname.startswith(subject_name):
            annotations_of_subject.append(annotation)

    assert len(annotations_of_subject) > 0, f"No annotations found for {subject_name}"

    # annotations_of_subject.sort()
    # random.shuffle(annotations_of_subject)

    # samples = len(annotations_of_subject)
    samples = 7
    n_images = 10
    fig, axs = plt.subplots(samples, n_images, figsize=(3 * samples, n_images))
    annotations_of_subject = annotations_of_subject[:samples]

    for i, annotation_fname in enumerate(annotations_of_subject):
        annotation = load_pkl(annotation_fname)
        annotation_basename = os.path.basename(
            annotation_fname
        )  # Get the base name of the annotation file
        annotation_basename = " ".join(annotation_basename.split("_image_aligned.pkl"))
        # dict to list
        annotation = list(annotation.values())
        tot = len(annotation)
        n_images_to_show = min(n_images, tot // n_images)
        data = annotation[::n_images_to_show]

        for j, frame_ann in enumerate(data[:n_images]):
            image_path = frame_ann["spot_pov_image"]

            find_file_in_dir = glob.glob(
                os.path.join(dataset_path, "**", image_path), recursive=True
            )
            if len(find_file_in_dir) == 0:
                print(f"File not found: {image_path}")
                continue

            image_path = find_file_in_dir[0]

            image = plt.imread(image_path)

            joints_2d = frame_ann["human_joints_2d"]
            visibles = frame_ann["visibles"]

            visible_joints = np.asarray([joints_2d[j] for j, v in enumerate(visibles) if v])

            ax = axs[i, j]
            ax.imshow(image)

            if len(visible_joints) > 0:
                ax.scatter(visible_joints[:, 0], visible_joints[:, 1], c="r", s=5)

            # ax.scatter(joints_2d[0, visibles == 0], joints_2d[1, visibles == 0], c="b")
            ax.set_title(f"Frame {frame_ann['frame']}")
            ax.axis("off")
        axs[i, 0].set_title(f"{annotation_basename}", fontsize=10, color="blue")

    plt.savefig(f"viz_subject_{subject_name}.png")

    print("Done.")


def load_pkl(path):
    with open(path, "rb") as f:
        return pkl.load(f)


if __name__ == "__main__":
    dataset_path = "data/harper"
    show_subject(dataset_path, "cun")
