# Scripts Layout

This folder keeps the active Isaac Lab entry points at the top level and moves the noisy one-off utilities into subfolders.

## Top Level

- `zero_agent.py`, `random_agent.py`, `list_envs.py`: small Isaac Lab entry points
- `isaaclab_deploy_policy_npz.py`: deployment inside Isaac Lab
- `track_trajectory_open_loop.py`: baseline open-loop rollout
- `ur10_ros2_cfg.py`: shared UR10 config
- `rsl_rl/`: training and inference entry points for RL

## Analysis

- `analysis/plot_deploy_log.py`: visualize rollout logs
- `analysis/plot_for_report.py`: generate publication figures

## Legacy

The `legacy/` folder contains older exploratory scripts that are not part of the main workflow anymore.

## Data And Outputs

- `*.npz` files: recorded trajectories and datasets
- `logs_deploy/`: saved rollout logs
- `report_figures/`: generated report images

The idea is to keep the main scripts easy to find without deleting the historical material that may still be useful.