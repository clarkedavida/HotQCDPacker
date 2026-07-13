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

LFN="$1"

if [ -z "${LFN}" ]; then
    echo "Please set LFN"
fi

MC="${LFN%/*}"
MC="mc://${MC#lfn://}"

ENSXML="${MC##*/}".xml

LIME=$(basename "${LFN}")
LIMEXML="${LIME%.lime}".xml

# Download the ens xml
${ILDGMDC} -o "${ENSXML}" -fmt -ge "${MC}"

# Download the lime xml
${ILDGMDC} -o "${LIMEXML}" -fmt -gc "${LFN}"

# Download the lime file
${ILDGSE} -get "${LFN}" 

