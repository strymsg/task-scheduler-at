#!/bin/bash

pip install tox
echo "************************"
echo "Compiling the code:"

echo "************************"
echo "Building the code:"
python setup.py sdist bdist_wheel

echo "************************"
echo "Running UnitTests :"
tox -v
