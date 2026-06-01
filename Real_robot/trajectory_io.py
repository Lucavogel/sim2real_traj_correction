from __future__ import annotations

from pathlib import Path

import numpy as np

UR10_JOINT_NAMES = [
    "shoulder_pan_joint",
    "shoulder_lift_joint",
    "elbow_joint",
    "wrist_1_joint",
    "wrist_2_joint",
    "wrist_3_joint",
]


def dataset_dt(data: np.lib.npyio.NpzFile) -> float:
    if "dt" in data:
        return float(data["dt"])
    if "control_hz" in data:
        return 1.0 / float(data["control_hz"])
    raise KeyError("Dataset must contain either 'dt' or 'control_hz'")


def to_dense_paths(paths: np.ndarray) -> np.ndarray:
    if isinstance(paths, np.ndarray) and paths.dtype == object:
        paths = np.stack(list(paths), axis=0)
    if paths.ndim != 3 or paths.shape[-1] != 6:
        raise ValueError(f"Invalid paths shape: {paths.shape} (expected N,T,6)")
    return paths.astype(np.float32, copy=False)


def to_dense_xyz(xyz: np.ndarray) -> np.ndarray:
    if isinstance(xyz, np.ndarray) and xyz.dtype == object:
        xyz = np.stack(list(xyz), axis=0)
    if xyz.ndim != 3 or xyz.shape[-1] != 3:
        raise ValueError(f"Invalid EE shape: {xyz.shape} (expected N,T,3)")
    return xyz.astype(np.float32, copy=False)


def load_dataset(dataset_path: str | Path) -> np.lib.npyio.NpzFile:
    return np.load(str(Path(dataset_path).expanduser()), allow_pickle=True)


def select_trajectory(data: np.lib.npyio.NpzFile, traj_index: int = 0) -> tuple[np.ndarray, float, np.ndarray | None]:
    paths = to_dense_paths(data["paths"])
    if not (0 <= traj_index < paths.shape[0]):
        raise IndexError(f"traj_index={traj_index} out of range for {paths.shape[0]} trajectories")

    ee = None
    if "ee_ref_pos" in data:
        ee = to_dense_xyz(data["ee_ref_pos"])[traj_index]
    elif "ee_pos" in data:
        ee = to_dense_xyz(data["ee_pos"])[traj_index]

    return paths[traj_index], dataset_dt(data), ee


def upsample_joint_trajectory(raw_path: np.ndarray, source_dt: float, target_hz: float = 125.0) -> np.ndarray:
    if raw_path.ndim != 2 or raw_path.shape[1] != 6:
        raise ValueError(f"Invalid trajectory shape: {raw_path.shape} (expected T,6)")

    num_points = raw_path.shape[0]
    duration = num_points * source_dt
    t_original = np.linspace(0.0, duration, num_points)
    target_steps = int(duration * target_hz)
    t_target = np.linspace(0.0, duration, target_steps)

    smooth_path = np.zeros((target_steps, 6), dtype=float)
    for joint_index in range(6):
        smooth_path[:, joint_index] = np.interp(t_target, t_original, raw_path[:, joint_index])
    return smooth_path
