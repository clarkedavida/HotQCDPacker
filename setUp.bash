# 
# setUp.bash
# 
# D. Clarke
# 
# Get everything you need to run the HotQCD packer.
# 

source env.bash

CURRENTDIR=$(pwd)

# Adjust as needed
INSTALLTOOLBOX=false
INSTALLQCDML=false
INSTALLILDGBINARY=false
INSTALLILDGSERVICE=false

echo
echo "Install parameters:"
echo "    QCDml folder:            ${CREATEQCDMLFOLDER}"
echo "    try-binary folder:       ${ILDGBINARYFOLDER}"
echo "    try-client folder:       ${ILDGSERVICEFOLDER}"
echo "    Install AnalysisToolbox? ${INSTALLTOOLBOX}"
echo "    Install createQCDml?     ${INSTALLQCDML}"
echo "    Download ILDG-binary?    ${INSTALLILDGBINARY}"
echo "    Download ILDG-client?    ${INSTALLILDGSERVICE}"
echo " (Folders can be adjusted in env.bash)"
echo

read -p "This will install using the above settings. It will also export a HOTQCDPACKER_DIR to the bashrc. Is that okay? (Y/y to proceed.) "
if ! [[ $REPLY =~ [Yy]$ ]]; then
    exit
fi

# Written by Claude. Export HOTQCDPACKER_DIR to ~/.bashrc so upload/download scripts can be run from anywhere.
if ! grep -q "HOTQCDPACKER_DIR" ~/.bashrc; then
    echo "" >> ~/.bashrc
    echo "# HotQCDPacker" >> ~/.bashrc
    echo "export HOTQCDPACKER_DIR=\"${CURRENTDIR}\"" >> ~/.bashrc
    echo "    Added HOTQCDPACKER_DIR to ~/.bashrc. Please re-source or open a new terminal."
else
    sed -i "s|^export HOTQCDPACKER_DIR=.*|export HOTQCDPACKER_DIR=\"${CURRENTDIR}\"|" ~/.bashrc
    echo "    Updated HOTQCDPACKER_DIR in ~/.bashrc. Please re-source or open a new terminal."
fi

# Written by Claude. Sorry that it's hard to read.
sed -i "s|^HOTQCD_PACK_FOLD *=.*|HOTQCD_PACK_FOLD = '${CURRENTDIR}'|" packILDGcommon.py
sed -i "s|^ILDG_BINARY_FOLD *=.*|ILDG_BINARY_FOLD = '${ILDGBINARYFOLDER}'|" packILDGcommon.py
sed -i "s|^ILDG_CLIENT_FOLD *=.*|ILDG_CLIENT_FOLD = '${ILDGSERVICEFOLDER}'|" packILDGcommon.py

if [ "$INSTALLTOOLBOX" = true ]; then
    echo "AnalysisToolbox: Installing..."
    pip install latqcdtools
fi

if [ "$INSTALLQCDML" = true ]; then
    echo "QCDml: Downloading..." 
    git clone https://github.com/LatticeQCD/createQCDml.git ${CREATEQCDMLFOLDER}
    cd ${CREATEQCDMLFOLDER}
    echo "QCDml: Installing..." 
    bash installQCDmlUtils.bash
    echo "QCDml: At this point, you may need to exit and re-open your terminal."
    cd ${CURRENTDIR}
fi

if [ "$INSTALLILDGBINARY" = true ]; then
    echo "ILDG-binary: Downloading..." 
    git clone https://gitlab.desy.de/ildg/hands-on/try-binary.git ${ILDGBINARYFOLDER} 
    echo "ILDG-binary: You are going to need to compile this"
fi

if [ "$INSTALLILDGSERVICE" = true ]; then
    echo "ILDG-client: Downloading..." 
    git clone https://gitlab.desy.de/ildg/hands-on/try-client.git ${ILDGSERVICEFOLDER} 
fi
