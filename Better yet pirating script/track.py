class Track:
    def __init__(self, song_name, album_name, album_cover, artists):
        self.song_name = song_name
        self.album_name = album_name
        self.album_cover = album_cover
        self.artists = artists

    def get_track(self):
        track = {
            "song_name" : self.song_name, 
            "album_name" : self.album_name, 
            "album_cover" : self.album_cover, 
            "artists" : self.artists
        }
        return track
    
class Album:
    def __init__(self, album_name, album_cover, album_artist, tracks):
        self.album_name = album_name
        self.album_cover = album_cover
        self.album_artist = album_artist
        self.tracks = tracks

    def get_album(self):
        album = {
            "album_name" : self.album_name,
            "album_cover" : self.album_cover,
            "album_artist" : self.album_artist,
            "tracks" : self.tracks
        }
        return album

        
