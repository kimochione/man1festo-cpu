#!/usr/bin/env python3
# ============================================================
# RESTORE LLAMA.CPP BINARIES FROM GITHUB
# ============================================================

import os
import requests
import subprocess
from pathlib import Path

print("=" * 80)
print("💜 RESTORE LLAMA.CPP BINARIES")
print("=" * 80)

REPO_OWNER = "kimochione"
REPO_NAME = "man1festo-cpu"
BRANCH = "main"
API_URL = f"https://api.github.com/repos/{{REPO_OWNER}}/{{REPO_NAME}}/contents/llama_cpp_binaries"

INSTALL_DIR = Path("/content/llama_cpp_restored")
BIN_DIR = INSTALL_DIR / "bin"
LIB_DIR = INSTALL_DIR / "lib"

INSTALL_DIR.mkdir(parents=True, exist_ok=True)
BIN_DIR.mkdir(parents=True, exist_ok=True)
LIB_DIR.mkdir(parents=True, exist_ok=True)

def download_file(url, dest_path):
    response = requests.get(url, stream=True)
    with open(dest_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    os.chmod(dest_path, 0o755)

def download_dir(api_path, local_dir):
    response = requests.get(f"{API_URL}{api_path}")
    if response.status_code != 200:
        return 0
    count = 0
    for item in response.json():
        if item['type'] == 'file':
            local_path = local_dir / item['name']
            print(f"   Downloading {{item['name']}}...")
            download_file(item['download_url'], local_path)
            count += 1
        elif item['type'] == 'dir':
            subdir = local_dir / item['name']
            subdir.mkdir(exist_ok=True)
            count += download_dir(f"/{{item['name']}}", subdir)
    return count

print("\n📥 Downloading binaries...")
total = download_dir("", INSTALL_DIR)
print(f"\n✅ Downloaded {{total}} files")

# Create symlinks
for target in ['llama-cli', 'llama-server', 'llama-quantize']:
    src = BIN_DIR / target
    if src.exists():
        link = Path("/content") / target
        if link.exists():
            link.unlink()
        link.symlink_to(src)
        print(f"   ✅ Created: /content/{{target}}")

print("\n" + "=" * 80)
print("💜 Restore complete!")
print("=" * 80)
