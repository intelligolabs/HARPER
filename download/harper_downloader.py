import argparse
import os
import shutil
from typing import Dict
import zipfile

from download.unzipper import unzipper_main

argparser = argparse.ArgumentParser()
argparser.add_argument("--dst", help="dst folder", default="data/harper")
argparser.add_argument(
    "--broken_file", help="path of broken sequences", default=None
)
args = argparser.parse_args()

dst = args.dst
broken_file = args.broken_file

if broken_file is None or not os.path.exists(broken_file):
    print(f"[W] Broken file {broken_file} does not exist, using empty list")
    broken_file = None
else:
    print(f"[I] Using broken file {broken_file}")
    with open(broken_file, "r") as f:
        broken_filedata = f.read().splitlines()
        print(f"[I] Found {len(broken_filedata)} broken files")
        print(broken_filedata)

os.makedirs(dst, exist_ok=True)

# Note: if link is broken, contact  federico.cunico@univr.it  to get the link expiration extended
ALL_FILES = {
    "avo": "https://univr-my.sharepoint.com/:u:/g/personal/federico_cunico_univr_it/EYLYus2SO2hFieVyoyboWcoBbOiFdhRZ-_BbRU9eZWhuXA?e=hgKPgB",
    "bn": "https://univr-my.sharepoint.com/:u:/g/personal/federico_cunico_univr_it/EWjNrf2EP01LsuwAliGuNV8BvqJs0rFd6QF5rD8ONdJuoQ?e=sKhxzu",
    "cun": "https://univr-my.sharepoint.com/:u:/g/personal/federico_cunico_univr_it/EVvMOPUoP1JBjJaX9VAjzXsB45QAK2kgphLogXpBITFxcg?e=jfcqpM",
    "el": "https://univr-my.sharepoint.com/:u:/g/personal/federico_cunico_univr_it/EYBzt6JoIVBBsXk_cECQEK8B_nmG7YYBbu6f3nCHBpCLGg?e=J87Rw2",
    "h": "https://univr-my.sharepoint.com/:u:/g/personal/federico_cunico_univr_it/EYMCa17HZshAn91TzOCpgfYBm0pe_CRmwUJw_d3n6FtVjg?e=i3vObI",
    "j": "https://univr-my.sharepoint.com/:u:/g/personal/federico_cunico_univr_it/ETwPtJt0ZRFGlSYLqB_umAoBWLHgis7KSoG5uxzH1MdGrw?e=OFFdCh",
    "jk": "https://univr-my.sharepoint.com/:u:/g/personal/federico_cunico_univr_it/Eczq1HgDC6ZFhR3M8adozcIBo5KDtjQnkZ4HMpLQe_BeyQ?e=rLewG3",
    "mt": "https://univr-my.sharepoint.com/:u:/g/personal/federico_cunico_univr_it/EXy24fbN2ANPudveHOWy2bUB8QprW6Pq1GyRzz6qShv_VA?e=pMWIDJ",
    "ric": "https://univr-my.sharepoint.com/:u:/g/personal/federico_cunico_univr_it/EYkhf9cO9fxFo00gI-N9nqsB79NFaMMXeRmrZTcKH6FTkQ?e=NlpAGT",
    "ry": "https://univr-my.sharepoint.com/:u:/g/personal/federico_cunico_univr_it/EUt5ZL6SuuNDmSY-IwUjHp0BAmk_41bkgvAsLILjVZgRxA?e=Ua7mRb",
    "sh": "https://univr-my.sharepoint.com/:u:/g/personal/federico_cunico_univr_it/EfXG-nO0zYRBnKH2aednxmcBW-5eoY0tAcAfmnu65G331w?e=HueY2J",
    "son": "https://univr-my.sharepoint.com/:u:/g/personal/federico_cunico_univr_it/Ef2J5nYQ-kRPlanvGgJIBxIBXdwXLlY33yAJHU1_PLTsZA?e=Fpq1Z1",
    "t": "https://univr-my.sharepoint.com/:u:/g/personal/federico_cunico_univr_it/EThvah4SM3JBldn_sBQfqjABvxQX25t4c88xwvi6xzx8Dw?e=tHbV1o",
    "toa": "https://univr-my.sharepoint.com/:u:/g/personal/federico_cunico_univr_it/EcAtXOqtInZKuiwSdMjgV0kBVml9j6VWeJ_6qQp8-AQ0gw?e=8J22af",
    "xu": "https://univr-my.sharepoint.com/:u:/g/personal/federico_cunico_univr_it/EasjA-sqGk9Gmvq1eXwvLaoBWfITQFGPWNxKJMb3Na2q9w?e=gXk4eo",
    "xy": "https://univr-my.sharepoint.com/:u:/g/personal/federico_cunico_univr_it/EZTb7tT-oXlFhCI4XMqqlRkBXbXQHQjvkEKYoPJb7PnvpQ?e=YJxywG",
    "yf": "https://univr-my.sharepoint.com/:u:/g/personal/federico_cunico_univr_it/EXp2vDxE5VtEuEXl_Nx15LMBNtRcjEQgclQ_mAd8ITX-jA?e=yZFCd1",
}


def download(url, filename) -> bool:
    import requests

    url += "&download=1"
    print("Downloading from", url, "to", filename)
    response = requests.get(url)
    if response.status_code == 200:
        print("Downloaded", len(response.content), "bytes")
        content = response.content

        # save the content to a file
        with open(filename, "wb") as file:
            file.write(content)
        print("Saved to", filename)
        return True
    else:
        return False


def download_dataset(tmp_dst: str, ALL_FILES: Dict[str, str]):
    lock_file = os.path.join(tmp_dst, "lock")
    if os.path.exists(lock_file):
        print("Dataset already downloaded...")
        return
    print("Downloading dataset to", tmp_dst)
    for subj, url in ALL_FILES.items():
        filename = os.path.join(tmp_dst, f"{subj}.zip")
        if not os.path.exists(filename):
            ret = False
            attempts = 0
            while not ret:
                if attempts > 5:
                    break
                try:
                    ret = download(url, filename)
                except Exception as e:
                    attempts += 1
                    if not ret:
                        print(f"[E] error while downloading to {filename}. Attempts={attempts}")
        else:
            print("File already exists", filename)

    for subj, url in ALL_FILES.items():
        filename = os.path.join(tmp_dst, f"{subj}.zip")
        if not os.path.exists(filename):
            print("Error downloading", filename)
            continue
        with zipfile.ZipFile(filename, "r") as zip_ref:
            zip_ref.extractall(os.path.join(tmp_dst, subj))
            print("Extracted", filename, "to", dst)
        os.remove(filename)

    with open(lock_file, "w") as f:
        f.write("done")
    print("Dataset downloaded to", tmp_dst)


# ================================================================

tmp_dst = os.path.join(dst, "tmp")
os.makedirs(tmp_dst, exist_ok=True)
download_dataset(tmp_dst, ALL_FILES)
unzipper_main(tmp_dst, dst, broken_file)
shutil.rmtree(tmp_dst, ignore_errors=True)
