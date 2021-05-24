#!/bin/bash

# Install requirements and preparing python environment
VENV=venv

echo "checking virtualenv..."
if ! virtualenv -v COMMAND &> /dev/null
then
    echo 
    echo "Need to have virtualenv to install requirements"
    echo "use: apt install virtualenv python3-virtualenv"
    exit 1
fi

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

# checking docker for databases
if ! docker -v COMMAND &> /dev/null
then
    echo
    echo "Need docker to be installed for completing tests"
    echo "Need mongo and redis container running"
    echo "Warning, tests will not finish successfully"
fi

coverage run -m pytest
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

pip3 install build

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

<<<<<<< HEAD
flask run
=======
flask run
>>>>>>> 1669d0047dc38a3da20c8fb7689a48f4be7f34dd
