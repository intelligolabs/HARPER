# Exploring 3D Human Pose Estimation and Forecasting from the Robot’s Perspective: The HARPER Dataset

We propose the Human from an Articulated Robot Perspective: the HARPER dataset!


## Dataset Description
Refer to main paper - coming soon!

## Dataset Splits
Coming soon!

## 3D panoptic data
The dataset has two points of view: the panoptic point of view and the robot's perspective point of view. 
The first one is obtained using a 6-camera OptiTrack MoCap system. Thanks to it, the human skeleton pose (21x3) and the Spot skeleton can be located in the same 3D reference system.

For the sake of completeness, we provide the 3D panoptic data [here](https://univr-my.sharepoint.com/:f:/g/personal/federico_cunico_univr_it/Esk9qR4fKyFBg05UdXK0YSYBY8JvLHpY2Bis2xyX1pcVWg). 
To download and create the data structure with train and test splits you can use the following code:

```bash
PYTHONPATH=. python download/harper_3d_downloader.py --dst_folder ./data
```

This will generate the following tree structure:

```
data
├── harper_3d_120
│   ├── test
│   │   ├── subj_act_120hz.pkl
│   │   ├── ...
│   │   └── subj_act_120hz.pkl
│   └── train
│       ├── subj_act_120hz.pkl
│       ├── ...
│       └── subj_act_120hz.pkl
└── harper_3d_30
    ├── test
    │   ├── subj_act_30hz.pkl
    │   ├── ...
    │   └── subj_act_30hz.pkl
    └── train
        ├── subj_act_30hz.pkl
        ├── ...
        └── subj_act_30hz.pkl

```

Each `.pkl` file contains a dictionary with the frame index as key and the following values:
- `frame`: the frame index
- `subject`: the subject id
- `action`: the action id
- `human_joints_3d`: the 3D human pose (21x3)
- `spot_joints_3d`: the 3D Spot pose (22x3)

A torch dataloader will be provided soon.

## Visualize the 3D panoptic data
To visualize the 3D panoptic data you can use the following code:

```bash
PYTHONPATH=. python tools/visualization/visualize_3d.py --pkl_file ./data/harper_3d_30/train/cun_act1_30hz.pkl
```


## Complete Dataset
Coming soon!
In the meantime you can take a look at the 3D panoptic data, particularly if you are interested in 3D human pose forecasting tasks.
