# VATSIM API

We provide full VATSIM statistics for connected clients and servers via a public RESTfull API.

All data we collect is publicly available from [VATSIM](https://status.vatsim.net/). On top of that information we expose some other tools for developers to query this information.

Our features:
 * Location information complies with the [GEOJson](https://tools.ietf.org/html/rfc7946) format;
 * Location history for all connected clients;
 * MongoDB query syntax.

## How it Works

### Data Collection

We schedule data collection from VATSIM, roughly, every minute. This is done by a 'clock process' leveraging the [APScheduler](https://apscheduler.readthedocs.io/en/latest/) library. This process schedules update operations to be run by a worker.

Data collection and transformations is executed by a 'worker process' using [Celery](http://www.celeryproject.org/). This process listens for scheduled jobs and executes them.

A job queue is provided by [Redis](https://redis.io/).
All results are stored in a [MongoDB](https://www.mongodb.com/) database.

On top of the same database we added an HTTP layer exposing the REST API, using [Python-Eve](https://docs.python-eve.org/en/stable/)

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