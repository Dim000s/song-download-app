import base64
from requests import post, get
import json

client_id = '910f74e8a1d34354838da00ba10cb66d'
client_secret = '975a1acbdb8c45e7883344b2207c62d7'

def get_token():
    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": "Basic " + auth_base64, 
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data =  {"grant_type":"client_credentials"}
    result = post(url=url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token

def get_auth_header(token):
    return {"Authorization":"Bearer " + token}

def get_album(token, album, limit):
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token=token)
    query = f"?q={album}&type=album&limit={limit}"
    query_url = url  + query
    result = get(url=query_url, headers=headers)
    albums_info = dict()
    for x in range(limit):
        json_result = json.loads(result.content)['albums']['items'][x]
        artists = json_result['artists']
        list_artists = []
        for index in range(len(artists)):
            list_artists.append(artists[index]['name'])
        album_info = {
            "album_name": json_result['name'],
            "album_cover": json_result['images'][0]['url'], 
            "artists": list_artists,
            "tracks": get_tracks(token, json_result['id'])
        }
        albums_info[x] = album_info
    return albums_info

def get_tracks(token,album_id):
    url = f'https://api.spotify.com/v1/albums/{album_id}/tracks'
    headers = get_auth_header(token=token)
    result = get(url=url, headers=headers)
    json_result = json.loads(result.content)['items']
    song_names = []
    artist_names = []
    for song in json_result:
        song_names.append(song['name'])
        artist_for_song = []
        for artist in song['artists']:
            artist_for_song.append(artist['name'])
        artist_names.append(artist_for_song)
    tracks_info = dict()
    for number, song in enumerate(song_names):
        tracks_info[song] = artist_names[number]
    return tracks_info

def get_song(token, song, limit):
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token=token)
    query = f"?q={song}&type=track&limit={limit}"
    query_url = url  + query
    result = get(url=query_url, headers=headers)
    albums_info = dict()
    for x in range(limit):
        json_result = json.loads(result.content)['tracks']['items'][x]
        artists = json_result['artists']
        list_artists = []
        for index in range(len(artists)):
            list_artists.append(artists[index]['name'])

        album_info = {
            "song_name": json_result['name'],
            "song_id": json_result['id'], 
            "album_cover": json_result['album']['images'][0]['url'],  
            "album_name": json_result['album']['name'],
            "album_id": json_result['album']['id'],
            "artists": list_artists
        }
        albums_info[x] = album_info
    return albums_info

#token = get_token()
#print(get_song(token, "BURN"))
