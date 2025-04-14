from pathlib import Path
from typing import List, Tuple

import torchvision.transforms as transforms
from PIL import Image
from torch.utils.data import Dataset


class StegoDataset(Dataset):
    def __init__(self, root_dir, transform=None):
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


    def __getitem__(self, index):
        path, label = self.samples[index]
        image = Image.open(path).convert("RGB")
        if self.transform:
            image = self.transform(image)

        return image, label

    def __len__(self):
        return len(self.samples)
