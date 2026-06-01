from pathlib import Path
import sys
import time

import numpy as np
import urx

sys.path.append(str(Path(__file__).resolve().parents[1]))

from ur10_rtde import RTDEConfig, UR10RTDESession

DURATION = 10.0
AMPLITUDE = 0.1
SERVO_T = 0.1
MAX_STEP_CHANGE = 0.05


def main():
    print("🔒 Connecting to 192.168.0.60 with SAFETY CHECKS...")

    with UR10RTDESession(RTDEConfig(socket_timeout=1.0, servo_t=SERVO_T)) as session:
        print("✅ Connection Established.")

        init_data = session.read(wait=True)
        start_q = np.array(init_data["qActual"])

        print(f"Initial Q: {np.round(start_q, 3)}")
        print("Starting Smooth Sine Wave on Wrist 3...")
        print("⚠️  KEEP HAND ON E-STOP BUTTON.")

        start_time = time.time()
        loop_count = 0

        while True:
            elapsed = time.time() - start_time
            if elapsed >= DURATION:
                print("Time limit reached.")
                break

            session.read(wait=True)

            offset = AMPLITUDE * np.sin(2 * np.pi * 0.5 * elapsed)
            target_q = start_q.copy()
            target_q[0] += offset

            current_q = np.array(session.read()["qActual"])
            diff = np.max(np.abs(target_q - current_q))

            if diff > 0.2:
                print(f"⛔ EMERGENCY STOP: Target deviation too high ({diff:.3f} rad)")
                break

            session.send_servoj(target_q, t=SERVO_T)
            loop_count += 1

        total_time = time.time() - start_time
        freq = loop_count / total_time
        print(f"Finished. Frequency: {freq:.1f} Hz")


if __name__ == "__main__":
    main()
