#!/bin/bash
#Dependencies Script
apt update
apt -y install nano
echo _______________________________testing0_______________________________
apt -y install software-properties-common << 'EOF'
8
29
EOF
echo _______________________________testing1_______________________________
apt -y install python3.9 
echo _______________________________testing2_______________________________
apt -y install python3-pip
echo testing3
pip3 --version