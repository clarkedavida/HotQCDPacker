# Generate token and set in env or .bashrc:
token=/home/dclarke/try-client/try-token

# Correct way to call as of 20 Apr 2026
OPT_S="storage.read:/public/ storage.read:/ldg/ storage.read:/hands-on/ storage.modify:/hands-on/ metadata.write:/hands-on/"
$token -v -c -s "$OPT_S"

