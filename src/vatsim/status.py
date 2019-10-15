from random import choice
import logging
import re
import requests

from . import STATUS_SERVERS

def get_status_info(status_file=None):
    """Returns the update time for the status file an iterable of all status entities.

    Args:
        status_file (iter, optional): The status file lines, obtained automatically from a random
            vatsim status server.

    Returns:
        int, iter: The update number or None, an iterable with status entities.
    """
    if status_file is None:
        status_file = _get_status_file()
    for line in status_file:
        match = re.match(r'^UPDATE\s=\s(?P<update>[\d]+)$', line)
        if not match:
            continue

        update = match.group(1)
        return update, _iter_status(status_file)
    return None, iter(())

def _get_status_file():
    url = choice(STATUS_SERVERS)
    resp = requests.get(url)
    if resp.status_code != 200:
        return

    yield from resp.iter_lines(decode_unicode=True)

def _iter_status(lines):
    yield from _split_voice_servers(lines)
    yield from _split_clients(lines)
    yield from _split_servers(lines)
    yield from _split_prefile(lines)

def _split_to_dict(keys, lines, *, separator=':'):
    for line in lines:
        line = line.strip()
        if line == '' or line[0] == '!':
            return
        values = line.split(separator)
        if len(keys) != len(values):
            logging.info(f'unparseable line {len(keys)} != {len(values)} for {line}')
        values = [key[1](value) if isinstance(key, tuple) else value
                  for key, value in zip(keys, values)]
        keys = [key[0] if isinstance(key, tuple) else key for key in keys]
        yield {key: value for key, value in zip(keys, values)}

def _split_voice_servers(lines):
    keys = (
        'hostname_or_IP',
        'location',
        'name',
        'clients_connection_allowed',
        'type_of_voice_server')
    yield from _split_to_dict(keys, lines)

def _split_clients(lines):
    keys = (
        'callsign',
        'cid',
        'realname',
        'clienttype',
        'frequency',
        ('latitude', float),
        ('longitude', float),
        ('altitude', int),
        ('groundspeed', int),
        'planned_aircraft',
        'planned_tascruise',
        'planned_depairport',
        'planned_altitude',
        'planned_destairport',
        'server',
        'protrevision',
        'rating',
        'transponder',
        ('facilitytype', int),
        'visualrange',
        'planned_revision',
        'planned_flighttype',
        'planned_deptime',
        'planned_actdeptime',
        'planned_hrsenroute',
        'planned_minenroute',
        'planned_hrsfuel',
        'planned_minfuel',
        'planned_altairport',
        'planned_remarks',
        'planned_route',
        ('planned_depairport_lat', float),
        ('planned_depairport_lon', float),
        ('planned_destairport_lat', float),
        ('planned_destairport_lon', float),
        'atis_message',
        'time_last_atis_received',
        'time_logon',
        'heading',
        'QNH_iHg',
        'QNH_Mb')
    yield from _split_to_dict(keys, lines)

def _split_servers(lines):
    keys = (
        'ident',
        'hostname_or_IP',
        'location',
        'name',
        'clients_connection_allowed')
    yield from _split_to_dict(keys, lines)

def _split_prefile(lines):
    keys = (
        'callsign',
        'cid',
        'realname',
        'clienttype',
        'frequency',
        'latitude',
        'longitude',
        'altitude',
        'groundspeed',
        'planned_aircraft',
        'planned_tascruise',
        'planned_depairport',
        'planned_altitude',
        'planned_destairport',
        'server',
        'protrevision',
        'rating',
        'transponder',
        'facilitytype',
        'visualrange',
        'planned_revision',
        'planned_flighttype',
        'planned_deptime',
        'planned_actdeptime',
        'planned_hrsenroute',
        'planned_minenroute',
        'planned_hrsfuel',
        'planned_minfuel',
        'planned_altairport',
        'planned_remarks',
        'planned_route',
        'planned_depairport_lat',
        'planned_depairport_lon',
        'planned_destairport_lat',
        'planned_destairport_lon',
        'atis_message',
        'time_last_atis_received',
        'time_logon',
        'heading',
        'QNH_iHg',
        'QNH_Mb')
    yield from _split_to_dict(keys, lines)
