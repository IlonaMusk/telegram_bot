#!/usr/bin/env bash

apt-get update
apt-get install -y chromium-browser chromium-chromedriver

python bot.py