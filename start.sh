#!/bin/bash

cd "$(dirname "$0")"

# Build images and start containers
docker-compose up -d --build

echo "✅ n8n and Telegram bot started!"
echo "Check n8n tunnel URL:"
docker logs n8n
