#!/usr/bin/env bash
# Update package lists
sudo apt-get update

# Install Chrome
wget -qO- https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb > chrome.deb
sudo dpkg -i chrome.deb
rm chrome.deb
sudo apt-get --fix-broken install -y

# Install Chromedriver
CHROME_VERSION=$(google-chrome --version | grep -oP '[0-9]+(\.[0-9]+)*')

