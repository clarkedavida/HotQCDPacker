#!/bin/bash
# 
# delete_lime.bash                                                               
# 
# D. Clarke
# 
# Delete a LIME file from the MDC, FC, and SE. If you have the
# LFN, you can get the SURL from get_SURL_from_LFN.bash. You'll
# need the token from get_token.bash. Call like
#   delete_lime LFN SURL
# 

source "${HOTQCDPACKER_DIR}/env.bash"
source "${HOTQCDPACKER_DIR}/convenience/convenience.bash"

LFN="$1"
SURL="$2"

_checkIfEmpty "LFN" "${LFN}"
_checkIfEmpty "SURL" "${SURL}"

_bashInfo
_bashInfo "Delete from MDC"
${ILDGMDC} -dc "${LFN}"

_bashInfo
_bashInfo "Delete from FC"
${ILDGFC} -d "${LFN}" "${SURL}"

_bashInfo
_bashInfo "Delete from SE"
${ILDGSE} -delete "${SURL}"

_bashInfo
_bashInfo "Done."
