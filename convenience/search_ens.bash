#!/bin/bash
# 
# search_ens.bash                                                               
# 
# D. Clarke
# 
# Search the metadata catalogue for some ensembles with the
# passed properties. They should be passed as a single string, .e.
#   search.bash 'wilsonTmQuarkAction beta=4.05' 
# 

source "$(dirname "$0")/../env.bash"
source convenience.bash

searchQuery="$1"

_checkIfEmpty "searchQuery" "${searchQuery}"

${ILDGMDC} -qe "${searchQuery}"

