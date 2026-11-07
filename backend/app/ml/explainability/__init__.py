"""
Explainable AI (XAI) and Grad-CAM visualization module for Agrivision AI+.
"""

from .gradcam import GradCAMExplainer, generate_gradcam

__all__ = [
    "GradCAMExplainer",
    "generate_gradcam",
]
