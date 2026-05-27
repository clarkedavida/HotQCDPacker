#!/bin/bash

source "$(dirname "$0")/../env.bash"

MC=mc://ldg/hotqcd/f21_highTspf/l6420f21b7570m003946m01973
ENS=$(basename "${MC}") 
ENSXML="${ENS}".xml
${ILDGMDC} -o ${ENSXML} -fmt -ge ${MC}
