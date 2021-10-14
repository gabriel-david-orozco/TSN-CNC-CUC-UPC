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
pip install networkx==2.6.3
pip install matplotlib
pip install pyomo
cd ~
mkdir tmp
wget -P tmp https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh
bash tmp/Anaconda3-2021.05-Linux-x86_64.sh
source .bashrc
conda install gurobi
