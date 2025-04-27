@echo off
REM Remove any existing container with the same name (ignore errors)
docker rm -f order-manager-container >nul 2>&1

REM Run the container with the desired name
docker run --name order-manager-container my-python-app