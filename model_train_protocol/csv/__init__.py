"""
Model Train Protocol (MTP) - A Python package for creating custom Language Model training protocols.

MTP is an open-source protocol for training custom Language Models on Databiomes.
MTP contains all the data that a model is trained on.
"""
from .conversion import CSVConversion

__all__ = [
    "CSVConversion"
]
