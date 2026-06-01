import time

from ur10_rtde import RTDEConfig, UR10RTDESession

ROBOT_IP = "192.168.0.60"


def main():
    print(f"Connecting to {ROBOT_IP} for realtime stream benchmark...")

    with UR10RTDESession(RTDEConfig(robot_ip=ROBOT_IP)) as session:
        print("Measuring realtime stream (30003) for 5 seconds...")
        start_time = time.time()
        cycles = 0
        last_ctrl_ts = None

        while time.time() - start_time < 5.0:
            data = session.read(wait=True)
            ctrl_ts = float(data["ctrltimestamp"])
            if last_ctrl_ts is None or ctrl_ts != last_ctrl_ts:
                cycles += 1
                last_ctrl_ts = ctrl_ts

        freq = cycles / 5.0
        print(f"Realtime frequency (30003): {freq:.1f} Hz")


if __name__ == "__main__":
    main()
