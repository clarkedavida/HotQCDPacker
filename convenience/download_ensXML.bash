#!/bin/bash
# 
# download_ensXML.bash                                                               
# 
# D. Clarke
# 
# Download the XML file for the ensemble with markovChainURI MC. 
# 

source "${HOTQCDPACKER_DIR}/env.bash"
source "${HOTQCDPACKER_DIR}/convenience/convenience.bash"

MC="$1"

_checkIfEmpty "MC" "${MC}"

ENS=$(basename "${MC}") 
ENSXML="${ENS}".xml
${ILDGMDC} -o ${ENSXML} -fmt -ge ${MC}
