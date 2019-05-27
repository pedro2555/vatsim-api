# VATSIM API

A RESTfull HTTP API providing VATSIM data.

## Application Stack

All stack programs run at Heroku, the REST API is available at
[vatsim-api.herokuapp.com](https://vatsim-api.herokuapp.com/).

### HTTP API

A Python-EVE based API exposing the client visible layer, exposes database information to clients
with a mongodb query syntax.

#### Starts with

```bash
python manage.py run
```

### Celery Background Worker

A Celery application that listens for tasks to be executed.

#### Starts with

```bash
python manage.py worker
```

#### Clock

An APScheduler application responsible to dispatch recorrent tasks.

#### Starts with

```bash
python manage.py clock
```


## Development Environment

### Requirements

 * Python 3.7+
 * A MongoDB instance
 * A Redis instance

### Setup

What you'll do:
 * Checkout a local version of the repository
 * Create a python virtual environment
 * Install required python packages
 * Run the app

#### Checkout a local version of the repository

```bash
git clone git@github.com:pedro2555/vatsim-api.git
```

Alternatively you can use an HTTPS url:

```bash
git clone https://github.com/pedro2555/vatsim-api.git
```

#### Create a python virtual environment

A python 3.7 runtime is expected at `/usr/bin/python3.7`, you may change this to fit your
environment.

```bash
virtualenv --python=/usr/bin/python3.7 venv
source venv/bin/activate
```

#### Install required python packages

```bash
pip install -r requirements.txt
```

#### Run the app

As mentioned before, you need both MongoDB and Redis instances runnnig locally. You may skip this
step if the instances are already running.

```bash
sudo service mongodb start
sudo service redis start
```

Start the app

```bash
python manage.py run
```