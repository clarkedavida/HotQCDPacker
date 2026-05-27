#!/bin/bash

source "$(dirname "$0")/../env.bash"

LFN=lfn://ldg/hotqcd/f21_highTspf/l6420f21b7570m003946m01973/1_10010to10140.lime

LIME=$(basename "${LFN}")
LIMEXML="${LIME%.lime}".xml
${ILDGMDC} -o ${LIMEXML} -fmt -gc ${LFN}
