import time

import numpy as np

from ur10_rtde import RTDEConfig, UR10RTDESession

TEST_DURATION = 10.0


def main():
    print("Connecting to 192.168.0.60 for FULL CONTROL LOOP test...")

    with UR10RTDESession(RTDEConfig(socket_timeout=1.0, servo_t=0.08)) as session:
        print("Socket connected. Measuring Round-Trip Frequency...")

        init_data = session.read(wait=True)
        q_hold = list(init_data["qActual"])

        timestamps = []
        start_time = time.time()
        loop_count = 0

        while time.time() - start_time < TEST_DURATION:
            session.read(wait=True)
            session.send_servoj(q_hold, t=0.08)
            timestamps.append(time.time())
            loop_count += 1

        deltas = np.diff(timestamps)
        avg_dt = np.mean(deltas)
        std_dt = np.std(deltas)
        freq = 1.0 / avg_dt

        print("\n" + "=" * 40)
        print("RESULTS: FULL CONTROL LOOP FREQUENCY")
        print("=" * 40)
        print(f"Loop Type:        Read + Write")
        print(f"Total Cycles:     {loop_count}")
        print(f"Working Freq:     {freq:.2f} Hz")
        print(f"Avg Interval:     {avg_dt * 1000:.2f} ms")
        print(f"Jitter (StdDev):  {std_dt * 1000:.3f} ms")
        print("=" * 40)

        if 120 < freq < 130:
            print("🚀 ELITE PERFORMANCE: 125 Hz Loop.")
            print("Set Isaac Lab Physics dt=0.008")
        elif 60 < freq < 65:
            print("✅ STANDARD PERFORMANCE: 62.5 Hz Loop.")
            print("Set Isaac Lab Physics dt=0.016 (Decimation 2)")
        elif 40 < freq < 45:
            print("⚠️ SLOW: 41 Hz Loop.")
            print("Set Isaac Lab Physics dt=0.024")
        else:
            print("❓ UNSTABLE: Frequency is erratic.")

        session.stopj(1.0)


if __name__ == "__main__":
    main()
