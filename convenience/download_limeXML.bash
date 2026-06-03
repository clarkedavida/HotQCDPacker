#!/bin/bash
# 
# download_limeXML.bash                                                               
# 
# D. Clarke
# 
# Download lime XML for lime file with LFN. 
# 

source "$(dirname "$0")/../env.bash"
source convenience.bash

LFN="$1"
_checkIfEmpty "LFN" "${LFN}"

LIME=$(basename "${LFN}")
LIMEXML="${LIME%.lime}".xml
${ILDGMDC} -o "${LIMEXML}" -fmt -gc "${LFN}"
