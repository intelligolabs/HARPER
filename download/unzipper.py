import os
import pickle
import shutil
from typing import List, Optional
import zipfile
from glob import glob

from tqdm import tqdm

# list of the test subjects
test_subjs = ["t", "toa", "xu", "xy", "yf"]


def _try_extract(input_zip: zipfile.ZipFile, src: str, dst: str):
    try:
        input_zip.extract(src, dst)
    except KeyError as e:
        print(f"Error extracting {src} from {input_zip}: {e}")
    except:
        print(f"Error extracting {src} from {input_zip}")


def extract_zip(
    input_zip_fname: str,
    annotation_folder: str,
    img_folder: str,
    depth_folder: str,
    raw_depth_folder: str = None,
    tool_folder: str = None,
):
    input_zip = zipfile.ZipFile(input_zip_fname)
    files = input_zip.filelist

    all_pkls = [f for f in files if f.filename.endswith(".pkl")]
    algned_annot = [a for a in all_pkls if "aligned" in a.filename][0]
    manual_annot = [a for a in all_pkls if "annotation" in a.filename][0]

    images = [f for f in files if f.filename.endswith(".png")]
    depths = [f for f in files if f.filename.endswith(".npy")]
    orig_depths = [f for f in files if f.filename.endswith("_orig.npy")]
    depths = [d for d in depths if not d.filename.endswith("_orig.npy")]

    # input_zip.extract(annotation, annotation_folder)
    _try_extract(input_zip, algned_annot, annotation_folder)
    for img in images:
        # input_zip.extract(img, img_folder)
        _try_extract(input_zip, img, img_folder)
    for depth in depths:
        # input_zip.extract(depth, depth_folder)
        _try_extract(input_zip, depth, depth_folder)
    annotation_fname = os.path.join(annotation_folder, algned_annot.filename)
    images_fnames = [os.path.join(img_folder, i.filename) for i in images]
    depths_fnames = [os.path.join(depth_folder, d.filename) for d in depths]

    ## convert them to absolute paths
    images_fnames = [os.path.abspath(i) for i in images_fnames]
    depths_fnames = [os.path.abspath(d) for d in depths_fnames]

    images_fnames.sort()
    depths_fnames.sort()

    if raw_depth_folder is not None:
        for orig_depth in orig_depths:
            # input_zip.extract(orig_depth, raw_depth_folder)
            _try_extract(input_zip, orig_depth, raw_depth_folder)
        orig_depths_fnames = [
            os.path.join(raw_depth_folder, d.filename) for d in orig_depths
        ]
        orig_depths_fnames = [os.path.abspath(d) for d in orig_depths_fnames]
        orig_depths_fnames.sort()
    else:
        orig_depths_fnames = []

    if tool_folder is not None:
        _try_extract(input_zip, manual_annot, tool_folder)

    # update the annotation file to point to the correct image and depth files
    with open(annotation_fname, "rb") as f:
        data = pickle.load(f)
    for frame_idx, curr_ann in data.items():
        if frame_idx > len(images_fnames):
            print(
                f"[E] Error: frame_idx {frame_idx} > len(images_fnames) {len(images_fnames)} for {annotation_fname}"
            )
            raise RuntimeError(
                f"[E] Error: frame_idx {frame_idx} > len(images_fnames) {len(images_fnames)} for {annotation_fname}"
            )
        curr_ann["spot_pov_image"] = images_fnames[frame_idx]
        curr_ann["spot_pov_depth"] = depths_fnames[frame_idx]
        if raw_depth_folder is not None:
            curr_ann["spot_pov_depth_orig"] = orig_depths_fnames[frame_idx]
    with open(annotation_fname, "wb") as f:
        pickle.dump(data, f)

    return {
        "annotation": annotation_fname,
        "images": images_fnames,
        "depths": depths_fnames,
        "raw_depths": orig_depths_fnames,
    }


def _extract(zips: List[str]):

    if len(zips) == 0:
        raise RuntimeError("No zip files found")

    for z in tqdm(zips, desc="Extracting zips"):
        subj = os.path.basename(z).split("_")[0]
        if subj in test_subjs:
            ann_folder = test_annotations_folder
            img_folder = test_images_folder
            depth_folder = test_depths_folder
            raw_depth_folder = test_raw_depths_folder
            tool_folder = test_tool_folder
        else:
            ann_folder = train_annotations_folder
            img_folder = train_images_folder
            depth_folder = train_depths_folder
            raw_depth_folder = train_raw_depths_folder
            tool_folder = train_tool_folder

        if is_data_broken(z):
            print("Data is broken, removing", z)
            continue

        try:
            extracted = extract_zip(
                z, ann_folder, img_folder, depth_folder, raw_depth_folder, tool_folder
            )
        except zipfile.BadZipFile as e:
            print(f"Error extracting {z}: {e}")
            continue


broken_fnames = []


def is_data_broken(filename: str):
    fname = os.path.basename(filename)
    for broken_fname in broken_fnames:
        if fname.startswith(broken_fname):
            return True
    return False


def unzipper_main(
    data_path: str,
    dst: str,
    broken_file: Optional[str] = None,
    clear_folder: bool = False,
    add_raw_depth: bool = True,
):
    global test_annotations_folder, test_images_folder, test_depths_folder, test_raw_depths_folder, test_tool_folder
    global train_annotations_folder, train_images_folder, train_depths_folder, train_raw_depths_folder, train_tool_folder
    global broken_fnames

    if broken_file is not None:
        with open(broken_file, "rb") as f:
            data = f.readlines()
            data = [d.decode("utf-8").strip() for d in data]
        # broken_fnames = [d.split(" ")[0] + "_" + d.split(" ")[1] for d in data]
        for d in data:
            a = "act" + d.split(" ")[0]
            subj = d.split(" ")[1]
            cam = d.split(" ")[2]
            broken_fnames.append(f"{subj}_{a}_{cam}_")

    if clear_folder:
        if os.path.exists(dst):
            shutil.rmtree(dst, ignore_errors=True)

    train_folder = os.path.join(dst, "train")
    test_folder = os.path.join(dst, "test")

    os.makedirs(dst, exist_ok=True)
    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(test_folder, exist_ok=True)

    train_annotations_folder = os.path.join(train_folder, "annotations")
    train_images_folder = os.path.join(train_folder, "images")
    train_depths_folder = os.path.join(train_folder, "depths")
    train_raw_depths_folder = os.path.join(train_folder, "raw_depths")
    train_tool_folder = os.path.join(train_folder, "tool")

    test_annotations_folder = os.path.join(test_folder, "annotations")
    test_images_folder = os.path.join(test_folder, "images")
    test_depths_folder = os.path.join(test_folder, "depths")
    test_raw_depths_folder = os.path.join(test_folder, "raw_depths")
    test_tool_folder = os.path.join(test_folder, "tool")

    os.makedirs(train_annotations_folder, exist_ok=True)
    os.makedirs(train_images_folder, exist_ok=True)
    os.makedirs(train_depths_folder, exist_ok=True)
    os.makedirs(train_raw_depths_folder, exist_ok=True)
    os.makedirs(train_tool_folder, exist_ok=True)

    os.makedirs(test_annotations_folder, exist_ok=True)
    os.makedirs(test_images_folder, exist_ok=True)
    os.makedirs(test_depths_folder, exist_ok=True)
    os.makedirs(test_raw_depths_folder, exist_ok=True)
    os.makedirs(test_tool_folder, exist_ok=True)

    """
    - train/test
        - annotations (file pkl)
        - images (file png)
        - depths (file npy)
    """

    if not add_raw_depth:
        train_raw_depths_folder = None
        test_raw_depths_folder = None

    # print("Step 1) Extracting action data from zips")
    # zips = glob(f"{data_path}/**/*.zip", recursive=True)
    # _extract(zips)
    # # [os.remove(z) for z in zips]
    print("Extracting to train/test folders")
    zips = glob(f"{data_path}/**/*.zip", recursive=True)
    _extract(zips)
    # [os.remove(z) for z in zips]


if __name__ == "__main__":
    data_path = "data/harper/tmp"
    dst = "data/harper"
    unzipper_main(data_path, dst)
