# 
# setUp.bash
# 
# D. Clarke
# 
# Get everything you need to run the HotQCD packer.
# 

CREATEQCDMLFOLDER=/home/${USER}/createQCDml    # Folder where you want to put createQCDml
CURRENTDIR=$(pwd)
INSTALLTOOLBOX=true
INSTALLQCDML=true

echo "QCDml folder: ${CREATEQCDMLFOLDER}"
echo "Install AnalysisToolbox: ${INSTALLTOOLBOX}"
echo "Install createQCDml: ${INSTALLQCDML}"

read -p "This will install using the above settings. Is that okay? (Y/y to proceed.) "
if ! [[ $REPLY =~ [Yy]$ ]]; then
    exit
fi

if [ "$INSTALLTOOLBOX" = true ]; then
    pip install latqcdtools
fi

if [ "$INSTALLQCDML" = true ]; then
    git clone https://github.com/LatticeQCD/createQCDml.git ${CREATEQCDMLFOLDER}
    cd ${CREATEQCDMLFOLDER}
    bash installQCDmlUtils.bash
    echo "At this point, you may need to exit and re-open your terminal."
    cd ${CURRENTDIR}
fi
