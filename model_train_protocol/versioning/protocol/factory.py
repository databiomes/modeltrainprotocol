from packaging.version import Version

from model_train_protocol.versioning.protocol.versions.base import BaseProtocol
from model_train_protocol.versioning.protocol.versions.v1.protocol import Protocol as ProtocolV1


class ProtocolFactory:
    """Factory for creating protocol instances."""

    def __init__(self, version: Version):
        self.version = version

    def get_protocol(self) -> BaseProtocol:
        """"
        Get the appropriate protocol instance based on the version.""
        """
        if self.version < Version("2.0.0"):
            return ProtocolV1(version=self.version)
        else:
            raise NotImplementedError(f"Protocol version {self.version} is not supported.")