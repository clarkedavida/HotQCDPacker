#!/bin/bash
# 
# search_ens.bash                                                               
# 
# D. Clarke
# 
# Search the metadata catalogue for some ensembles with the
# passed properties. They should be passed as a single string.
# Searches seem to be based on ensemble QCDml tags.
#
# Examples: 
#   search.bash 'wilsonTmQuarkAction beta=4.05' 
#   search.bash 'collaboration="hotqcd"' 
#   search.bash 'projectName="f21_highTspf"' 
# 

source "${HOTQCDPACKER_DIR}/env.bash"
source "${HOTQCDPACKER_DIR}/convenience/convenience.bash"

searchQuery="$1"

_checkIfEmpty "searchQuery" "${searchQuery}"

${ILDGMDC} -qe "${searchQuery}"

