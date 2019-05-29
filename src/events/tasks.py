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
from .. import celery

@celery.task()
def update():
    """Updates VATEUD events.
    """
    # load events from the server
    r = requests.get('http://api.vateud.net/events.json')

    # early exit on non 200 responses, we're not expecting anything else
    if r.status_code != 200:
        logging.info(f'update_events: vateud API returned {r.status_code}')

    date_format = r'%Y-%m-%dT%H:%M:%SZ'
    now = datetime.now()
    db = app.data.driver.db['events']
    events = json.loads(r.text)
    for event in events:
        # early exit on existing events (not sure if they update the things or
        # not, but theres no etag, or any other evident versioning scheme, so
        # we're skiping on updated records until that is clarified)
        if db.find_one({'vateud_id': event['id']}):
            continue

        db.insert_one({
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
    db.remove({'ends': {'$lt': now}})
