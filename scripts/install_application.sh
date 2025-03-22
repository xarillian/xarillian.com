#!/bin/bash
set -e

DEPLOY_DIR="/home/ubuntu/xarillian.com"
VENV_DIR="$DEPLOY_DIR/venv"

sudo apt-get update -y
sudo apt-get install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx

sudo mkdir -p "$DEPLOY_DIR"
sudo chown -R ubuntu:ubuntu "$DEPLOY_DIR"

cd "$DEPLOY_DIR"

if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
pip install --upgrade -r requirements.txt

sudo chown -R ubuntu:ubuntu app/static

echo "Starting prebuild steps..."
mkdir -p app/static/raw_posts
mkdir -p app/static/posts
mkdir -p app/static/styles

python -m app.prebuild.prebuild_blog || echo "Warning: prebuild_blog failed, continuing anyway"
python -m app.prebuild.bundle_css || echo "Warning: bundle_css failed, continuing anyway"
echo "Prebuild steps complete."

deactivate