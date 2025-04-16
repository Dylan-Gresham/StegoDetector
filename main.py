import os

import stegodetector.evaluate as sde
import stegodetector.train as sdt


def main():
    """Trains and then evaluates a ResNet18 model for steganography detection."""
    if not os.path.exists("model_output/stego_classifier.pt"):
        sdt.main()

    sde.main()

if __name__ == "__main__":
    main()
