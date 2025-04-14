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
    transform = T.Compose([T.Resize((224, 224)), T.ToTensor()])
    train_data = StegoDataset("data/train", transform=transform)
    train_loader = DataLoader(train_data, batch_size=16, shuffle=True)

    model = get_model()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
    criterion = nn.CrossEntropyLoss()

    for epoch in range(5):
        model.train()

        loss = None
        for imgs, labels in tqdm(train_loader):
            imgs, labels = imgs.to(device), labels.to(device)
            preds = model(imgs)
            loss = criterion(preds, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        if loss is not None:
            print(f"Epoch {epoch + 1} | Loss: {loss.item():.4f}")

    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    torch.save(model.state_dict(), SAVE_PATH)

    print(f"[✓] Model saved to {SAVE_PATH}")

if __name__ == "__main__":
    main()
