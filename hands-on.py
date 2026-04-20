#
# hands-on.py
#
# D. Clarke
#
# Here we try some of the exercises in
#     https://slides.koutsou.net/ILDG-hands-on-2025-07-08/#1
# Some of them may require that you get a token. You can do that
# using setUpToken.bash
#

from packILDGcommon import ILDGMDC, ILDGFC, ILDGSE
from latqcdtools.base.utilities import shellVerbose

#shellVerbose(f'{ILDGMDC} -le')       # List ensembles in LDG catalogue
#shellVerbose(f'{ILDGMDC} -le -jldg') # List ensembles in JLDG catalogue

# Look for wilsonTmQuarkAction, beta=4.05 
#shellVerbose(f"{ILDGMDC} -qe 'wilsonTmQuarkAction beta=4.05'")

# Download one of the ensemble XMLs into ens.xml
#shellVerbose(f"{ILDGMDC} -ge mc://ldg/etmc/tmqcd_nf2/tlSym_b3.8_L20T48_k0.164099_mu0.0060 -fmt -o ens.xml")
# Also show that it is a valid XML.
#shellVerbose(f"{ILDGMDC} -ve ens.xml")

# List configurations with this mcURI 
# mcURI="mc://ldg/etmc/tmqcd_nf2/tlSym_b4.2_L48T96.154073_mu0.002"
# shellVerbose(f"{ILDGMDC} -lc {mcURI}")

# List all storage allocations
#shellVerbose(f"{ILDGFC} -la")

# List all files under storage allocation z-ho (one of the above listed)
# Shows an SURL, which is a "Storage" URL
#shellVerbose(f"{ILDGFC} -lsa z-ho")

# Get the SURL of conf with the supplied LFN
#LFN="lfn://hands-on/rqcd/qcdML/ens_001_example/config_1"
#shellVerbose(f"{ILDGFC} -ll {LFN}") 

# Download one of the config XMLs into conf.xml
#LFN="lfn://hands-on/rqcd/qcdML/ens_001_example/config_1"
#shellVerbose(f"{ILDGMDC} -o config.xml -fmt -gc {LFN}")

# The SURLs given above are what are needed to download files using the
# try-se script. Here is an example
#SURL="https://dcache-desy-webdav.desy.de:2880/pnfs/desy.de/ildg/ldg/cls/nf21/D200r000/D200r000n9.lime"
#shellVerbose(f"{ILDGSE} -get {SURL}") 

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

