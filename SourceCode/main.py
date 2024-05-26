"""
    main.py

    @author : Vedant Wakalkar (@karna98)

    To parse input data file and populate in given Template document.

    Input File      : sample.{yaml/json}
    Input Template  : template.docx
    Output File     : output.docx

    Command : python main.py {Input_File} {Input_Template} {Output_File}
            # python SourceCode/main.py -df='example/sample.json' -tf='example/template.docx' -of='example/output.docx'
            # python SourceCode/main.py -df='example/sample.json' -tf='example/template.docx' -of='example/output.docx' -ll='DEBUG'
            # python SourceCode/main.py -h
"""

import argparse
import logging
import pathlib
from json import load as json_load, JSONDecodeError
from logging import config as logging_config, basicConfig, getLogger, _levelToName

from docxtpl import DocxTemplate
from yaml import load as yaml_load, Loader as yaml_Loader, YAMLError

# Constants
STR_YAML = 'YAML'
STR_JSON = 'JSON'
STR_DOC = 'DOC'

ARGS_LIST = ['DATA', 'TEMPLATE', 'OUTPUT']
EXT_YAML = ['.yaml', '.yml']
EXT_JSON = ['.json']
EXT_DOC = ['.docx']

LOG_STR_FORMAT = "%(asctime)s [%(name)s] [%(levelname)s] : %(message)s"

# Command Line Arguments Parser
argParser = argparse.ArgumentParser(description="Python Template Parser Configuration")

requiredArgsParser = argParser.add_argument_group("Required Args [ Mandatory ]")
requiredArgsParser.add_argument("-df", "--dataFile",
                                dest="input_data_file",
                                required=True,
                                help="Input Data File")
requiredArgsParser.add_argument("-tf", "--templateFile",
                                dest="input_template_file",
                                required=True,
                                help="Input Template File")
requiredArgsParser.add_argument("-of", "--outputFile",
                                dest="output_file",
                                required=True,
                                help="Rendered Output File")

loggingArgsParser = argParser.add_argument_group("Logging Args [ Optional ]")
loggingArgsParser.add_argument("-lcf", "--logConfigFile",
                               dest="loggerConfigFile",
                               help="Logger Configuration File")
loggingArgsParser.add_argument("-ll", "--logLevel",
                               dest="loggerLevel", help="Logger Level [ " + ', '.join(_levelToName.values()) + " ]")

cmdArgs = argParser.parse_args()

# Setting Logger Config from file
if cmdArgs.loggerConfigFile is not None:
    logging_config.fileConfig(cmdArgs.loggerConfigFile)
else:
    if cmdArgs.loggerLevel is not None:
        basicConfig(format=LOG_STR_FORMAT, level=cmdArgs.loggerLevel)
    else:
        basicConfig(format=LOG_STR_FORMAT, level=logging.ERROR)

# Initializing Logger
LOGGER = getLogger(__name__)


def determine_file_type(file_name: str, arg_type: str) -> str:
    _p_ = pathlib.Path(file_name).expanduser().resolve()

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


def read_file(file_type: str, file: str) -> dict:
    with open(file, "r", encoding='utf8') as stream:
        try:
            if file_type == STR_JSON:
                return json_load(stream)
            if file_type == STR_YAML:
                return yaml_load(stream.read(), Loader=yaml_Loader)

        except YAMLError as exc:
            LOGGER.error(exc)

        except JSONDecodeError as exc:
            LOGGER.error(exc)

    raise RuntimeError("Error while reading file '{}'".format(file))


def read_template(file_type: str, file: str) -> DocxTemplate:
    if file_type == STR_DOC:
        return DocxTemplate(file)

    raise RuntimeError("Error while reading template file '{}'".format(file))


def main() -> None:
    input_data_file = cmdArgs.input_data_file
    input_template_file = cmdArgs.input_template_file
    output_file = cmdArgs.output_file

    LOGGER.debug("Reading Input Data File '{}'".format(input_data_file))
    context = read_file(determine_file_type(input_data_file, ARGS_LIST[0]), input_data_file)

    LOGGER.debug("Reading Input Template File '{}'".format(input_template_file))
    template_file = read_template(determine_file_type(input_template_file, ARGS_LIST[1]), input_template_file)

    # Check if output file with supported extension provided
    determine_file_type(output_file, ARGS_LIST[2])

    # Render Template file with Input Data File
    LOGGER.debug("Rendering Input Template File {}' with '{}' ".format(input_template_file, input_data_file))
    template_file.render(context)

    # Save Rendered Template (with values) in provided output file
    LOGGER.debug("Saving Rendered File '{}' ".format(output_file))
    template_file.save(output_file)


if __name__ == '__main__':
    main()
