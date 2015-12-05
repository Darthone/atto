# atto
------
Lightweight Monitoring System


Intro
-----

Atto aims to be a lightweight monitoring solution. This is currently a prototype and should not be relied on for anything serious.

Prerequisites:
- [virtualenv](https://virtualenv.readthedocs.org/en/latest/installation.html)
- [npm](https://github.com/npm/npm)
- grunt `npm install -g grunt-cli`

Setup
-----

First Clone the Repo
```bash
git clone https://github.com/Darthone/atto.git && cd atto
```

Server or Client
```bash
cd atto/
INSTALL_DIR=$(pwd) ./scripts/setup.sh
# Edit configurations in ./configs
source venv/bin/activate
cd bin
# start client or server or both
python client.py &
# distribute to other clients as desired, and add client IPs to auth list in config/server.yml
python server.py &
# Make sure log/ files are growing in size
```

Backend
```bash
cd backend/
./setup.sh
source venv/bin/activate && python setup.py
./run.py &
# REST API now running on 0.0.0.0:5001
```

UI
```bash
cd ui/
npm install
bower install
vi ./app/scripts/services/backendfactory.js
# set var BACK_URL = "http://$IP_ADDR:5001/";   where IP_ADDR is the IP address of the server running the backend.
# Avoid using 127.0.0.01
grunt serve
# Web UI now running on 0.0.0.0:9999/
```


