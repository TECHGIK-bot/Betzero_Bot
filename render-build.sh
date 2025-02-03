#!/bin/bash

# Update and install necessary dependencies for Chrome
apt-get update
apt-get install -y wget gnupg2 curl unzip
curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb
apt-get install -f

# Install the necessary ChromeDriver for Selenium
CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/local/bin/

# Clean up
rm google-chrome-stable_current_amd64.deb chromedriver_linux64.zip
