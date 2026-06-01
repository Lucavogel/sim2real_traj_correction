import torch

paths = [
    "/home/ajin/workspace/sim2real-pnp/Real_robot/validation_mujoco/policy(1).pt",
    "/home/ajin/workspace/sim2real-pnp/Real_robot/model_converged.pt"
]

for path in paths:
    print(f"\n--- Checking {path} ---")
    try:
        data = torch.load(path, map_location="cpu", weights_only=False)
        if isinstance(data, dict):
            print("Keys:", data.keys())
            if "model_state_dict" in data:
                print("Model State Dict Keys (first 5):", list(data["model_state_dict"].keys())[:5])
            if "optimizer_state_dict" in data:
                print("Optimizer present")
            if "running_mean_std" in data:
                print("Found running_mean_std!")
        else:
            print("Type:", type(data))
            if isinstance(data, torch.jit.ScriptModule):
                print("Is JIT ScriptModule")
                print("Named params:", [name for name, _ in data.named_parameters()])
    except Exception as error:
        print(f"Error loading: {error}")
