import json
import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")
playlist_id = os.getenv("PLAYLIST_ID")
scope="playlist-modify-private, playlist-modify-public,user-library-read"

def get_playlist(spotipy_client_id, spotipy_client_secret, spotipy_redirect_uri, scope):
    sp = Spotify(
        auth_manager=SpotifyOAuth(
            client_id=spotipy_client_id,
            client_secret=spotipy_client_secret,
            redirect_uri=spotipy_redirect_uri,
            scope=scope
        )
    )

    results = sp.current_user_saved_tracks()
    tracks = results['items']

    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    track_list = []
    track_uris = []
    for track in tracks:
        x = track['track']
        track_info = {
            "id": x['id'],
            "uri": x['uri'],
            "artist": x['artists'][0]['name'],
            "name": x['name']
        }
        track_list.append(track_info)
        track_uris.append(x['uri'])

    with open('output.json', 'w') as f:
        json.dump(track_list, f, indent=4)

    for i in range(0, len(track_uris), 100):
        chunk = track_uris[i:i + 100]
        sp.playlist_add_items(playlist_id, chunk)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_playlist(spotipy_client_id=client_id, spotipy_client_secret=client_secret,
                 spotipy_redirect_uri=redirect_uri, scope=scope)
    