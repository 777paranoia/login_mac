#!/bin/bash

python3 -m venv venv
source ./venv/bin/activate

if ! command -v pip &> /dev/null; then
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
    rm get-pip.py
fi

pip install -r requirements.txt

mkdir -p ~/.login_log

sed -i '' "s|\$USER|$USER|g" com.showcrewnetwork.login.plist
cp com.showcrewnetwork.login.plist ~/Library/LaunchAgents/com.showcrewnetwork.login.plist

launchctl load ~/Library/LaunchAgents/com.showcrewnetwork.login.plist

