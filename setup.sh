#!/bin/bash

# This script sets up the SHT20 sensor on a Raspberry Pi

sudo apt update
sudo apt upgrade -y

sudo cp upload-image.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable upload-image.service
sudo systemctl start upload-image.service
