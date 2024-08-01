#!/bin/bash

#chmod +x create_pixi_service.sh
#RUN THE SCRIPT
#sudo ./create_pixi_service.sh

# Get the current directory name
CURRENT_DIR=$(basename "$PWD")

# Get the current path
CURRENT_PATH=$(pwd)

# Get the current user
CURRENT_USER=$(whoami)

# Get the pixi task name from pixi.toml using awk
PIXITASKNAME=$(awk -F= '/^\[tasks\]/{getline; gsub(/^[ \t]+|[ \t]+$/, "", $1); print $1}' pixi.toml)

# Create the service file content
SERVICE_FILE_CONTENT="[Unit]
Description=Run ${CURRENT_DIR} Service
After=network.target

[Service]
Type=simple
WorkingDirectory=${CURRENT_PATH}
ExecStart=/usr/bin/pixi run ${PIXITASKNAME}
Restart=on-failure
User=${CURRENT_USER}
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target"

# Define the service filename
SERVICE_FILENAME="${CURRENT_DIR}.service"

# Create and write to the service file
echo "$SERVICE_FILE_CONTENT" | sudo tee /etc/systemd/system/$SERVICE_FILENAME

# Reload systemd to recognize the new service
sudo systemctl daemon-reload

# Start the new service
sudo systemctl start $SERVICE_FILENAME

# Enable the service to start on boot
sudo systemctl enable $SERVICE_FILENAME

# Show the status of the service
sudo systemctl status $SERVICE_FILENAME
