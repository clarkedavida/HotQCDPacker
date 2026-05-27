#
# hands-on.py
#
# D. Clarke
#
# Here we try some of the exercises in
#     https://slides.koutsou.net/ILDG-hands-on-2025-07-08/#1
# Some of them may require that you get a token. You can do that
# using getToken.bash
#

from packILDGcommon import ILDGMDC, ILDGFC
from latqcdtools.base.utilities import shellVerbose

shellVerbose(f'{ILDGMDC} -le')       # List ensembles in LDG catalogue
shellVerbose(f'{ILDGMDC} -le -jldg') # List ensembles in JLDG catalogue

# Look for wilsonTmQuarkAction, beta=4.05 
shellVerbose(f"{ILDGMDC} -qe 'wilsonTmQuarkAction beta=4.05'")

# List configurations with this mcURI 
mcURI="mc://ldg/etmc/tmqcd_nf2/tlSym_b4.2_L48T96.154073_mu0.002"
shellVerbose(f"{ILDGMDC} -lc {mcURI}")

# Get the SURL of conf with the supplied LFN
LFN="lfn://hands-on/rqcd/qcdML/ens_001_example/config_1"
shellVerbose(f"{ILDGFC} -ll {LFN}") 
