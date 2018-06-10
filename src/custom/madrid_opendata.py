import sys
import os.path
import json
import urllib3


_CACHE_DIR = os.getenv('XDG_CACHE_HOME') or os.path.expanduser('~/.cache')
_VR_CACHE_DIR = os.path.join(_CACHE_DIR, 'voice-recognizer')

_MADRID_OPENDATA_CREDENTIALS = (
    os.path.join(_VR_CACHE_DIR, 'madrid_opendata.json')
)


def _load_credentials(credentials_path):
    with open(credentials_path, 'r') as f:
        credentials_data = json.load(f)
        if 'id' in credentials_data and 'pass' in credentials_data:
            return credentials_data['id'], credentials_data['pass']
    
    print('You must define "id" and "pass" attributes.')
    print('Put the value at', credentials_path)
    sys.exit(1)


def _try_to_get_credentials(client_secrets):
    """Try to get credentials, or print an error and quit on failure."""

    if os.path.exists(_MADRID_OPENDATA_CREDENTIALS):
        return _load_credentials(_MADRID_OPENDATA_CREDENTIALS)

    print('You need client secrets to use the Dialogflow API.')
    print('Put the file at', _MADRID_OPENDATA_CREDENTIALS)
    sys.exit(1)


CLIENT_ACCESS_TOKEN = _load_credentials(_MADRID_OPENDATA_CREDENTIALS)
TIMETABLE_URL = 'https://openbus.emtmadrid.es/emt-proxy-server/last/geo/GetArriveStop.php'

def get_timetable_for(id_stop):
    print(id_stop)
    http = urllib3.PoolManager()
    r = http.request(
        'POST',
        TIMETABLE_URL,
        fields={
            'cultureInfo': 'es',
            'idStop': id_stop,
            'idClient': CLIENT_ACCESS_TOKEN[0],
            'passKey': CLIENT_ACCESS_TOKEN[1]
        }
    )
    data = r.data.decode('utf8')
    return json.loads(data)
