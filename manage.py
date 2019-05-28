#!/usr/bin/env python
"""
VATSIM API
Copyright (C) 2019  Pedro Rodrigues <prodrigues1990@gmail.com>

This file is part of VATSIM API.

VATSIM API is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 2 of the License.

VATSIM API is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with VATSIM API.  If not, see <http://www.gnu.org/licenses/>.


CLI module for app management and development tasks.

"""
import click
import subprocess
import sys
import os

@click.group()
def cli():
    pass

@cli.command()
@click.option('--host', '-h', default='0.0.0.0', help='The address the web app will listen in.')
@click.option('--port', '-p', default=5000, help='The TCP port to listen to')
@click.option('--debug', '-d', default=False, is_flag=True, help='Set enviroment mode')
def run(host, port, debug):
    """Runs a development web server."""
    if debug:
        from wsgi import app
        app.run(host=host, port=port, debug=debug)
    else:
        host = os.environ.get('HOST', host)
        port = os.environ.get('PORT', port)
        subprocess.call(['gunicorn', 'wsgi:app', '--bind', f'{host}:{port}', '--log-file=-'])

@cli.command()
def clock():
    """Runs the AP scheduler."""
    from clock import sched
    sched.start()

@cli.command()
def worker():
    """Runs a background celery worker."""
    subprocess.call(['celery', 'worker', '-A', 'worker.celery', '--loglevel=info'])

@cli.command()
def shell():
    """Runs a shell in the app context."""
    subprocess.call(['flask', 'shell'])

@cli.command()
def lint():
    """Runs pylinter."""
    lint = subprocess.call(['pylint', 'src'])
    sys.exit(lint)

@cli.group()
def tasks():
    """Manually schedules tasks."""

@tasks.command()
def update():
    """Schedules a database a update."""
    from src.tasks import update
    update.apply_async()

@cli.command()
@click.option('--only', help='Run only the specified test.')
def test(only=None):
    """Runs tests."""
    suite = ['coverage', 'run', '--source=src', '-m', 'unittest', '-v']
    if only:
        suite.append(only)
    tests = subprocess.call(suite)
    subprocess.call(['coverage', 'report', '--show-missing'])
    sys.exit(tests)

if __name__ == '__main__':
    cli()
