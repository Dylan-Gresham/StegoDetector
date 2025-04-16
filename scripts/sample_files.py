import argparse
import os
import random
import string


def generate_random_text(max_len=1000, characters=string.ascii_letters + string.digits):
    """
    Helper method to randomly generate text.
    """
    return ''.join(random.choice(characters) for _ in range(random.randint(1, max_len)))


def sample_files(seed: int | None=None):
    """
    Randomly samples 25% of the clean files.

    # Parameters:

    - `seed: Union[int, None]` The seed to use for the random generator. Defaults to `None`.

    # Returns:

    `None`
    """
    # Seed random if given
    if seed is not None:
        random.seed(seed)

    # Confirm that the clean files exist
    if os.path.exists("data/clean") and os.path.isdir("data/clean"):
        print("Found data/clean directory!")
    else:
        print("data/clean directory doesn't exist")
        return None

    dirs = [
        "bike",
        "cars",
        "cats",
        "dogs",
        "flowers",
        "horses",
        "human",
    ]

    # Sample
    with open("sample_files.txt", "w") as f:
        for dir in dirs:
            dir_path = f"data/clean/{dir}"
            if not os.path.isdir(dir_path):
                print(f"[!] Skipping missing directory: {dir_path}")
                continue

            files = [f"{dir}/{entry}" for entry in os.listdir(dir_path) if os.path.isfile(f"{dir_path}/{entry}")]
            num_files_to_sample = round(len(files) * 0.25)

            if files and num_files_to_sample > 0:
                for sample in random.sample(files, num_files_to_sample):
                    f.write(sample + "," + generate_random_text() + "\n")

def main():
    # Parse CLI arguments
    parser = argparse.ArgumentParser(description="Sample 20% of image files from each category in data/clean")
    parser.add_argument("--seed", type=int, help="Optional seed for reproducible sampling")
    args = parser.parse_args()

    # Sample w/potential seed
    sample_files(seed=args.seed)

if __name__ == "__main__":
    main()
