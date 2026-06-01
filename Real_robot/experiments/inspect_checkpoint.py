import torch

path = "/home/ajin/workspace/sim2real-pnp/Real_robot/model_converged.pt"
print(f"\n--- Deep Check {path} ---")
data = torch.load(path, map_location="cpu", weights_only=False)
state_dict = data["model_state_dict"]
print("All Keys in model_state_dict:")
for key in state_dict.keys():
    print(key)
