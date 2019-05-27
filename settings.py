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
	'groundspeed': {'type': 'number'},
	'altitude': {'type': 'number'},
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
firs_schema = {
	'icao': {
		'type': 'string'
	},
	'name': {'type': 'string'},
	'location': {'type': 'point'},
	'boundaries': {'type': 'polygon'},
	'callsigns': {
		'type': 'list',
        'schema': {'type': 'string'}
	}
}
firs = {
	'schema': firs_schema,
	'resource_methods': ['GET', 'POST'],
	'item_methods': ['GET', 'PATCH', 'PUT'],
	'pagination': False
}
data_version = {
	'schema': {},
	'internal_resource': True
}

DOMAIN = {
	'voice_servers': copy(default),
	'clients': clients,
	'servers': copy(default),
	'prefiles': copy(default),
	'firs': firs,
	'dataversion': data_version
}

# We want to seamlessy run our API both locally and on Heroku. If running on
# Heroku, sensible DB connection settings are stored in environment variables.
MONGO_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/vatsim-api')

X_DOMAINS = '*'
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
MONGO_QUERY_BLACKLIST = ['$where', '$regex']
