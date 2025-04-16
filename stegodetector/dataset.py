from pathlib import Path
from typing import List, Tuple

import torchvision.transforms as transforms
from PIL import Image
from torch.utils.data import Dataset


class StegoDataset(Dataset):
    """Dataset class for our StegoDetector problem."""
    def __init__(self, root_dir: str, transform=None):
        """
        Gathers all of the image paths and assigns binary labels to them. 0 = clean, 1 = stego.

        # Parameters:

        - `root_dir: str` The root directory of the dataset
        - `transform` The transformations to apply to the images. Should come from `torchvision.transforms`.

        Returns:

        A `StegoDataset` instance.
        """
        self.root_dir = Path(root_dir)
        self.transform = transform or transforms.ToTensor()
        self.image_paths: List[Path] = list(self.root_dir.rglob("*"))
        self.image_paths = [p for p in self.image_paths if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp"}]

        self.samples: List[Tuple[Path, int]] = []
        for path in self.image_paths:
            normalized_path = str(path).replace("\\", "/")
            if "/clean/" in normalized_path:
                label = 0
            elif "/stego/" in normalized_path:
                label = 1
            else:
                raise ValueError(f"Could not determine label for path: {path}")

            self.samples.append((path, label))


    def __getitem__(self, index: int):
        """
        Gets the image and label associated with the requested index.

        # Parameters:

        - `index: int` The index to retrieve.

        # Returns:

        A tuple in which the first element is the transformed image and the second is the label.
        """
        path, label = self.samples[index]
        image = Image.open(path).convert("RGB")
        if self.transform:
            image = self.transform(image)

        return image, label

    def __len__(self):
        """Returns the length of this dataset. Length = number of images."""
        return len(self.samples)
