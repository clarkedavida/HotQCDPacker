#!/bin/bash
# 
# get_ensXML.bash                                                               
# 
# D. Clarke
# 
# Download the XML file for the ensemble with markovChainURI MC. 
# 

source "$(dirname "$0")/../env.bash"
source convenience.bash

MC="$1"

_checkIfEmpty "MC" "${MC}"

ENS=$(basename "${MC}") 
ENSXML="${ENS}".xml
${ILDGMDC} -o ${ENSXML} -fmt -ge ${MC}
