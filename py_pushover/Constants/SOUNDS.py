"""
Sounds - Collection of Push Notification sounds.

This is to be used with the 'sounds' argument of the PushOverManager.push_notification method.

see also: https://pushover.net/api#sounds
"""
from py_pushover._base import  send

_sounds_url = "https://api.pushover.net/1/sounds.json"

SHORT_PUSHOVER = 'pushover'
SHORT_BIKE = 'bike'
SHORT_BUGLE = 'bugle'
SHORT_CASH_REGISTER = 'cashregister'
SHORT_CLASSICAL = 'classical'
SHORT_COSMIC = 'cosmic'
SHORT_GAMELAN = 'gamelan'
SHORT_INCOMING = 'incoming'
SHORT_INTERMISSION = 'intermission'
SHORT_MAGIC = 'magic'
SHORT_MECHANICAL = 'mechanical'
SHORT_PIANO_BAR = 'pianobar'
SHORT_SIREN = 'siren'
SHORT_SPACE_ALARM = 'spacealarm'
SHORT_TUG_BOAT = 'tugboat'
LONG_ALIEN_ALARM = 'alien'
LONG_CLIMB = 'climb'
LONG_PERSISTENT = 'persistent'
LONG_PUSHOVER_ECHO = 'echo'
LONG_UP_DOWN = 'updown'
SILENT = 'none'


class CurrentSounds(object):
    """
    Dynamic class for selecting sounds directly queried from the Pushover Api.
    """
    def __init__(self, app_token):
        res = send(_sounds_url, {'token': app_token})
        for k, v in res['sounds'].items():
            p = v.replace('(', '').replace(')', '').replace(' ', '_')
            setattr(self, p, k)
