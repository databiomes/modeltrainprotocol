"""
Model Train Protocol (MTP) - A Python package for creating custom Language Model training protocols.

MTP is an open-source protocol for training custom Language Models on Databiomes.
MTP contains all the data that a model is trained on.
"""
from .public import get_bloom_schema_url, get_template_schema_url, get_schema_version

__all__ = [
    "get_bloom_schema_url",
    "get_template_schema_url",
    "get_schema_version"
]
