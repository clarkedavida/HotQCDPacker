#!/bin/bash
# 
# setUpToken.bash                                                               
# 
# D. Clarke
# 
# Some of the actions in the metadata catalogue require you to have
# a "token". Tokens provide short-lived access credentials. In our
# case, the access tokens are valid for 1h and the identity tokens
# are valid for 10 min.

token=/home/dclarke/try-client/try-token

# Correct way to call as of 20 Apr 2026
OPT_S="storage.read:/public/ storage.read:/ldg/ storage.read:/hands-on/ storage.modify:/hands-on/ metadata.write:/hands-on/"
$token -v -c -s "$OPT_S"

