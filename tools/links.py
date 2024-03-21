human_links = [
    [0, 1],  # hip -> ab
    [1, 2],  # ab -> chest
    [2, 3],  # chest -> neck
    [3, 4],  # neck -> head
    [3, 5],  # neck, L shoulder
    [5, 6],  # L shoulder, L U arm
    [6, 7],  # L u arm, L l f arm
    [7, 8],  # L f arm, L hand
    [3, 9],  # neck, R shoulder
    [9, 10],  # R shoulder, R U arm
    [10, 11],  # R u arm, R l f arm
    [11, 12],  # R f arm, R hand
    [0, 13],  # hip, LShin
    [13, 14],  # LShin, LTigh
    [14, 15],  # LTigh, LFoot
    [15, 16],  # LFoot, Ltoe
    [0, 17],  # hip, RShin
    [17, 18],  # RShin, RTigh
    [18, 19],  # RTigh, RFoot
    [19, 20],  # RFoot,RLtoe
    [6, 13],  # LShin to L u arm  (hip to shoulder)
    [10, 17],  # RShin to R u arm  (hip to shoulder)
]

spot_links = [
    # 0 Is the center of the body (i.e. optitrack maker), added manually during loading
    # [1, 4],# between legs; long side
    [4, 10],  # between legs; short side
    # [10, 7],# between legs; long side
    [7, 1],  # between legs; short side
    [1, 2],  # leg1 hip-knee
    [2, 3],  # leg1 knee-foot
    [4, 5],  # leg2
    [5, 6],  # leg2
    [7, 8],  # leg3
    [8, 9],  # leg3
    [10, 11],  # leg4
    [11, 12],  # leg4
    [13, 14],
    [14, 16],
    [16, 15],
    [15, 13],
    [17, 18],
    [18, 20],
    [20, 19],
    [19, 17],
    [13, 17],
    [14, 18],
    [15, 19],
    [16, 20],
    [0, 21],  # center(body) - wrist
    [21, 22],  # wrist-hand
]