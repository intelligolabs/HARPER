from glob import glob
from itertools import chain
import os
import pickle as pkl

import numpy as np

PATH = "data/harper/FINAL"

train_file = "data/hrnet_3d_poses_harper_train.pkl"
test_file = "data/hrnet_3d_poses_harper_test.pkl"

assert os.path.exists(train_file), f"File not found: {train_file}"
assert os.path.exists(test_file), f"File not found: {test_file}"

gt_annotations = glob(os.path.join(PATH, "**", "*.pkl"), recursive=True)
gt_annotations_names = [
    os.path.splitext(os.path.basename(a))[0].split("_aligned")[0] for a in gt_annotations
]
assert len(gt_annotations) > 0, "No annotations found"

def get_annotation(path):
    with open(path, "rb") as f:
        return pkl.load(f)


def save_annotation(path, data):
    with open(path, "wb") as f:
        pkl.dump(data, f)

train_data = get_annotation(train_file)
test_data = get_annotation(test_file)

for a, data in chain(train_data.items(), test_data.items()):
    assert a in gt_annotations_names, f"Annotation {a} not found in ground truth annotations"

    idx = gt_annotations_names.index(a)
    gt_annotation = get_annotation(gt_annotations[idx])

    assert len(data) == len(gt_annotation), f"Data length mismatch for {a}"

    for i in gt_annotation.keys():
        vis_3d = np.asarray(data[i]["visibles_3d"]).tolist()
        depth_fov = np.asarray(data[i]["depth_fov"]).tolist()
        ann = gt_annotation[i]

        if "/" in ann["spot_pov_image"]:
            split = "train" if "/train/" in ann["spot_pov_image"] else "test"
        else:
            split = ann["metadata"]["split"]

        ann["spot_pov_image"] = os.path.basename(ann["spot_pov_image"])
        ann["spot_pov_depth"] = os.path.basename(ann["spot_pov_depth"])
        ann["spot_pov_depth_orig"] = os.path.basename(ann["spot_pov_depth_orig"])
        intrinsics = ann["intrinsics"]

        if "intrinsics" in ann:
            del ann["intrinsics"]
        if "extrinsics" in ann:
            del ann["extrinsics"]
        if "metadata" not in ann:
            ann["metadata"] = {}
        else:
            if "fixed_by" in ann["metadata"]:
                del ann["metadata"]["fixed_by"]

        ann["metadata"]["intrinsics"] = intrinsics
        ann["metadata"]["split"] = split

        if "visibles" in ann:
            vis = ann["visibles"]
            del ann["visibles"]
        else:
            vis = ann["visibles_2d"]
        ann["visibles_2d"] = vis
        ann["visibles_3d"] = vis_3d
        ann["depth_fov"] = depth_fov

        gt_annotation[i] = ann

    save_annotation(gt_annotations[idx], gt_annotation)

print("Fixed everything")


# CHECK

rand = 140
a = gt_annotations[rand]
data = get_annotation(a)
print(data[10])

print("End")