#
# uploadILDG.py
#
# D. Clarke
#
# Wrap together the commands needed to upload to ILDG. 
#

from packILDGcommon import ILDGMDC, ILDGFC, ILDGSE
from latqcdtools.base.utilities import shellVerbose

# Upload an ensemble XML file. Where the ensemble XML is uploaded is controlled
# by the markovChainURI of the XML. So you need to make sure you got a token that
# has permission to upload where you want to. (Similarly the LFN controls where
# the config/lime XML is uploaded. If you generate your LFN and mcURI through
# createQCDml, they should automatically fit together correctly.)
#
# try-mdc -ie ens.xml
# try-mdc -ic cfg.xml

# Once you've uploaded ensemble XML and lime XML, you need to upload the LIME itself.
# You can do that with this one:
#
# export LDG_Z=https://globe-door.ifh.de:2880/pnfs/ifh.de/acs/grid/ildg/
# try-se -put data.txt $LDG_Z/hands-on/homework/ens999/cfg123
#
# For your purpose, you will need to figure out what SE you are using.

# Finally you have to register the uploaded conf in the file catalogue.
# try-fc -i <lfn> <surl>

# Now you should be able to see the lattice you uploaded
# try-se -list <LFN> -lol
# If you see NEARLINE instead of ONLINE, it is on tape, so you may need to wait
# for the tape arm to get where it needs to go before your conf is downloaded



