from glob import glob
import os
import shutil
from tools.download_utils import download_onedrive_file

HARPER_3D_120hz = "https://univr-my.sharepoint.com/:u:/g/personal/federico_cunico_univr_it/EeofmATON85Ilw4b64HkrwoBT97vwrIsUTwA9O7O3CHSqg?e=1JwMAH"
HARPER_3D_30hz = "https://univr-my.sharepoint.com/:u:/g/personal/federico_cunico_univr_it/EWO4iz-gGldDqFvGJq9lMYgBLxkv3Ud8D2JQO8pp2cToDA?e=eEFBN8"
TEST_SUBJECTS = ["t", "toa", "xu", "xy", "yf"]


def _download_and_extract(url: str, name: str, dst_folder: str) -> None:
    dst_folder = os.path.join(dst_folder, name)
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    fname_zip = os.path.join(dst_folder, f"{name}.zip")

    download_onedrive_file(url, fname_zip)
    shutil.unpack_archive(fname_zip, dst_folder)
    os.remove(fname_zip)

    train = os.path.join(dst_folder, "train")
    test = os.path.join(dst_folder, "test")
    if not os.path.exists(train):
        os.makedirs(train)
    if not os.path.exists(test):
        os.makedirs(test)
    for pkl_file in glob(os.path.join(dst_folder, "*.pkl")):
        pkl_filename: str = os.path.basename(pkl_file)
        if _is_test_subj(pkl_filename):
            shutil.move(pkl_file, os.path.join(test, pkl_filename))
        else:
            shutil.move(pkl_file, os.path.join(train, pkl_filename))


def _is_test_subj(fname: str) -> bool:
    for subject in TEST_SUBJECTS:
        template = f"{subject}_"
        if template in fname:
            return True
    return False


def download_harper_3d(dst_folder: str) -> None:
    """
    Main for downloading the Harper 3D dataset from OneDrive.
    """
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
    _download_and_extract(HARPER_3D_120hz, "harper_3d_120", dst_folder)
    _download_and_extract(HARPER_3D_30hz, "harper_3d_30", dst_folder)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dst_folder",
        help="Folder to save the dataset to",
        default="./data/",
        type=str,
    )
    args = parser.parse_args()
    download_harper_3d(args.dst_folder)
