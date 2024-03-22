import os
from glob import glob
import torch
from torch.utils.data import Dataset
from tqdm import tqdm

from tools.utils_io import load_pkl


class Harper3D(Dataset):
    """
    Data loader for the Harper (3D) dataset.
    This data loader is designed to provide data for forecasting, but can easily adapted as per your needs.
    """

    def __init__(self, data_path: str, split: str, n_input: int, n_output: int) -> None:
        # Sanity checks
        assert os.path.exists(data_path), f"Path {data_path} does not exist. Please download the dataset first"
        assert split in ["train", "test"], f"Split {split} not recognized. Use either 'train' or 'test'"
        data_folder = os.path.join(data_path, split)
        assert os.path.exists(data_folder), f"Path {data_folder} does not exist. It is in the correct format? Refer to the README"
        assert n_input > 0 and isinstance(n_input, int), f"n_input must be an integer greater than 0"
        assert n_output > 0 and isinstance(n_output, int), f"n_output must be an integer greater than 0"

        # Load data
        self.n_input = n_input
        self.n_output = n_output
        pkls_files: list[str] = glob(os.path.join(data_folder, "*.pkl"))
        self.all_sequences: list[dict[int, dict]] = [load_pkl(f) for f in pkls_files]

        # list of slding windows on sequences
        # NOTE: if you need to select a specific subject and action, you can find it in every dictionary under "subject" and "action" keys
        self.all_sequences_windows = []
        for sequence in self.all_sequences:
            sequence_list: list[dict] = [v for k, v in sequence.items()]
            for i in range(len(sequence_list) - n_input - n_output + 1):
                self.all_sequences_windows.append(sequence_list[i : i + n_input + n_output])

    def __len__(self):
        return len(self.all_sequences_windows)

    def __getitem__(self, idx) -> "dict[str, torch.Tensor|str]":
        curr_data = self.all_sequences_windows[idx]
        subject = curr_data[0]["subject"]
        action = curr_data[0]["action"]
        observation = curr_data[: self.n_input]
        future = curr_data[self.n_input :]

        return {
            "subject": subject,
            "action": action,
            "human_observation": torch.tensor([obs["human_joints_3d"] for obs in observation], dtype=torch.float32),
            "human_future": torch.tensor([fut["human_joints_3d"] for fut in future], dtype=torch.float32),
            "spot_observation": torch.tensor([obs["spot_joints_3d"] for obs in observation], dtype=torch.float32),
            "spot_future": torch.tensor([obs["spot_joints_3d"] for obs in future], dtype=torch.float32),
        }


def __test__():

    # testing dataset
    dataset = Harper3D(data_path="data/harper_3d_30", split="train", n_input=10, n_output=10)
    print("Dataset size: ", len(dataset))
    print("Testing dataset")
    for i in tqdm(range(len(dataset)), total=len(dataset), desc="Testing dataset"):
        if i == 0:
            print("Datum ", i)
            print("Keys: ", list(dataset[i].keys()))
            print("Human observation shape: ", dataset[i]["human_observation"].shape)
            print("Human future shape: ", dataset[i]["human_future"].shape)
            print("Spot observation shape: ", dataset[i]["spot_observation"].shape)
            print("Spot future shape: ", dataset[i]["spot_future"].shape)
    print("Dataset testing done")

    # testing dataloader
    from torch.utils.data import DataLoader

    dl = DataLoader(dataset, batch_size=4, shuffle=True)
    for i, batch in tqdm(enumerate(dl), total=len(dl), desc="Testing dataloader"):
        if i == 0:
            print("Batch ", i)
            print("Keys: ", list(batch.keys()))
            print("Human observation shape: ", batch["human_observation"].shape)
            print("Human future shape: ", batch["human_future"].shape)
            print("Spot observation shape: ", batch["spot_observation"].shape)
            print("Spot future shape: ", batch["spot_future"].shape)

    print("Testing done, everything is ready!")


if __name__ == "__main__":
    __test__()
