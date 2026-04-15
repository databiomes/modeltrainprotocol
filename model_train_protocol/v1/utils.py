from packaging.version import Version

from model_train_protocol.v1.protocol_file.protocol_version import PROTOCOL_VERSION
from model_train_protocol.v1.template_file.template_version import TEMPLATE_VERSION


def get_default_protocol_version() -> Version:
    """Get the default protocol version."""
    return Version(PROTOCOL_VERSION)


def get_default_template_version() -> Version:
    """Get the default template version"""
    return Version(TEMPLATE_VERSION)
