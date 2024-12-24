import spotify_handler
import playlist_handler
import track

limit = 5
token = spotify_handler.get_token()

def get_item(song_or_album, query):
    results = dict()
    if song_or_album == "Song":
        # song
        results = spotify_handler.get_song(token, query, limit=limit) 
        results_tracks = {}
        for index in range(len(results)):
            item = results[index]
            song_name = item["song_name"]
            album_name = item["album_name"]
            artists = item["artists"]
            album_cover=item["album_cover"]   
            song = track.Track(song_name, album_name, album_cover, artists).get_track()
            result_num = index + 1
            results_tracks[result_num] = song

        return results_tracks

    elif song_or_album == "Album":
        # album
        results = spotify_handler.get_album(token=token, album=query, limit=limit)
        album_results = {}
        for index in range(len(results)):
            item = results[index]
            album_name = item["album_name"]
            album_artists = item["artists"]
            album_cover = item["album_cover"]
            tracks_in_album = list()
            for song_name in item["tracks"]:
                chosen_track = track.Track(
                song_name=song_name, 
                album_name=album_name, 
                album_cover=album_cover, 
                artists=item["tracks"][song_name]
                )
                tracks_in_album.append(chosen_track.get_track())
            album = track.Album(album_name, album_cover, album_artists, tracks_in_album).get_album()
            result_num = index+1
            album_results[result_num] = album
        return album_results
        
    