"""
Disease classification package for Agrivision AI+.
"""

from .classifier import DiseaseClassifier, PLANT_VILLAGE_CLASSES
from .ensemble import EnsembleClassifier

__all__ = [
    "DiseaseClassifier",
    "EnsembleClassifier",
    "PLANT_VILLAGE_CLASSES",
]
