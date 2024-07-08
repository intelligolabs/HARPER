from glob import glob
import os
import pickle
import tarfile
from tqdm import tqdm
import argparse
from tools.download_utils import download_onedrive_file

parser = argparse.ArgumentParser()
parser.add_argument(
    "--dst_folder",
    help="Folder to save the dataset to",
    default="./data/",
    type=str,
)
args = parser.parse_args()

HARPER_DATA = "https://univr-my.sharepoint.com/:u:/g/personal/federico_cunico_univr_it/EX_kQzwAHPdJstpRS98M3EkB-grnV5pkS89PTZ16--Ro_w?e=IVCr3g"
dst = args.dst_folder

os.makedirs(dst, exist_ok=True)
fname = os.path.join(dst, "harper_data.tar.gz")
if os.path.isfile(fname):
    print(f"{fname} already exists. Deleting it to download again...")
    os.remove(fname)
download_onedrive_file(HARPER_DATA, fname)

with tarfile.open(fname, "r:gz") as tar:
    tar.extractall(dst)
os.remove(fname)


def open_pkl(pkl_file: str) -> dict:
    with open(pkl_file, "rb") as f:
        return pickle.load(f)


def save_pkl(pkl_file: str, data) -> None:
    with open(pkl_file, "wb") as f:
        pickle.dump(data, f)


def fix(annotations, type):
    tags = [
        ("spot_pov_image", "images"),
        ("spot_pov_depth", "depths"),
        ("spot_pov_depth_orig", "raw_depths"),
    ]
    assert len(annotations) > 0, "No annotations found"
    for ann in tqdm(annotations, "Fixing annotations for " + type):
        data = open_pkl(ann)
        for frame_idx, curr in data.items():
            # edit path according to dst
            for t, ppath in tags:
                orig = curr[t]
                orig = os.path.split(orig)[-1]
                new_fname = os.path.realpath(os.path.join(dst, type, ppath, orig))
                assert os.path.isfile(new_fname), f"File {new_fname} not found"
                curr[t] = new_fname

        save_pkl(ann, data)


annotations_train = glob(
    os.path.join(dst, "train", "**", "*_aligned.pkl"), recursive=True
)
annotations_test = glob(
    os.path.join(dst, "test", "**", "*_aligned.pkl"), recursive=True
)

fix(annotations_train, "train")
fix(annotations_test, "test")
