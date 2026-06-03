# 
# convenience.bash                                                               
# 
# D. Clarke
# 
# A bunch of helper functions for the convenience methods.
# Based on my bashTools git. 
#


#
# COLORS. Example use: 
#   echo -e "  ${cred}ERROR encountered while running in this folder!${endc}"
#
endc="\e[0m"
cblk="\e[90m"
cred="\e[91m"
cgrn="\e[92m" 
cyel="\e[93m" 
cblu="\e[94m" 
cpur="\e[95m" 
ccyn="\e[96m" 
cwhi="\e[97m"


#
# UNDERLYING LOGGING COMMAND. Example use:
#   _bashLog "message!"
#
function _bashLog {
    # The @ sign indicates all arguments passed to this function.
    echo -e "[$(date)] $@"
}


#
# FAIL AND EXIT. Example use:
#   _bashFail "Division by zero!"
#
function _bashFail {
  _bashLog "${cred}FAIL: $@ ${endc}"
  exit
}


#
# LOGGING. Example use:
#   _bashWarn "Using this package is not recommended."
#
function _bashError {
  _bashLog "${cred}ERROR: $@ ${endc}"
} 
function _bashWarn {
  _bashLog "${cyel}WARNING: $@ ${endc}"
} 
function _bashPass {
  _bashLog "${cgrn}PASS: $@ ${endc}"
}
function _bashInfo {
  _bashLog "${ccyn}INFO: $@ ${endc}"
}


#
# CHECK FOR ERRORS OR FAILURES. Example use:
#   _checkForError $? "That was not supposed to happen..."
#
function _checkForError {
  if [ ! $1 -eq 0 ]; then _bashError "$2"; fi
}
function _checkForFail {
  if [ ! $1 -eq 0 ]; then _bashFail "$2"; fi
}


#
# PARAMETER HANDLING. Example use:
#   _checkIfEmpty ${paramName} ${param}
#
function _checkIfEmpty {
  paramName=$1
  param=$2
  if [ -z "${param}" ]; then
    _bashFail "Please set ${paramName}"
  fi
}


#
# CHECK EXTENSION. Example use:
#   _checkExtension CampaignExample.xml xml
# Returns 0 if the extension matches.
#
function _checkExtension {
  _checkIfParamEmpty "fileName" "${1}"
  _checkIfParamEmpty "extension" "${2}"
  case "$1" in *."$2") return 0;; esac
  return 1
}


#
# ARE YOU SURE YOU WANT TO DO THIS? Example use:
#   _confirmAction "Are you sure you want to do this?"
#
function _confirmAction {
  read -p "$1 (Y/y to proceed.) "
  if ! [[ "$REPLY" =~ [Yy]$ ]]; then
    exit
  fi
}


#
# DOES STRING START WITH SUBSTRING? Example use:
#   _startsWith helloWorld hello
#
function _startsWith {
  _checkIfParamEmpty "string" "${1}"
  _checkIfParamEmpty "substring" "${2}"
  if [[ "$1" == "$2"* ]]; then
      return 0 
  else
      return 1 
  fi
}

