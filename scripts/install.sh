#!/bin/bash
set -e

sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx

sudo mkdir -p /home/ubuntu/xarillian.com
sudo chown ubuntu:ubuntu /home/ubuntu/xarillian.com

cd /home/ubuntu/xarillian.com

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
pip install gunicorn

deactivate