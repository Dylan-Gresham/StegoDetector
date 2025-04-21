import torch.nn as nn
import torchvision.models as models


def get_model() -> models.ResNet:
    """
    Helper method to get an untrained ResNet18 model.

    # Parameters:

    `None`

    # Returns:

    A `ResNet` instance in which the weights are not pre-trained.
    """
    model = models.resnet18(weights=None)
    # TODO: Add a layer here!

    return model
