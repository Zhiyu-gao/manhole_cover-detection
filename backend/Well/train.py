"""Reference training script for fine-tuning ResNet18 on manhole data."""

from __future__ import annotations

from pathlib import Path

import torch
import torch.nn as nn
from PIL import Image
from torchvision import models, transforms

TRANSFORM = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
)


def load_img(path: Path) -> torch.Tensor:
    return TRANSFORM(Image.open(path).convert("RGB"))


def train_classifier(
    train_image_paths: list[Path],
    train_labels: list[int],
    output_path: Path,
    num_classes: int,
    epochs: int = 20,
) -> None:
    if len(train_image_paths) != len(train_labels):
        raise ValueError("train_image_paths and train_labels must have the same length")
    if not train_image_paths:
        raise ValueError("training set is empty")

    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    model.fc = nn.Linear(model.fc.in_features, num_classes)

    for param in model.parameters():
        param.requires_grad = False
    for param in model.fc.parameters():
        param.requires_grad = True

    inputs = torch.stack([load_img(path) for path in train_image_paths])
    labels = torch.tensor(train_labels)

    optimizer = torch.optim.Adam(model.fc.parameters(), lr=0.01)
    criterion = nn.CrossEntropyLoss()

    model.train()
    for epoch in range(epochs):
        outputs = model(inputs)
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(f"Epoch {epoch + 1}/{epochs}, Loss: {loss.item():.4f}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), output_path)


if __name__ == "__main__":
    raise SystemExit(
        "Use train_classifier() from another script and provide real dataset paths/labels."
    )
