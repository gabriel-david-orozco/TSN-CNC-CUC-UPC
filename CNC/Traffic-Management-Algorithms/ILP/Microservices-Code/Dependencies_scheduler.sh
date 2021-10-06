#!/bin/bash
#For installing all the dependencies of the code
apt update
apt -y install nano wget
apt -y install software-properties-common << 'EOF'
8
29
EOF
apt -y install python3.9 
apt -y install python3-pip
pip install pandas
pip install networkx
pip install matplotlib
pip install glpk
cd ~
mkdir tmp
wget -P tmp https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh
bash tmp/Anaconda3-2021.05-Linux-x86_64.sh -b
source .bashrc
conda install -c conda-forge glpk
conda install -c conda-forge/label/gcc7 glpk
conda install -c conda-forge/label/broken glpk
conda install -c conda-forge/label/cf201901 glpk
conda install -c conda-forge/label/cf202003 glpk
