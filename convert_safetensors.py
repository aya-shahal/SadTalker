from safetensors.torch import load_file
import torch
import os

folder = "./checkpoints"
for fname in os.listdir(folder):
    if fname.endswith(".safetensors"):
        path = os.path.join(folder, fname)
        data = load_file(path)
        new_path = path.replace(".safetensors", ".pth")
        torch.save(data, new_path)
        print(f"✅ Converted {fname} -> {os.path.basename(new_path)}")
