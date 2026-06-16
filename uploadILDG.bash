#!/bin/bash
#
# uploadILDG.bash
#
# D. Clarke
#
# Wrap together the commands needed to upload to ILDG. Call with
#   uploadILDG.bash <lime-xml-file-name>
#

source env.bash
source "${bashToolsPath}/bashTools.bash"

# Get limeXML from user.
if [ -z "$1" ]; then
    echo "ERROR: no lime XML file provided. Usage: uploadILDG.bash <limeXML>"
    exit 1
fi
LIMEXML="$1"

# Written by Claude, sorry that this is unreadable.
LFN=$(sed -n 's|.*<dataLFN>\(.*\)</dataLFN>.*|\1|p' "${LIMEXML}")
ENS=$(basename "$(sed -n 's|.*<markovChainURI>\(.*\)</markovChainURI>.*|\1|p' "${LIMEXML}")")
ENSXML="${ENS}.xml"
LIME=$(basename "${LFN}")
SURL="${SE}/${LFN#lfn://}"

# A weak check that these variables were actually populated
for var in LFN ENS ENSXML LIME SURL; do
    if [ -z "${!var}" ]; then
        echo "ERROR: ${var} is empty. Check ${LIMEXML}."
        exit 1
    fi
done

# Upload ensemble. This will only work the first time. After that
# this does nothing, because the XML already exists
${ILDGMDC} -ie ${ENSXML}

# Upload lime XML
_bashInfo "upload XML"
${ILDGMDC} -ic ${LIMEXML}
_checkForFail $? "upload lime XML"

# Upload lime file
_bashInfo "upload lime"
time ${ILDGSE} -put ${LIME} ${SURL}
_checkForFail $? "upload lime"

# Link LFN to SURL
_bashInfo "link LFN and SURL"
${ILDGFC} -i ${LFN} ${SURL}
_checkForFail $? "link LFN and SURL"

