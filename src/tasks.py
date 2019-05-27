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


Async tasks definitions.

"""
# pylint: disable=C0103
# C0103 doesn't conform to UPPER_CASE naming style
from datetime import datetime, timedelta
from wsgi import app
from .vatsim import VatsimStatus
from . import celery

@celery.task()
def update():
    """Updates vatsim status information if older than a predefined time (60 seconds).

    Args:
        resource (str): The endpoint name being accessed
    """
    # verify if an update is due
    db = app.data.driver.db['dataversion']
    dataversion = db.find_one()
    now = datetime.utcnow()
    if dataversion:
        _last_update = dataversion['_updated'].replace(tzinfo=None)
    else:
        _last_update = now - timedelta(seconds=60)
    seconds_since_update = (now - _last_update).total_seconds()
    if seconds_since_update < 60 and not app.debug:
        return
    if dataversion:
        dataversion['_updated'] = now
        db.save(dataversion)
    else:
        db.insert_one({'_created': now, '_updated': now})

    # fetch and save data
    status = VatsimStatus.from_url()
    def save(existing, new):
        new['_updated'] = now
        if existing:
            existing.update(new)
            db.save(existing)
        else:
            new['_created'] = now
            db.insert_one(new)

    db = app.data.driver.db['voice_servers']
    for item in status.voice_servers:
        existing = db.find_one({'hostname_or_IP': item['hostname_or_IP']})
        save(existing, item)
    db.remove({'_updated': {'$lt': now}}) # purge offline clients
    db = app.data.driver.db['clients']
    for item in status.clients:
        existing = db.find_one({
            'callsign': item['callsign'],
            'cid': item['cid'],
            'clienttype': item['clienttype']})
        save(existing, item)
    db.remove({'_updated': {'$lt': now}})
    db = app.data.driver.db['servers']
    for item in status.servers:
        existing = db.find_one({'hostname_or_IP': item['hostname_or_IP']})
        save(existing, item)
    db.remove({'_updated': {'$lt': now}})
    db = app.data.driver.db['prefile']
    for item in status.prefile:
        existing = db.find_one({'callsign': item['callsign'], 'cid': item['cid']})
        save(existing, item)
