#!/bin/bash

# @Author : Vedant Wakalkar (@karna98)
# @Version :  1.0.0
# @Description : Setup script for python-template-parser

# Supported OS List
OS_LIST=("Linux" "Mac" "Cygwin" "Windows")

# Project Directory Name
PTP_DIR="python-template-parser"

# Full path to parent directory of setup.sh (executed)
SETUP_SH_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Virtual Environment Name
VENV_NAME="ptp_venv"

# Virtual Environment Path
VENV_PATH=$SETUP_SH_DIR/$VENV_NAME


# Flag to track if not present in required directory
MISMATCH_DIR=0
VAR_DIRECTORY_CHANGE="DIRECTORY_CHANGE"

if [ "$1" = $VAR_DIRECTORY_CHANGE ];
then
  MISMATCH_DIR=1
fi

# Detect OS
unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     OS=${OS_LIST[0]};;
    Darwin*)    OS=${OS_LIST[1]};;
    CYGWIN*)    OS=${OS_LIST[2]};;
    MINGW*)     OS=${OS_LIST[3]};;
    *)          OS="UNKNOWN:${unameOut}"
esac

# Check if setup.sh is not executed inside 'python-template-parser' directory
if [ "${PWD##*/}" != $PTP_DIR ];
then
    printf -- "\nERROR : Working in wrong directory (%s).\n" "${PWD##*/}"
    printf -- "\nWait I will make it right for you.\nAnyway what am I for :-)\n"

    if [ -f "$SETUP_SH_DIR/setup.sh" ]
    then
        # shellcheck disable=SC2164
        cd "$SETUP_SH_DIR" || exit 1
        chmod +x setup.sh
        ./setup.sh "$VAR_DIRECTORY_CHANGE"
    fi
    exit 0
fi

# Display Message
stage_start() {
    printf -- "\n*------------------------------*"
    printf -- "\n*------  Stage-%s Setup  -------*" "$1"
    printf -- "\n*------------------------------*\n"
}

stage_finished() {
    printf -- "\n*------------------------------*"
    printf -- "\n*--- Stage-%s Setup Finished ---*" "$1"
    printf -- "\n*------------------------------*\n"
}

stage_aborted() {
    printf -- "\n*------------------------------*"
    printf -- "\n*------ Stage-%s Aborted -------*" "$1"
    printf -- "\n*------------------------------*\n"
    exit 1
}

# Display activate virtual environment message
activate_venv_msg() {
    if [ "$1" != 0 ]
    then
        printf -- "\nERROR: Activate virtual environment '%s' and run setup.sh for 'Stage-$1' again.\n" "$VENV_NAME"
    fi

    printf -- "\n-- Activate virtual environment by running following command :"

    if [ "$OS" = "${OS_LIST[0]}" ];
    then
        ACTIVATE_PATH="/bin/activate"
    elif [ "$OS" = "${OS_LIST[3]}" ];
    then
        ACTIVATE_PATH="/Scripts/activate"
    fi

    if [ "$OS" = "${OS_LIST[1]}" ];
    then
        printf -- "\n\n   > . %s" "$VENV_PATH$ACTIVATE_PATH"
    else
        printf -- "\n\n   > source %s" "$VENV_PATH$ACTIVATE_PATH"

        if [ $MISMATCH_DIR = 0 ];
        then
          printf -- "\n\n                OR                     "
          printf -- "\n\n   > source %s" "$VENV_NAME$ACTIVATE_PATH"
        fi
    fi
}

# Stage-1 Setup
stage_1(){

    # 1.1 Detect Virtual Environment
    printf -- "\n1. Detecting 'virtualenv'\n"
    if ! [ -x "$(command -v virtualenv)" ];
    then
        printf -- "\n-- No 'virtualenv' command found."
        printf -- "\n-- Installing 'virtualenv' ...\n"
        if [ "$OS" = "${OS_LIST[0]}" ];
        then
            sudo apt-get install python3-pip
        elif [ "$OS" = "${OS_LIST[3]}" ];
        then
            py -3 -m ensurepip
            python -m pip install --upgrade pip
        fi

        pip3 install virtualenv
        printf -- "\n-- Successfully installed 'virtualenv'."
    fi

    printf -- "\n-- 'virtualenv' detected!!"
    printf -- "\n-- 'virtualenv' version %s" "$(virtualenv --version | perl -pe '($_)=/([0-9]+([.][0-9]+)+)/')"

    # 1.2 Create Virtual Environment
    printf -- "\n\n2. Creating Virtual Environment"
    printf -- "\n\n-- virtualenv name : %s " $VENV_NAME
    printf -- "\n-- virtualenv path : %s \n" "$VENV_PATH"

    if [ -d "$VENV_PATH" ];
    then
        printf -- "\n-- Environment (%s) exists !!\n" "$VENV_NAME"
        read -rp "   Do you want to setup virtual environment by removing existing one ? [y|N] " yesNo

        if [[  $yesNo =~ ^(y|Y)$ ]]
        then
            printf --  "\n"
            if [ "$OS" = "${OS_LIST[0]}" ];
            then
                sudo rm -r "$VENV_PATH"
            else
                rm -r "$VENV_PATH"
            fi
        fi
    fi

    if [ ! -d "$VENV_PATH" ];
    then
        virtualenv "$VENV_PATH" --python=python3
        printf -- "\n-- Virtual Environment (%s) created successfully !!" "$VENV_NAME"
    fi

    activate_venv_msg 0

    printf -- "\n\nAfter activating Virtual Environment, run setup.sh for Stage-2 Setup.\n"
}

# Stage-2 Setup
stage_2() {

    # 2.1 Detect Virtual Environment
    printf -- "\n1. Detecting (%s) virtual environment\n" "$VENV_NAME"

    if [ "$VIRTUAL_ENV" = "$VENV_PATH" ];
    then
        printf -- "\n-- Detected Virtual Environment : %s \n" "$VENV_NAME"
    else
        activate_venv_msg 2
        stage_aborted 2
    fi

    # 2.2 Install Dependencies
    printf -- "\n2. Installing required dependencies \n"
    pip3 install -r requirements.txt
    printf -- "\nSuccessfully installed required dependencies\n"
}

# Packing start message, function call and finished message for each stage
stage_pack() {
    stage_start "$1"
    stage_"$1"
    stage_finished "$1"

    exit 0
}

# Display Header message
printf -- "\n*------ %s Project Setup ------*\n" "$PTP_DIR"
printf -- "\n*-------------------------------------------------*"
printf -- "\n*---  Select option to get started with setup  ---*"
printf -- "\n*-------------------------------------------------*\n"

# Prompt user to select option
# 1. Stage 1 Setup
# 2. Stage 2 Setup (run inside virtualenv)
PS3="Option : "
options=("Stage 1 Setup" "Stage 2 Setup (run inside virtualenv)" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "Stage 1"*)
            stage_pack 1
            ;;
        "Stage 2"*)
            stage_pack 2
            ;;
        "Quit")
            printf -- "\nExiting Project Setup !!\n"
            break
            ;;
        *) printf -- "\nInvalid option %s\n" "$REPLY";;
    esac
done
