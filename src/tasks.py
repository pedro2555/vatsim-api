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
# pylint: disable=C0103,W1203
# C0103 doesn't conform to UPPER_CASE naming style
# W1203: Use % formatting in logging functions and pass the % parameters as arguments
import logging
import json
from datetime import datetime
import requests
from wsgi import app
from .vatsim import VatsimStatus
from . import celery

@celery.task()
def update_status():
    """Updates vatsim status information if older than a predefined time (60 seconds).

    Args:
        resource (str): The endpoint name being accessed
    """
    now = datetime.utcnow()
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
        # keep location history
        if item['clienttype'] == 'PILOT':
            try:
                item['location_history'] = existing['location_history']
            except (KeyError, TypeError):
                item['location_history'] = {'type': 'linestring', 'coordinates': list()}
            try:
                if item['location'] != existing['location']:
                    item['location_history']['coordinates'].append(item['location'])
            except (KeyError, TypeError):
                pass
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
    db.remove({'_updated': {'$lt': now}})


@celery.task()
def update_events():
    # load events from the server
    r = requests.get('http://api.vateud.net/events.json')

    # early exit on non 200 responses, we're not expecting anything else
    if r.status_code != 200:
        logging.info(f'update_events: vateud API returned {r.status_code}')

    date_format = r'%Y-%m-%dT%H:%M:%SZ'
    events_collection = app.data.driver.db['events']
    events = json.loads(r.text)
    for event in events:
        # early exit on existing events (not sure if they update the things or
        # not, but theres no etag, or any other evident versioning scheme, so
        # we're skiping on updated records until that is clarified)
        if events_collection.find_one({'vateud_id': event['id']}):
            continue

        now = datetime.now()
        events_collection.insert_one({
            '_created': now,
            '_updated': now,
            'vateud_id': event['id'],
            'title': event['title'],
            'subtitle': event['subtitle'],
            'description': event['description'],
            'airports': event['airports'].split(', '),
            'banner_url': event['banner_url'],
            'starts': datetime.strptime(event['starts'], date_format),
            'ends': datetime.strptime(event['ends'], date_format)
        })