#!/bin/bash
set -e

DEPLOY_DIR="/home/ubuntu/xarillian.com"
VENV_DIR="$DEPLOY_DIR/venv"

sudo apt-get update -y
sudo apt-get install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx

sudo mkdir -p "$DEPLOY_DIR"
sudo chown ubuntu:ubuntu "$DEPLOY_DIR"

cd "$DEPLOY_DIR"

if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -sf /etc/nginx/sites-available/xarillian.com /etc/nginx/sites-enabled/
sudo systemctl restart nginx
