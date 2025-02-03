#!/bin/bash

# Install Google Chrome (no need for sudo)
wget -q -O chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get update && apt-get install -y ./chrome.deb
rm chrome.deb

# Install ChromeDriver using WebDriver Manager (recommended)
pip install selenium webdriver-manager

echo "Setup complete!"
