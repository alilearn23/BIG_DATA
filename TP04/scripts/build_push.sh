#!/usr/bin/env bash
set -euo pipefail
# ===  القيم ===
DOCKER_USERNAME="alilkahoues"
IMAGE_NAME="tp4-dockerized-tp03"
IMAGE_TAG="latest"
# ===================
FULL="${DOCKER_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}"
echo "[1/3] Building ${FULL} ..."
docker build -t "${IMAGE_NAME}:${IMAGE_TAG}" .
echo "[2/3] Tagging ..."
docker tag "${IMAGE_NAME}:${IMAGE_TAG}" "${FULL}"
echo "[3/3] Pushing ..."
docker push "${FULL}"
echo "Pushed: ${FULL}"
