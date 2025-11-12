#!/usr/bin/env bash
set -euo pipefail
# === عدّل القيم ===
DOCKER_USERNAME="alilkahoues"
IMAGE_NAME="tp4-dockerized-tp03"
IMAGE_TAG="latest"
NET="mynetwork"
# ===================
FULL="${DOCKER_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}"
docker pull "${FULL}"
docker network inspect "${NET}" >/dev/null 2>&1 || docker network create "${NET}"
docker run -d --name c1 --network "${NET}" -p 8081:80 "${FULL}"
docker run -d --name c2 --network "${NET}" -p 8082:80 "${FULL}"
docker run -d --name c3 --network "${NET}" -p 8083:80 "${FULL}"
echo "Open: http://localhost:8081  http://localhost:8082  http://localhost:8083"
