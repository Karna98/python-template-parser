"""
    main.py

    @author : Vedant Wakalkar (@karna98)

    Command Line Utility
    To parse input data file and populate in given Template document.

    Input File      : sample.{yaml/json}
    Input Template  : template.docx
    Output File     : output.docx

    Command : python main.py {Input_File} {Input_Template} {Output_File}
            # python src/template-parser/main.py -df='example/sample.json' -tf='example/template.docx' -of='example/output.docx'
            # python src/template-parser/main.py -df='example/sample.json' -tf='example/template.docx' -of='example/output.docx' -ll='DEBUG'
            # python src/template-parser/main.py -h
"""

import argparse

from template_parser import parse_template_with_data
from utils import get_custom_logger, get_logging_levels


def init_cmd_argument_parser():
    # Command Line Arguments Parser
    arg_parser = argparse.ArgumentParser(description="Python Template Parser Configuration")

    required_args_parser = arg_parser.add_argument_group("Required Args [ Mandatory ]")
    required_args_parser.add_argument("-df", "--dataFile",
                                      dest="input_data_file",
                                      required=True,
                                      help="Input Data File")
    required_args_parser.add_argument("-tf", "--templateFile",
                                      dest="input_template_file",
                                      required=True,
                                      help="Input Template File")
    required_args_parser.add_argument("-of", "--outputFile",
                                      dest="output_file",
                                      required=True,
                                      help="Rendered Output File")

    logging_args_parser = arg_parser.add_argument_group("Logging Args [ Optional ]")
    logging_args_parser.add_argument("-lcf", "--logConfigFile",
                                     dest="loggerConfigFile",
                                     help="Logger Configuration File")
    logging_args_parser.add_argument("-ll", "--logLevel",
                                     dest="loggerLevel",
                                     help="Logger Level [ " + ', '.join(get_logging_levels()) + " ]")

    return arg_parser.parse_args()


def main() -> None:
    input_data_file = cmdArgs.input_data_file
    input_template_file = cmdArgs.input_template_file
    output_file = cmdArgs.output_file

    parse_template_with_data(input_data_file, input_template_file, output_file, LOGGER)


if __name__ == '__main__':
    cmdArgs = init_cmd_argument_parser()

    # Initializing Logger
    LOGGER = get_custom_logger(cmdArgs.loggerConfigFile, cmdArgs.loggerLevel)

    main()
