#!/bin/bash
# 
# getToken.bash                                                               
# 
# D. Clarke
# 
# Some of the actions in the metadata catalogue require you to have
# a "token". Tokens provide short-lived access credentials. In our
# case, the access tokens are valid for 1h and the identity tokens
# are valid for 10 min.
#
#

source env.bash

token=${ILDGSERVICEFOLDER}/try-token
GROUP=/ldg/hotqcd

# Correct way to call as of 20 Apr 2026. Will give READ, MODIFY, and WRITE
# permissions for uploading of HotQCD configurations to LDG.
OPT_S="storage.read:/public/ storage.read:/ldg/ storage.read:${GROUP}/ storage.modify:${GROUP}/ metadata.write:${GROUP}/"
${token} -v -c -s "$OPT_S"

