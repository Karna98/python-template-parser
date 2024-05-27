"""
    template_parser.py

    @author : Vedant Wakalkar (@karna98)

    Core Logic for Template parsing

"""

from docxtpl import DocxTemplate

from constants import STR_DOC, ARGS_LIST
from utils import get_custom_logger, read_file, determine_file_type


def read_template(file_type: str, file: str) -> DocxTemplate:
    if file_type == STR_DOC:
        return DocxTemplate(file)

    raise RuntimeError("Error while reading template file '{}'".format(file))


def parse_template_with_data(input_data_file, input_template_file, output_file, custom_logger=None):
    # Initializing Logger
    logger = get_custom_logger() if custom_logger is None else custom_logger

    logger.debug("Reading Input Data File '{}'".format(input_data_file))
    context = read_file(determine_file_type(input_data_file, ARGS_LIST[0]), input_data_file, logger)

    logger.debug("Reading Input Template File '{}'".format(input_template_file))
    template_file = read_template(determine_file_type(input_template_file, ARGS_LIST[1]), input_template_file)

    # Check if output file with supported extension provided
    determine_file_type(output_file, ARGS_LIST[2])

    # Render Template file with Input Data File
    logger.debug("Rendering Input Template File {}' with '{}' ".format(input_template_file, input_data_file))
    template_file.render(context)

    # Save Rendered Template (with values) in provided output file
    logger.debug("Saving Rendered File '{}' ".format(output_file))
    template_file.save(output_file)
