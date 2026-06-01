from pathlib import Path
import sys
import time

import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1]))

from trajectory_io import load_dataset, select_trajectory, upsample_joint_trajectory
from ur10_rtde import DEFAULT_ROBOT_IP, ROBOT_DT, ROBOT_FREQ, RTDEConfig, UR10RTDESession

DATASET_FILE = Path(__file__).resolve().parents[1] / "dataset.npz"
SERVO_T = 0.08


def main() -> None:
    print(f"📂 Loading {DATASET_FILE}...")
    data = load_dataset(DATASET_FILE)
    raw_path, file_dt, _ = select_trajectory(data, traj_index=0)

    print(f"   Data shape: {data['paths'].shape}")
    print(f"   Recorded freq: {1.0 / file_dt:.1f} Hz (dt={file_dt:.3f}s)")

    path_125hz = upsample_joint_trajectory(raw_path, file_dt, ROBOT_FREQ)
    start_q = path_125hz[0]
    end_q = path_125hz[-1]

    print(f"\n🔌 Connecting to {DEFAULT_ROBOT_IP}...")

    with UR10RTDESession(RTDEConfig(servo_t=SERVO_T)) as session:
        print("✅ Connected.")

        print("\n🚀 Moving to START position (slow movej)...")
        current_q = session.current_q()
        dist = float(np.max(np.abs(current_q - start_q)))
        print(f"   Distance to start: {dist:.3f} rad")

        session.send_movej(start_q, a=0.5, v=0.5)
        time.sleep(dist / 0.3 + 1.0)

        current_q = session.current_q()
        if np.max(np.abs(current_q - start_q)) > 0.05:
            print("⚠️ Robot did not reach the start pose exactly.")

        print("\n▶️ Executing trajectory (125 Hz streaming)...")
        print("   HOLD E-STOP.")

        start_time = time.time()
        for step_index, q in enumerate(path_125hz):
            session.read(wait=True)
            session.send_servoj(q, t=SERVO_T)

            if step_index % 125 == 0:
                print(f"   Step {step_index}/{len(path_125hz)}")

        total_time = time.time() - start_time
        print(f"\n✅ Finished in {total_time:.2f}s (expected: {len(path_125hz) * ROBOT_DT:.2f}s)")
        print(f"   Final joint delta: {np.max(np.abs(path_125hz[-1] - end_q)):.6f}")

        session.stopj(2.0)


if __name__ == "__main__":
    main()
