#!/usr/bin/env python3
# ============================================================
# Restore asset from release
# ============================================================

import os
import requests
from pathlib import Path

print("=" * 50)
print("Restoring asset from release")
print("=" * 50)

RELEASE_TAG = "v1.0.0"
REPO_OWNER = "kimochione"
REPO_NAME = "man1festo-cpu"

# Construct download URL
download_url = f"https://github.com/{REPO_OWNER}/{REPO_NAME}/releases/download/{RELEASE_TAG}/model.gguf"

dest_path = Path("/content/VERTA_Train/models/model.gguf")
dest_path.parent.mkdir(parents=True, exist_ok=True)

print(f"\n📥 Downloading from: https://huggingface.co/VLTX/VertaLily-1.2-1B-GGUF/resolve/main/VertaLily-1.2-1B-Q4_K_M-stable.gguf")
print(f"📂 Saving to: /content/VERTA_Train/models/VertaLily-1.2-1B-Q4_K_M-stable.gguf")

# Download with progress
response = requests.get(download_url, stream=True)
total_size = int(response.headers.get('content-length', 0))

with open(dest_path, 'wb') as f:
    downloaded = 0
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)
        downloaded += len(chunk)
        if total_size > 0:
            percent = (downloaded / total_size) * 100
            print(f"\r   Progress: {percent:.1f}%", end="", flush=True)
print()

print(f"\n✅ Restored to: {dest_path}")
print(f"   Size: {dest_path.stat().st_size / (1024*1024):.2f} MB")
