import os
import random
import shutil
from pathlib import Path
from typing import List, Tuple

# Define constants
CLEAN_DIR = Path("data/clean")
STEGO_DIR = Path("data/stego")
OUT_DIR = Path("data")
SPLITS = ("train", "test")
RATIOS = (0.75, 0.25)
SEED = 42

random.seed(SEED)  # Seed random for reproducability


def gather_image_paths(base_dir: Path) -> List[Path]:
    """
    Gets the paths to all of the images for our datasets.

    # Parameters:

    - `base_dir: Path` The file path to the base directory of our data.

    # Returns:
    
    A list of `Path`s.
    """
    if os.path.exists(base_dir) and os.path.isdir(base_dir):
        return [p for p in base_dir.rglob("*") if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp"}]
    else:
        raise FileNotFoundError(f"{base_dir} does not exist.")

def split_data(paths: List[Path], ratios: Tuple[float, float]) -> Tuple[List[Path], List[Path]]:
    """
    Splits the data into a train and test split.

    # Parameters:

    - `paths: List[Path]` The array of `Path`s to produce the splits from.
    - `ratios: Tuple[float, float]` The sizes of the two splits. Should sum to 1.0.

    # Returns:

    A two element Tuple in which the first element is the train split and the second is the test split.
    """
    if sum(ratios) != 1.0:
        raise ValueError("Ratios do not sum to 1")
    elif len(paths) <= 0:
        raise ValueError("No paths were provided to generate splits from.")

    random.shuffle(paths)
    n = len(paths)
    train_end = int(n * ratios[0])

    return paths[:train_end], paths[train_end:]

def copy_files(file_list: List[Path], dest_dir: Path, label: str, base_dir: Path) -> None:
    """
    Copies files to the destination directory.

    Helper method for keeping the file structure clean and organized.

    # Parameters:

    - `file_list: List[Path]` The list of file paths to copy
    - `dest_dir: Path` The directory to copy the files to
    - `label: str` The label of the file (clean/stego)
    - `base_dir: Path` The base directory of where the files are

    # Returns:

    `None`
    """
    for path in file_list:
        rel_path = path.relative_to(base_dir)
        dest_path = dest_dir / label / rel_path
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(path, dest_path)

def prepare():
    """
    Wrapper method to split the data into the train/test split and then copy to
    a directory.

    # Parameters:

    `None`

    # Returns:

    `None`
    """
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
