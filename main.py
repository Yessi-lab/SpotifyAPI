import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred
import requests
import json

def authenticate_spotify_user():
    scope = "user-top-read"
    return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id, client_secret=cred.client_secret, redirect_uri=cred.redirect_url, scope=scope))

def authenticate_spotify_playlist():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id, client_secret=cred.client_secret, redirect_uri=cred.redirect_url))

def user_top_10_artists():
    sp = authenticate_spotify_user()
    results = sp.current_user_top_artists(limit=10, time_range='medium_term')

    top_10_artists = {}
    for idx, item in enumerate(results['items']):
        top_10_artists[idx+1] = item['name']

    return top_10_artists

def user_top_10_songs():
    sp = authenticate_spotify_user()
    results = sp.current_user_top_tracks(limit=10, time_range='medium_term')

    top_songs = {}
    for idx, item in enumerate(results['items']):
        top_songs[idx+1] = item['name']

    return top_songs 

def user_top_10_songs_with_artists():
    sp = authenticate_spotify_user()
    results = sp.current_user_top_tracks(limit=10, time_range='medium_term')

    songs_with_artists = {}

    for idx, item in enumerate(results['items']):
        track_name = item['name']
        artist_name = item['artists'][0]['name']
        songs_with_artists[idx+1] = {'track_name': track_name, 'artist_name': artist_name}
        
    return songs_with_artists

def playlist_cover():
    sp = authenticate_spotify_playlist()
    playlist = sp.playlist_cover_image('https://open.spotify.com/playlist/37i9dQZF1DWWGFQLoP9qlv')
    url_name = playlist[0]['url']
    r = requests.get(url_name, allow_redirects=True)
    open('playlist_cover.jpg', 'wb').write(r.content)

def playlist_followers():
    sp = authenticate_spotify_playlist()
    playlist = sp.playlist('https://open.spotify.com/playlist/37i9dQZF1DWWGFQLoP9qlv')
    
    followers_count = playlist['followers']['total']

    result = {
        "Followers count": followers_count,
    }

    return result

def playlist_audio_features():
    sp = authenticate_spotify_playlist()
    tracks = sp.playlist_tracks('https://open.spotify.com/playlist/37i9dQZF1DWWGFQLoP9qlv')
    tracks_id = [track['track']['id'] for track in tracks['items']]

    tempo_sum = 0
    acousticness_sum = 0
    danceability_sum = 0
    energy_sum = 0
    instrumentalness_sum = 0
    liveness_sum = 0
    loudness_sum = 0
    valence_sum = 0

    for i in range(0, len(tracks_id)):
        audio_features = sp.audio_features(tracks_id[i])
        for track in audio_features:
            if track:
                tempo_sum += track['tempo']
                acousticness_sum += track['acousticness']
                danceability_sum += track['danceability']
                energy_sum += track['energy']
                instrumentalness_sum += track['instrumentalness']
                liveness_sum += track['liveness']
                loudness_sum += track['loudness']
                valence_sum += track['valence']
    
    num_tracks = len(tracks_id)
    tempo_avg = tempo_sum / num_tracks
    acousticness_avg = acousticness_sum / num_tracks
    danceability_avg = danceability_sum / num_tracks
    energy_avg = energy_sum / num_tracks
    instrumentalness_avg = instrumentalness_sum / num_tracks
    liveness_avg = liveness_sum / num_tracks
    loudness_avg = loudness_sum / num_tracks
    valence_avg = valence_sum / num_tracks

    result = {
        "Tempo (BPM)": tempo_avg,
        "Acousticness": acousticness_avg,
        "Danceability": danceability_avg,
        "Energy": energy_avg,
        "Instrumentalness": instrumentalness_avg,
        "Liveness": liveness_avg,
        "Loudness": loudness_avg,
        "Valence": valence_avg
    }

    return result


playlist_cover()

results = {
    "top_10_artists": user_top_10_artists(),
    "top_10_songs": user_top_10_songs(),
    "top_10_songs_with_artists": user_top_10_songs_with_artists(),
    "playlist_followers": playlist_followers(),
    "playlist_audio_features": playlist_audio_features()
}

with open("results.json", "w") as f:
    json.dump(results, f)
