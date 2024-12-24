import spotify_handler
import playlist_handler
import track

limit = 10
token = spotify_handler.get_token()

def get_item():
    song_or_album = int(input("Enter 1 for song and 2 for album: "))

    query = input("Search? ")
    results = dict()
    if song_or_album == 1:
        # song
        results = spotify_handler.get_song(token, query, limit=limit) 
        for index in range(len(results)):
            item = results[index]
            song_name = item["song_name"]
            album_name = item["album_name"]
            artists = "| "
            for artist in item["artists"]:
                artists += artist + " | "
            print(f"{index + 1}: {song_name} on {album_name} by {artists}")
        option = int(input("Select one: "))
        option -= 1
        chosen_option = results[option]   
        chosen_track = track.Track(
            song_name=chosen_option["song_name"], 
            album_name=chosen_option["album_name"], 
            album_cover=chosen_option["album_cover"], 
            artists=chosen_option["artists"]
        ) 
        return chosen_track.get_track()

    elif song_or_album == 2:
        # album
        results = spotify_handler.get_album(token=token, album=query, limit=limit)
        for index in range(len(results)):
            item = results[index]
            album_name = item["album_name"]
            artists = "| "
            for artist in item["artists"]:
                artists += artist + " | "
            print(f"{index + 1}: {album_name} by {artists}")
        option = int(input("Select one: "))
        option -= 1
        chosen_option = results[option]
        tracks_in_album = list()
        for song_name in chosen_option["tracks"]:
            chosen_track = track.Track(
                song_name=song_name, 
                album_name=chosen_option["album_name"], 
                album_cover=chosen_option["album_cover"], 
                artists=chosen_option["tracks"][song_name]
            )
            tracks_in_album.append(chosen_track.get_track())
        return tracks_in_album
    
item = get_item()
playlists = playlist_handler.Playlists()
playlist_name = playlists.get_playlist_name()
if type(item) is dict:
    playlists.add_track(item, playlist_name)
else:
    for track_obj in item:
        playlists.add_track(track_obj, playlist_name)

playlists.save_playlist()
