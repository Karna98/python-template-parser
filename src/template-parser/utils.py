"""
    utils.py

    @author : Vedant Wakalkar (@karna98)

    Utility Functions

"""

from json import load as json_load, JSONDecodeError
from logging import Logger
from logging import config as logging_config, basicConfig, getLogger, _levelToName, ERROR
from pathlib import Path

from yaml import load as yaml_load, Loader as yaml_Loader, YAMLError

from constants import *


def read_file(file_type: str, file: str, custom_logger: Logger = None) -> dict:
    with open(file, "r", encoding='utf8') as stream:
        try:
            if file_type == STR_JSON:
                return json_load(stream)
            if file_type == STR_YAML:
                return yaml_load(stream.read(), Loader=yaml_Loader)

        except YAMLError as exc:
            custom_logger.error(exc) if custom_logger is not None else print(exc)

        except JSONDecodeError as exc:
            custom_logger.error(exc) if custom_logger is not None else print(exc)

    raise RuntimeError("Error while reading file '{}'".format(file))


def determine_file_type(file_name: str, arg_type: str) -> str:
    _p_ = Path(file_name).expanduser().resolve()

    if _p_.suffix in EXT_YAML:
        return STR_YAML
    if _p_.suffix in EXT_JSON:
        return STR_JSON
    if _p_.suffix in EXT_DOC:
        return STR_DOC

    raise TypeError(
        "Unsupported file '{}' provided as input. Supported file formats are ['{}']"
        .format(_p_.name, '\', \''.join(EXT_YAML + EXT_JSON if (arg_type == ARGS_LIST[0]) else EXT_DOC))
    )


def get_custom_logger(config_file=None, log_level=None):
    # Setting Logger Config from file
    if config_file is not None:
        logging_config.fileConfig(config_file)
    else:
        if log_level is not None:
            basicConfig(format=LOG_STR_FORMAT, level=log_level)
        else:
            basicConfig(format=LOG_STR_FORMAT, level=ERROR)

    # Initializing Logger
    return getLogger(__name__)


def get_logging_levels():
    return _levelToName.values()
