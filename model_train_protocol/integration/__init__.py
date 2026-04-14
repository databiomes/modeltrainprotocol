"""
Model Train Protocol (MTP) - A Python package for creating custom Language Model training protocols.

MTP is an open-source protocol for training custom Language Models on Databiomes.
MTP contains all the data that a model is trained on.
"""
from model_train_protocol.versioning.files.protocol_file.v1.ProtocolFile import ProtocolFile
from model_train_protocol.versioning.files.template_file.v1.TemplateFile import TemplateFile

__all__ = [
    "ProtocolFile",
    "TemplateFile"
]
