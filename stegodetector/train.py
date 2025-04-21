import os

import torch
import torchvision.transforms as T
from torch import nn
from torch.utils.data import DataLoader
from tqdm.auto import tqdm

from stegodetector.dataset import StegoDataset
from stegodetector.model import get_model

SAVE_PATH = "model_output/stego_classifier.pt"


def main():
    """Trains a ResNet model for steganography detection."""
    # Load data
    transform = T.Compose([T.Resize((224, 224)), T.ToTensor()])
    train_data = StegoDataset("data/train", transform=transform)
    train_loader = DataLoader(train_data, batch_size=16, shuffle=True)

    # Set up the base model
    model = get_model()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.train()

    # Define hyperparameters
    # TODO: Define optimizer
    optimizer = None
    # TODO: Define loss function
    criterion = None

    # Training loop
    for epoch in range(5):
        loss = None
        for imgs, labels in tqdm(train_loader):
            imgs, labels = imgs.to(device), labels.to(device)
            # TODO: Get predictions

            # TODO: Compute loss

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        if loss is not None:
            print(f"Epoch {epoch + 1} | Loss: {loss.item():.4f}")

    # Output the trained model
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)

    # TODO: Save it!

    print(f"[✓] Model saved to {SAVE_PATH}")


if __name__ == "__main__":
    main()
