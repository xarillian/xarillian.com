#!/bin/bash
sudo apt-get update
sudo apt-get install -y python3-venv python3-pip
python3 -m venv /home/ubuntu/xarillian.com/venv
source /home/ubuntu/xarillian.com/venv/bin/activate
pip install -r /home/ubuntu/xarillan.com/requirements.txt
