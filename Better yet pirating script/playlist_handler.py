import json

class Playlists():
    def __init__(self):
        self.playlists = self.search_for_playlists()

    def search_for_playlists(self):
        try:
            with open("playlists.json", 'r') as infile:
                self.playlists = json.load(infile)
        except json.decoder.JSONDecodeError:
            self.playlists = {}
        return self.playlists
    
    def create_playlist(self, playlist_name):
        if playlist_name in self.playlists or playlist_name.isspace() or playlist_name == "":
            print("Ts alr exist")
        else:
            self.playlists[playlist_name] = {}
            self.save_playlist()
            print("written")
    
    def delete_playlist(self, playlist_name):
        new_playlist_list = {}
        playlist_name_in_playlists = False
        for playlist in self.playlists:
            if playlist_name == playlist:
                playlist_name_in_playlists= True
            else:
                new_playlist_list[playlist] = self.playlists[playlist]
        self.playlists = new_playlist_list
        self.save_playlist()


    def add_track(self, track, playlist):
        if playlist in self.playlists and track['song_name'] not in self.playlists[playlist]:
            tracklist = self.playlists[playlist]
            tracklist[track['song_name']] = track
            self.playlists[playlist] = tracklist
            self.save_playlist()
    
    def remove_track(self, song_name, playlist):
        if playlist in self.playlists and song_name in self.playlists[playlist]:
            new_tracklist = {}
            for track_name in self.playlists[playlist]:
                if not track_name == song_name:
                    new_tracklist[track_name] = self.playlists[playlist][track_name]
            self.playlists[playlist] = new_tracklist 
    
    def save_playlist(self):
        json_dict = json.dumps(obj=self.playlists, indent=4)
        with open("playlists.json", 'w') as outfile:
            outfile.write(json_dict)

    def show_playlist_info(self, playlist):
        return self.playlists[playlist]
    
    def get_playlist_name(self):
        playlist_name = ""
        if self.playlists == {}:
            print("No current playlists. Create one")
            playlist_name = input("Name: ")
            self.create_playlist(playlist_name=playlist_name)
        else:
            print("Choose of the following or make new:")
            for index, name in enumerate(list(self.playlists.keys())):
                print(f"{index + 1}: {name}")
            option = int(input("Choose(or 0 for new playlist): "))
            if option == 0:
                playlist_name = input("Name: ")
                self.create_playlist(playlist_name=playlist_name)
            else:
                option -= 1
                playlist_name = list(self.playlists.keys())[option]
        return playlist_name


        
