"""
Model Train Protocol (MTP) - A Python package for creating custom Language Model training protocols.

MTP is an open-source protocol for training custom Language Models on Databiomes.
MTP contains all the data that a model is trained on.
"""
from model_train_protocol.versioning.files.protocol_file.v1.protocol_file import ProtocolFileV1
from model_train_protocol.versioning.files.template_file.v1.template_file import TemplateFileV1

__all__ = [
    "ProtocolFileV1",
    "TemplateFileV1"
]
