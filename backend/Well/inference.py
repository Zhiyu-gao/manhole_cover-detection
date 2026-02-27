"""Model loading and image inference helpers."""

from __future__ import annotations

import logging
import os
from pathlib import Path

import torch
from PIL import Image
from torchvision import models, transforms

LOGGER = logging.getLogger(__name__)

NUM_CLASSES = 5
_DEFAULT_MODEL_PATH = (
    Path(__file__).resolve().parents[2] / "models" / "finetune_resnet18.pth"
)
MODEL_PATH = Path(os.getenv("MODEL_PATH", _DEFAULT_MODEL_PATH))

_TRANSFORM = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
)
_MODEL: torch.nn.Module | None = None
_MODEL_LOAD_ERROR: Exception | None = None


class InferenceError(RuntimeError):
    """Raised when model inference cannot be completed."""


def _build_model() -> torch.nn.Module:
    model = models.resnet18(weights=None)
    model.fc = torch.nn.Linear(model.fc.in_features, NUM_CLASSES)
    model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
    model.eval()
    return model


def get_model() -> torch.nn.Module:
    """Lazy-load model once for the current process."""
    global _MODEL, _MODEL_LOAD_ERROR

    if _MODEL is not None:
        return _MODEL
    if _MODEL_LOAD_ERROR is not None:
        raise InferenceError("Model unavailable") from _MODEL_LOAD_ERROR

    try:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
        _MODEL = _build_model()
        LOGGER.info("Model loaded from %s", MODEL_PATH)
        return _MODEL
    except Exception as exc:  # pragma: no cover
        _MODEL_LOAD_ERROR = exc
        LOGGER.exception("Failed to load model from %s", MODEL_PATH)
        raise InferenceError("Model unavailable") from exc


def predict_image(image_path: Path) -> str:
    """Predict category string like [0] for a local image path."""
    try:
        img = Image.open(image_path).convert("RGB")
    except Exception as exc:
        raise InferenceError("Invalid image file") from exc

    model = get_model()
    input_tensor = _TRANSFORM(img).unsqueeze(0)
    with torch.no_grad():
        pred = model(input_tensor).argmax(dim=1).item()
    return f"[{pred}]"
