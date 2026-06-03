#!/bin/bash
# 
# get_SURL_from_LFN.bash                                                               
# 
# D. Clarke
# 
# Get the SURL of conf with supplied LFN 
#

source "$(dirname "$0")/../env.bash"
source convenience.bash

LFN="$1"

_checkIfEmpty "LFN" "${LFN}"

${ILDGFC} -ll "${LFN}"
