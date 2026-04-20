# 
# setUp.bash
# 
# D. Clarke
# 
# Get everything you need to run the HotQCD packer.
# 

CURRENTDIR=$(pwd)

INSTALLTOOLBOX=false
INSTALLQCDML=false
INSTALLILDGBINARY=false
INSTALLILDGSERVICE=false

CREATEQCDMLFOLDER=/home/${USER}/createQCDml # Folder where you want to put createQCDml
ILDGBINARYFOLDER=/home/${USER}/try-binary   # Folder where you want to put try-binary 
ILDGSERVICEFOLDER=/home/${USER}/createQCDml # Folder where you want to put try-client 

echo "Install parameters:"
echo "    QCDml folder: ${CREATEQCDMLFOLDER}"
echo "    try-binary folder: ${ILDGBINARYFOLDER}"
echo "    try-client folder: ${ILDGSERVICEFOLDER}"
echo "    Install AnalysisToolbox? ${INSTALLTOOLBOX}"
echo "    Install createQCDml? ${INSTALLQCDML}"
echo "    Download ILDG-binary? ${INSTALLILDGBINARY}"
echo "    Download ILDG-client? ${INSTALLILDGSERVICE}"

read -p "This will install using the above settings. Is that okay? (Y/y to proceed.) "
if ! [[ $REPLY =~ [Yy]$ ]]; then
    exit
fi

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
