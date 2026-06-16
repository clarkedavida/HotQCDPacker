#!/bin/bash
#
# downloadILDG.bash
#
# D. Clarke
#
# Wrap together the commands needed to download a lime file
# and its XML. These can then be used to reconstruct configurations
# using upackILDG.py  
#   downloadILDG.bash <LFN>
#

source "${HOTQCDPACKER_DIR}/env.bash"

echo "I ALSO NEED TO DOWNLOAD ENS XML"
exit()

LFN="$1"

if [ -z "${LFN}" ]; then
    echo "Please set LFN"
fi

LIME=$(basename "${LFN}")
LIMEXML="${LIME%.lime}".xml

# Download the lime xml
${ILDGMDC} -o "${LIMEXML}" -fmt -gc "${LFN}"

# Download the lime file
${ILDGSE} -get "${LFN}" 

