import random
import shutil
from pathlib import Path
from typing import List, Tuple

CLEAN_DIR = Path("data/clean")
STEGO_DIR = Path("data/stego")
OUT_DIR = Path("data")
SPLITS = ("train", "test")
RATIOS = (0.75, 0.25)
SEED = 42

random.seed(SEED)


def gather_image_paths(base_dir: Path) -> List[Path]:
    return [p for p in base_dir.rglob("*") if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp"}]

def split_data(paths: List[Path], ratios: Tuple[float, float]):
    random.shuffle(paths)
    n = len(paths)
    train_end = int(n * ratios[0])

    return paths[:train_end], paths[train_end:]

def copy_files(file_list: List[Path], dest_dir: Path, label: str, base_dir: Path):
    for path in file_list:
        rel_path = path.relative_to(base_dir)
        dest_path = dest_dir / label / rel_path
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(path, dest_path)

def prepare():
    print("[*] Gathering image files...")
    clean_images = gather_image_paths(CLEAN_DIR)
    stego_images = gather_image_paths(STEGO_DIR)

    print(f"[+] Found {len(clean_images)} clean images")
    print(f"[+] Found {len(stego_images)} stego images")

    splits = {}
    for label, images, base in [("clean", clean_images, CLEAN_DIR), ("stego", stego_images, STEGO_DIR)]:
        train, test = split_data(images, RATIOS)
        splits[label] = {"train": train, "test": test}
        for split in SPLITS:
            print(f"[{label}] {split}: {len(splits[label][split])} images")
            copy_files(splits[label][split], OUT_DIR / split, label, base)

    print("[✓] Dataset preparation complete.")

if __name__ == "__main__":
    prepare()
