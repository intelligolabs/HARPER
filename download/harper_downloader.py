import os
import tarfile
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

os.makedirs(args.dst_folder, exist_ok=True)
fname = os.path.join(args.dst_folder, "harper_data.tar.gz")
if os.path.isfile(fname):
    print(f"{fname} already exists. Deleting it to download again...")
    os.remove(fname)
download_onedrive_file(HARPER_DATA, fname)

with tarfile.open(fname, "r:gz") as tar:
    tar.extractall(args.dst_folder)
os.remove(fname)
