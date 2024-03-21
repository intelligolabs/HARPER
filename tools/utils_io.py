import pickle as pkl


def load_pickle(pkl_file: str):
    with open(pkl_file, "rb") as f:
        data = pkl.load(f)
    return data
