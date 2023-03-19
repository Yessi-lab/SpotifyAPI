import requests

from auth import Auth

base_url = 'https://api.spotify.com/v1/'

auth = Auth()
auth.generate_token()    # use it only for the first time
token = auth.get_token()

headers = {
    'Authorization': f'Bearer {token}',
    "Accept": "application/json"
}

search = requests.utils.quote("album:Blackstar")

params = {
    'type' : "album",
    'q' : search
}

response = requests.get(base_url+"search", headers=headers, params=params)
print(response.json())