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


Module with Eve app specific settings.

"""
import os
from copy import copy

default = {
	'schema': {},
	'allow_unknown': True,
	'resource_methods': ['GET'],
	'item_methods': ['GET'],
	'pagination': False
}
clients_schema = {
	'callsign': {
		'type': 'string',
		'unique': True
	},
	'cid': {'type': 'string'},
	'realname': {'type': 'string'},
	'clienttype': {'type': 'string'},
	'location': {'type': 'point'},
	'location_history': {'type': 'linestring'},
	'groundspeed': {'type': 'number'},
	'altitude': {'type': 'number'},
	'heading': {'type': 'number'},
	'planned_altairport': {'type': 'string'},
	'planned_depairport': {'type': 'string'},
	'planned_destairport': {'type': 'string'},
	'planned_aircraft': {'type': 'string'},
	'planned_tascruise': {'type': 'string'},
	'planned_altitude': {'type': 'string'},
	'planned_route': {'type': 'string'},
	'transponder': {'type': 'number'},
	'boundaries': {
		'type': 'objectid',
		'required': False,
		'data_relation': {
			'resource': 'firs',
			'field': '_id',
			'embeddable': True
		},
    },
}
clients = {
	'schema': clients_schema,
	'allow_unknown': True,
	'resource_methods': ['GET'],
	'item_methods': ['GET'],
	'pagination': False,
	'mongo_indexes': {
		'location_2d': [ ('location', '2d') ],
		'location_2dsphere': [ ('location', '2dsphere') ],
        'callsign_text': [ ('callsign', 'text') ]
	}
}
pilots = {
	'schema': clients_schema,
	'datasource': {
		'source': 'clients',
		'filter': {'clienttype': 'PILOT'}
	},
	'resource_methods': ['GET'],
	'item_methods': ['GET'],
	'pagination': False
}
controllers = {
	'schema': clients_schema,
	'datasource': {
		'source': 'clients',
		'filter': {'clienttype': 'ATC'}
	},
	'resource_methods': ['GET'],
	'item_methods': ['GET'],
	'pagination': False
}
events_schema = {
	# this is just used for definitely avoid duplicated records
	# and quite a nice way to keep track of things overall
	'vateud_id': {
			'type': 'integer',
			'unique': True
	},
	'title': {'type': 'string'},
	'subtitle': {'type': 'string'},
	'description': {'type': 'string'},
	'airports': {'type': 'list'},
	'banner_url': {'type': 'string'},
	'starts': {'type': 'datetime'},
	'ends': {'type': 'datetime'}
}
events = {
	'schema': events_schema,
	'item_title': 'event',
	'resource_methods': ['GET'],
	'item_methods': ['GET'],
	'pagination': False
}

DOMAIN = {
	'voice_servers': copy(default),
	'clients': clients,
	'pilots': pilots,
	'controllers': controllers,
	'servers': copy(default),
	'prefile': copy(default),
	'events': events
}

# We want to seamlessy run our API both locally and on Heroku. If running on
# Heroku, sensible DB connection settings are stored in environment variables.
MONGO_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/vatsim-api')

X_DOMAINS = '*'
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
MONGO_QUERY_BLACKLIST = ['$where', '$regex']
