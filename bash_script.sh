#!/bin/bash

sudo apt-get install python3.8
sudo apt-get install python3-pip
sudo apt-get install python3-virtualenv
virtualenv -p /usr/bin/python3 ../venv
source ../venv/bin/activate

pip3 install -r requirements.dev.txt
pip3 install tox
pip3 install wheel
sudo apt-get install tox

echo "************************"
echo "Building the code:"
python setup.py sdist bdist_wheel

echo "************************"
echo "Running UnitTests :"
tox -vvv
