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


This module initializes all application wide components.

"""
# pylint: disable=C0103
# C0103 doesn't conform to UPPER_CASE naming style
import os

from eve import Eve
from celery import Celery

from config import config

celery = Celery(__name__,
                broker=os.environ.get('REDIS_URL', 'redis://'))
celery.config_from_object('celeryconfig')

def create_app(config_name=None):
    """Example function with types documented in the docstring.

    `PEP 484`_ type annotations are supported. If attribute, parameter, and
    return types are annotated according to `PEP 484`_, they do not need to be
    included in the docstring:

    Args:
        config_name (str): The configuration name to load (check module config.py).

    Returns:
        Eve: An initialized eve instance."""
    if config_name is None:
        config_name = os.environ.get('APP_CONFIG', 'development')
    app = Eve(__name__)
    app.config.from_object(config[config_name])

    # init extensions
    celery.conf.update(config[config_name].CELERY_CONFIG)

    return app
