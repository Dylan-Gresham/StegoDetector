import torch
import torch.nn as nn
from torch._C import device
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.models import ResNet
from tqdm.auto import tqdm

from stegodetector.dataset import StegoDataset
from stegodetector.model import get_model


def evaluate(model: ResNet, dataloader: DataLoader, device: device):
    """
    Evaluates a given model.

    # Parameters:

    - `model: ResNet` The model to evaluate
    - `dataloader: DataLoader` The dataloader to get data from
    - `device: device` The device to put the model and data on for classification

    # Returns:

    A tuple in which the first element is the averge loss throughout the data samples and
    the second is the accuracy.
    """
    model.eval()
    criterion = nn.CrossEntropyLoss()
    total_loss = 0.0
    total_correct = 0
    total_samples = 0

    with torch.no_grad():
        for images, labels in tqdm(dataloader, desc="Running test predictions"):
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            loss = criterion(outputs, labels)
            total_loss += loss.item() * images.size(0)

            _, preds = torch.max(outputs, dim=1)
            total_correct += (preds == labels).sum().item()
            total_samples += labels.size(0)


    avg_loss = total_loss / total_samples
    accuracy = total_correct / total_samples

    return avg_loss, accuracy


def main():
    # Determine device to use
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Get the trained model from local files
    model = get_model()
    model.to(device)
    model.load_state_dict(torch.load("model_output/stego_classifier.pt", map_location=device))
    model.eval()

    # Define the transformatinons to apply to the images
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])

    print("[✓] Model loaded and ready for testing!")

    # Load the data
    test_dataset = StegoDataset("data/test", transform=transform)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

    # Run the evaluation
    loss, acc = evaluate(model, test_loader, device)

    # Print metrics
    print(f"Test Loss: {loss:.4f}")
    print(f"Test Accuracy: {acc * 100.0:.2f}%")


if __name__ == "__main__":
    main()
