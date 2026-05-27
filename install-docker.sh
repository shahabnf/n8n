#!/usr/bin/env bash

set -e

echo "== Detecting OS =="

if [ ! -f /etc/os-release ]; then
    echo "Cannot detect operating system."
    exit 1
fi

source /etc/os-release

OS_ID="$ID"
CODENAME="$VERSION_CODENAME"

echo "Detected OS: $OS_ID"
echo "Detected Codename: $CODENAME"

if [[ "$OS_ID" != "ubuntu" && "$OS_ID" != "debian" ]]; then
    echo "Unsupported OS: $OS_ID"
    exit 1
fi

echo "== Installing dependencies =="

apt-get update

apt-get install -y \
    ca-certificates \
    curl \
    gnupg

echo "== Setting up Docker repository =="

install -m 0755 -d /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/$OS_ID/gpg \
    -o /etc/apt/keyrings/docker.asc

chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
  https://download.docker.com/linux/$OS_ID \
  $CODENAME stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

echo "== Installing Docker =="

apt-get update

apt-get install -y \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin

echo "== Docker Installed =="

docker --version
docker compose version