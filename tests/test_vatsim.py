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

Unit tests for src.vatsim module

"""
import unittest

from src.vatsim import VatsimStatus

class VatsimTest(unittest.TestCase):
    """Tests for VatsimStatus dataclass."""
    def test(self):
        """Test against a sample version of the status information."""
        with open('tests/sample.data', 'r') as file:
            file = file.readlines()
        status = VatsimStatus(file)

        self.assertIsNotNone(status.version)
        self.assertEqual(status.connected_clients, len(status.clients))
        self.assertTrue(len(status.voice_servers) > 0)
        for item in [*status.voice_servers, *status.clients, *status.servers, *status.prefile]:
            self.assertIs(type(item), dict)
        self.assertTrue(len(status.clients) > 0)
        self.assertTrue(len(status.servers) > 0)
        self.assertTrue(len(status.prefile) > 0)
