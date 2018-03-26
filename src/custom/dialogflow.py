import sys
import os.path
import json
from aiy.i18n import get_language_code

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai


_CACHE_DIR = os.getenv('XDG_CACHE_HOME') or os.path.expanduser('~/.cache')
_VR_CACHE_DIR = os.path.join(_CACHE_DIR, 'voice-recognizer')

_DIALOGFLOW_CREDENTIALS = (
    os.path.join(_VR_CACHE_DIR, 'dialogflow_credentials.json')
)


def _load_credentials(credentials_path):
    with open(credentials_path, 'r') as f:
        credentials_data = json.load(f)
        if 'client_token' in credentials_data:
            return credentials_data['client_token']
    
    print('You must define "client_token" attribute.')
    print('Put the value at', credentials_path)
    sys.exit(1)


def _try_to_get_credentials(client_secrets):
    """Try to get credentials, or print an error and quit on failure."""

    if os.path.exists(_DIALOGFLOW_CREDENTIALS):
        return _load_credentials(_DIALOGFLOW_CREDENTIALS)

    print('You need client secrets to use the Dialogflow API.')
    print('Put the file at', _DIALOGFLOW_CREDENTIALS)
    sys.exit(1)


CLIENT_ACCESS_TOKEN = _load_credentials(_DIALOGFLOW_CREDENTIALS)

def call(query):
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = get_language_code().split('-')[0]
    request.session_id = 'home-pi'
    request.query = query
    response = request.getresponse()
    data = response.read().decode('utf8')
    # data = dumps(response.read().decode()).replace("'", '"')[1:-1]
    return json.loads(data)
