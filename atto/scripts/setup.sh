#!/bin/bash

mkdir -p ../logs
mkdir -p ../certs
cd ..
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python scripts/generate_certificates.py

