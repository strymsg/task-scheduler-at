#!/bin/bash

#TODO: Install virtualenv

# Install requirements and preparing python environment
VENV=venv

echo "checking virtualenv..."


if [[ -d "$VENV" ]]
then
    echo "$VENV exists on your filesystem."
    source $VENV/bin/activate
else
    virtualenv --python=python3 venv
fi

echo "Installing python requirements"
pip install -r requirements.dev.txt
pip install coverage

echo "-------------------------------------"
echo "Running tests"
echo "-------------------------------------"

coverage -m pytest
echo "-------------------------------------"
echo "Coverage report"
echo "-------------------------------------"
coverage report -m

echo "-------------------------------------"
echo "Building and packaging"
echo "-------------------------------------"

if [[ -d "dist/" ]]
then
  echo ""
  echo "Forcing rebuild..."
  echo ""
  rm -rf dist
fi

python3 -m build

echo ""
echo "Package built see dist/ directory"
ls dist

echo
echo "Done building B-) "


echo "--------------------------------------"
echo "Running the flask server"
echo
echo

export FLASK_APP=main.py
export FLASK_ENV=development

flask run


