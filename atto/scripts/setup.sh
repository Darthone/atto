#!/bin/bash

mkdir -p $INSTALL_DIR/logs
mkdir -p $INSTALL_DIR/certs
cd $INSTALL_DIR
virtualenv venv
source $INSTALL_DIR/venv/bin/activate
pip install -r $INSTALL_DIR/requirements.txt
python $INSTALL_DIR/scripts/generate_certificates.py

