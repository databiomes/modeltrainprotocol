from model_train_protocol.schema_version import SCHEMA_VERSION
from model_train_protocol.template_version import TEMPLATE_VERSION


def get_schema_version() -> str:
    """
    Gets the schema version bundled with the package.
    """
    return SCHEMA_VERSION


def get_template_version() -> str:
    """
    Gets the template version bundled with the package.
    """
    return TEMPLATE_VERSION


def get_bloom_schema_url():
    """
    Retrieves the schema URL for the current version of the Model Train Protocol.
    """
    version_semantic: str = get_schema_version()
    schema_url = f"https://mtp.schemas.databiomes.com/v{version_semantic[0]}/bloom_{version_semantic.replace('.', '_')}.json"
    return schema_url


def get_template_schema_url():
    """
    Retrieves the schema URL for the current version of the MTP Template.
    """
    version_semantic: str = get_template_version()
    schema_url = f"https://mtp.schemas.databiomes.com/v{version_semantic[0]}/template_{version_semantic.replace('.', '_')}.json"
    return schema_url
