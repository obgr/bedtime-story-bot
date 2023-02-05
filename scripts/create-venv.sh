#!/bin/bash

if [ -d "venv" ] 
then
    echo "Directory venv exists, removing it before building a new venv." 
    rm -rf venv
else
    echo "Directory venv does not exists."
fi

python3 --version


mkdir venv \
  && python3 -m venv venv \
  && source venv/bin/activate \
  && pip3 install -r requirements.txt