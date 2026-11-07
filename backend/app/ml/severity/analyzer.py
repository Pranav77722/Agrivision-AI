"""
Severity Analyzer Adapter for Agrivision AI+.

Delegates to SeverityEstimator (U-Net) and provides output schemas for
FastAPI routes and diagnosis pipeline.
"""

from __future__ import annotations

import io
import logging
from typing import Any, Dict

import cv2
import numpy as np
from PIL import Image

try:
    from backend.app.ml.severity.estimator import SeverityEstimator
    from backend.app.ml.preprocessing import load_image
except ImportError:
    from app.ml.severity.estimator import SeverityEstimator
    from app.ml.preprocessing import load_image

logger = logging.getLogger(__name__)


class SeverityAnalyzer:
    """
    Adapter bridging SeverityEstimator with the FastAPI diagnosis pipeline.
    """

    def __init__(self) -> None:
        self.estimator = SeverityEstimator(auto_load=True)

    def analyze(self, image: Any) -> Dict[str, Any]:
        """
        Analyze leaf infection severity, returning mask_bytes, percentage, and level.
        """
        res = self.estimator.segment(image)

        # Fallback mask if model is unavailable
        if res.get("status") == "model_unavailable" or "overlay_image" not in res:
            img_rgb = load_image(image, to_rgb=True)
            h, w = img_rgb.shape[:2]

            # Color-based fallback mask
            r = img_rgb[:, :, 0].astype(float)
            g = img_rgb[:, :, 1].astype(float)
            b = img_rgb[:, :, 2].astype(float)

            leaf_pixels = (g > 30) & (r < 240) & (b < 240)
            necrotic = leaf_pixels & ((r > g + 10) | ((g > 80) & (r > 80) & (b < 60)) | (g < 60))

            mask_arr = np.zeros_like(img_rgb, dtype=np.uint8)
            mask_arr[leaf_pixels] = [34, 197, 94]  # Green healthy
            mask_arr[necrotic] = [239, 68, 68]     # Red diseased

            mask_img = Image.fromarray(mask_arr)
            buf = io.BytesIO()
            mask_img.save(buf, format="JPEG", quality=85)
            mask_bytes = buf.getvalue()

            total_leaf = max(1, int(np.sum(leaf_pixels)))
            lesion_count = int(np.sum(necrotic))
            pct = round((lesion_count / total_leaf) * 100.0, 1)

            if pct < 5.0:
                level = "Healthy"
            elif pct < 20.0:
                level = "Mild"
            elif pct < 40.0:
                level = "Moderate"
            elif pct < 60.0:
                level = "Severe"
            else:
                level = "Critical"

            return {
                "severity_level": level,
                "severity_percentage": pct,
                "description": f"Severity estimated at {pct}% ({level}). Model weights missing, using agronomic colorimeter.",
                "mask_bytes": mask_bytes,
                "model_available": False,
            }

        # Model is available
        # Decode overlay image to bytes
        import base64

        b64_str = res["overlay_image"].split(",")[1] if "," in res["overlay_image"] else res["overlay_image"]
        mask_bytes = base64.b64decode(b64_str)

        return {
            "severity_level": res.get("severity_category", "Moderate"),
            "severity_percentage": res.get("severity_percentage", 0.0),
            "description": f"U-Net semantic segmentation detected {res.get('severity_percentage', 0.0)}% leaf lesion coverage ({res.get('severity_category', 'Moderate')}).",
            "mask_bytes": mask_bytes,
            "healthy_area_pixels": res.get("healthy_area_pixels", 0),
            "diseased_area_pixels": res.get("diseased_area_pixels", 0),
            "model_available": True,
        }
