"""
Agrivision AI+ - Image Preprocessing and Validation Pipeline.

Provides production-grade image loading, validation, quality checks (blur/brightness),
resizing, color conversions, and model-specific normalization.
"""

from __future__ import annotations

import base64
import io
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import cv2
import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)

# Supported formats and size boundaries
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
MIN_IMAGE_DIMENSION = 64
MAX_IMAGE_DIMENSION = 8192
MAX_IMAGE_FILE_SIZE_BYTES = 20 * 1024 * 1024  # 20 MB
BLUR_THRESHOLD_DEFAULT = 100.0  # Laplacian variance threshold


class ImageValidationError(ValueError):
    """Raised when an input image fails structural or quality validation."""
    pass


def load_image(
    image_input: Union[str, Path, bytes, io.BytesIO, Image.Image, np.ndarray],
    to_rgb: bool = True,
) -> np.ndarray:
    """
    Load an image from varied input sources into a numpy uint8 RGB or BGR array.

    Args:
        image_input: File path (str/Path), raw bytes, BytesIO stream, PIL Image, or ndarray.
        to_rgb: If True, guarantees returning RGB format. If False, keeps BGR (OpenCV standard).

    Returns:
        np.ndarray: Image array in uint8 with shape (H, W, 3).
    """
    if isinstance(image_input, np.ndarray):
        img = image_input.copy()
        if img.dtype != np.uint8:
            if img.max() <= 1.0:
                img = (img * 255.0).clip(0, 255).astype(np.uint8)
            else:
                img = img.clip(0, 255).astype(np.uint8)
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB if to_rgb else cv2.COLOR_GRAY2BGR)
        elif len(img.shape) == 3 and img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB if to_rgb else cv2.COLOR_BGRA2BGR)
        return img

    if isinstance(image_input, Image.Image):
        rgb_image = image_input.convert("RGB")
        arr = np.array(rgb_image, dtype=np.uint8)
        return arr if to_rgb else cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)

    if isinstance(image_input, (str, Path)):
        path = Path(image_input)
        if not path.is_file():
            raise FileNotFoundError(f"Image file does not exist: {path}")
        if path.suffix.lower() not in ALLOWED_IMAGE_EXTENSIONS:
            raise ImageValidationError(
                f"Unsupported image extension '{path.suffix}'. Allowed: {ALLOWED_IMAGE_EXTENSIONS}"
            )
        file_size = path.stat().st_size
        if file_size > MAX_IMAGE_FILE_SIZE_BYTES:
            raise ImageValidationError(
                f"Image file size {file_size / (1024 * 1024):.2f}MB exceeds limit of 20MB."
            )
        bgr = cv2.imread(str(path), cv2.IMREAD_COLOR)
        if bgr is None:
            raise ImageValidationError(f"OpenCV failed to decode image at {path}.")
        return cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB) if to_rgb else bgr

    if isinstance(image_input, io.BytesIO):
        image_bytes = image_input.getvalue()
    elif isinstance(image_input, bytes):
        image_bytes = image_input
    else:
        raise TypeError(f"Unsupported image input type: {type(image_input)}")

    if len(image_bytes) == 0:
        raise ImageValidationError("Received empty image byte payload.")

    if len(image_bytes) > MAX_IMAGE_FILE_SIZE_BYTES:
        raise ImageValidationError(
            f"Image payload size ({len(image_bytes) / 1024 / 1024:.2f}MB) exceeds 20MB maximum."
        )

    # Check for base64 data URI header e.g. "data:image/jpeg;base64,..."
    if image_bytes.startswith(b"data:image"):
        try:
            comma_idx = image_bytes.find(b",")
            if comma_idx != -1:
                image_bytes = base64.b64decode(image_bytes[comma_idx + 1:])
        except Exception as e:
            logger.warning("Failed to decode presumed base64 prefix: %s", e)

    nparr = np.frombuffer(image_bytes, np.uint8)
    bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if bgr is None:
        # Fallback to PIL
        try:
            pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            arr = np.array(pil_img, dtype=np.uint8)
            return arr if to_rgb else cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
        except Exception as exc:
            raise ImageValidationError(f"Could not decode image from bytes: {exc}") from exc

    return cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB) if to_rgb else bgr


def validate_image_dimensions(
    img: np.ndarray,
    min_dim: int = MIN_IMAGE_DIMENSION,
    max_dim: int = MAX_IMAGE_DIMENSION,
) -> Tuple[int, int]:
    """
    Validate that image dimensions fall within permissible bounds.

    Returns:
        (height, width)
    """
    if not isinstance(img, np.ndarray) or len(img.shape) < 2:
        raise ImageValidationError("Invalid image array format.")
    h, w = img.shape[:2]
    if h < min_dim or w < min_dim:
        raise ImageValidationError(
            f"Image resolution {w}x{h} is too small. Minimum dimension is {min_dim}px."
        )
    if h > max_dim or w > max_dim:
        raise ImageValidationError(
            f"Image resolution {w}x{h} exceeds maximum allowed {max_dim}px."
        )
    return h, w


def assess_image_quality(
    img_rgb: np.ndarray,
    blur_threshold: float = BLUR_THRESHOLD_DEFAULT,
) -> Dict[str, Any]:
    """
    Evaluate technical image quality: sharpness/blur score (Laplacian variance),
    average brightness, contrast, and resolution sanity.

    Args:
        img_rgb: RGB uint8 numpy image.
        blur_threshold: Variance of Laplacian below which an image is flagged as blurry.

    Returns:
        Dict containing quality metrics and boolean flags.
    """
    h, w = img_rgb.shape[:2]
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

    # Laplacian variance as sharpness proxy
    laplacian_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    is_blurry = laplacian_var < blur_threshold

    mean_brightness = float(np.mean(gray))
    std_contrast = float(np.std(gray))

    is_too_dark = mean_brightness < 30.0
    is_overexposed = mean_brightness > 230.0
    is_low_contrast = std_contrast < 15.0

    is_acceptable = not (is_too_dark or is_overexposed) and (laplacian_var >= (blur_threshold * 0.3))

    reasons: List[str] = []
    if is_blurry:
        reasons.append(f"Image may be blurry (sharpness score {laplacian_var:.1f} < {blur_threshold})")
    if is_too_dark:
        reasons.append("Image is under-exposed (too dark)")
    if is_overexposed:
        reasons.append("Image is over-exposed (washed out)")
    if is_low_contrast:
        reasons.append("Image has low contrast")

    return {
        "is_acceptable": is_acceptable,
        "is_blurry": is_blurry,
        "laplacian_variance": round(laplacian_var, 2),
        "mean_brightness": round(mean_brightness, 2),
        "contrast_std": round(std_contrast, 2),
        "dimensions": {"width": w, "height": h},
        "quality_warnings": reasons,
    }


def resize_and_pad(
    img_rgb: np.ndarray,
    target_size: Tuple[int, int],
    interpolation: int = cv2.INTER_AREA,
    pad_color: Tuple[int, int, int] = (0, 0, 0),
) -> np.ndarray:
    """
    Resize image to target_size (width, height) preserving aspect ratio by letterboxing/padding.
    """
    target_w, target_h = target_size
    h, w = img_rgb.shape[:2]

    scale = min(target_w / w, target_h / h)
    new_w, new_h = int(round(w * scale)), int(round(h * scale))

    interp = cv2.INTER_CUBIC if scale > 1.0 else interpolation
    resized = cv2.resize(img_rgb, (new_w, new_h), interpolation=interp)

    canvas = np.full((target_h, target_w, 3), pad_color, dtype=np.uint8)
    x_offset = (target_w - new_w) // 2
    y_offset = (target_h - new_h) // 2
    canvas[y_offset : y_offset + new_h, x_offset : x_offset + new_w] = resized
    return canvas


def preprocess_for_model(
    img_rgb: np.ndarray,
    model_name: str,
    target_size: Optional[Tuple[int, int]] = None,
    keep_aspect_ratio: bool = False,
) -> np.ndarray:
    """
    Apply model-specific resizing and tensor normalization for inference.

    Args:
        img_rgb: RGB image array with values in [0, 255].
        model_name: Name of model ('efficientnetb3', 'vgg16', 'vgg19',
                    'inceptionv3', 'resnet101v2', 'unet', 'yolo').
        target_size: (height, width) or (width, height) override.
        keep_aspect_ratio: If True, uses letterboxing.

    Returns:
        np.ndarray: Batch tensor ready for model inference (1, H, W, 3) in float32.
    """
    model_key = model_name.lower().replace("-", "").replace("_", "")

    # Default sizes (H, W)
    default_sizes = {
        "efficientnetb3": (300, 300),
        "vgg16": (224, 224),
        "vgg19": (224, 224),
        "inceptionv3": (299, 299),
        "resnet101v2": (224, 224),
        "unet": (256, 256),
        "yolo": (640, 640),
    }

    hw_size = target_size if target_size else default_sizes.get(model_key, (224, 224))
    h, w = hw_size[0], hw_size[1]

    if keep_aspect_ratio:
        resized = resize_and_pad(img_rgb, (w, h))
    else:
        resized = cv2.resize(img_rgb, (w, h), interpolation=cv2.INTER_AREA)

    arr = resized.astype(np.float32)

    if "efficientnet" in model_key:
        # Keras EfficientNet expects RGB with values in [0, 255] (built-in Rescaling layer)
        # or tf.keras.applications.efficientnet.preprocess_input which is identity for v1/v2
        processed = arr
    elif "vgg" in model_key:
        # VGG expects BGR, zero-centered with ImageNet means [103.939, 116.779, 123.68]
        bgr = cv2.cvtColor(resized, cv2.COLOR_RGB2BGR).astype(np.float32)
        bgr[..., 0] -= 103.939
        bgr[..., 1] -= 116.779
        bgr[..., 2] -= 123.68
        processed = bgr
    elif "inception" in model_key:
        # InceptionV3 expects values normalized in [-1, +1]
        processed = (arr / 127.5) - 1.0
    elif "resnet" in model_key:
        # ResNetV2 expects values normalized in [-1, +1]
        processed = (arr / 127.5) - 1.0
    elif "unet" in model_key:
        # U-Net leaf segmentation: normalized in [0, 1]
        processed = arr / 255.0
    elif "yolo" in model_key:
        # YOLO typically takes [0, 1] or raw image
        processed = arr / 255.0
    else:
        # Generic [0, 1] normalization
        processed = arr / 255.0

    # Expand batch dimension (1, H, W, 3)
    return np.expand_dims(processed, axis=0)


def encode_image_base64(img: np.ndarray, format_ext: str = ".jpg") -> str:
    """Encode an image array (RGB or BGR) to base64 string with data URI prefix."""
    if len(img.shape) == 3 and img.shape[2] == 3:
        bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    else:
        bgr = img
    success, buffer = cv2.imencode(format_ext, bgr)
    if not success:
        raise RuntimeError("Failed to encode image to buffer.")
    b64_str = base64.b64encode(buffer).decode("utf-8")
    mime = "image/jpeg" if format_ext.lower() in [".jpg", ".jpeg"] else "image/png"
    return f"data:{mime};base64,{b64_str}"
