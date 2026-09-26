import os
import glob
from collections import defaultdict

root_dir = 'C:/Users/umang/SIH'

def get_dir_size_and_count(start_path):
    total_size = 0
    total_count = 0
    for dirpath, _, filenames in os.walk(start_path):
        if 'node_modules' in dirpath or '.git' in dirpath or 'venv' in dirpath:
            continue
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
                total_count += 1
    return total_count, total_size

def list_level_one(folder):
    path = os.path.join(root_dir, folder)
    if not os.path.exists(path):
        return "Folder does not exist."
    items = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            items.append(f"{item}/")
        else:
            items.append(item)
    return ", ".join(items)

print("=== 1. Level 1 Contents ===")
folders_to_check = ['data', 'DATASETS', 'MODELS', 'SIH-AI-ML', 'SIH-BACKEND', 'SIH-FRONTEND']
for f in folders_to_check:
    print(f"[{f}]: {list_level_one(f)}")

print("\n=== 2. Overlap/Duplication Checks ===")
# data vs DATASETS
print("Comparing data/ and DATASETS/:")
def get_all_files(folder):
    files = []
    path = os.path.join(root_dir, folder)
    if not os.path.exists(path): return set()
    for dp, _, fn in os.walk(path):
        for f in fn:
            files.append(os.path.relpath(os.path.join(dp, f), path))
    return set(files)

data_files = get_all_files('data')
datasets_files = get_all_files('DATASETS')
print(f"data/ files: {len(data_files)}")
print(f"DATASETS/ files: {len(datasets_files)}")
print(f"Common filenames (by relative path): {data_files.intersection(datasets_files)}")
print(f"Only in data: {[f for f in data_files if os.path.basename(f) not in [os.path.basename(x) for x in datasets_files]]}")
print(f"Only in DATASETS: {[f for f in datasets_files if os.path.basename(f) not in [os.path.basename(x) for x in data_files]]}")

# MODELS vs SIH-AI-ML
print("\nComparing MODELS/ and SIH-AI-ML/:")
models_files = get_all_files('MODELS')
sih_aiml_files = get_all_files('SIH-AI-ML')
print(f"MODELS/ files: {len(models_files)}")
print(f"SIH-AI-ML/ files: {len(sih_aiml_files)}")

# SIH-BACKEND internal folders
print("\nSIH-BACKEND/ internal folders check:")
print("SIH-BACKEND contents:")
for sub in ['aiml', 'models', 'data']:
    sub_path = os.path.join(root_dir, 'SIH-BACKEND', sub)
    if os.path.exists(sub_path):
        print(f"  Found {sub}/ with {len(os.listdir(sub_path))} items.")
    else:
        print(f"  No {sub}/ folder found.")

print("\n=== 3. Loose .py Files ===")
root_py_files = [f for f in os.listdir(root_dir) if f.endswith('.py') and os.path.isfile(os.path.join(root_dir, f))]
for f in root_py_files:
    with open(os.path.join(root_dir, f), 'r', encoding='utf-8', errors='ignore') as file:
        lines = [file.readline().strip() for _ in range(5)]
    print(f"{f}: {lines}")

print("\n=== 4. Sizes and Counts ===")
for folder in folders_to_check:
    path = os.path.join(root_dir, folder)
    if os.path.exists(path):
        cnt, sz = get_dir_size_and_count(path)
        print(f"{folder}/: {cnt} files, {sz / 1024 / 1024:.2f} MB")
