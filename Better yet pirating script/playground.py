import streamlit as st
import download_handler
import os
import set_metadata

playlist = {"Mood":
    {
        "The Search": {
            "song_name": "The Search",
            "album_name": "The Search",
            "album_cover": "https://i.scdn.co/image/ab67616d0000b273942a0c9ac8f1def7c8805044",
            "artists": [
                "NF"
            ]
        },
        "Leave Me Alone": {
            "song_name": "Leave Me Alone",
            "album_name": "The Search",
            "album_cover": "https://i.scdn.co/image/ab67616d0000b273942a0c9ac8f1def7c8805044",
            "artists": [
                "NF"
            ]
        }
    }
}

@st.dialog("Playlist Info")
def open_dialog():
    status_msg = "waiting..."
    can_download = [True, ""]
    downloading = False
    download_button = st.button("Download")
    track_to_download = 0
    list_tracks = []
    playlist_name = "Mood"
    for track_name in playlist[playlist_name]:
        track = playlist[playlist_name][track_name]
        list_tracks.append(track)
    if download_button:
        downloading = True
    if downloading:
        for track in list_tracks:
            if can_download[0]:
                track_details = list_tracks[track_to_download]
                path = os.path.join("Downloads", track_details["song_name"])
                search_term = track_details["song_name"] + track_details["album_name"] + track_details["artists"][0]
                yt_link = download_handler.get_track_ytlink(search_term)
                status_msg = f"Downloading {track_details["song_name"]}"
                st.write(f"{status_msg} : {track_to_download + 1} of {len(list_tracks)}")
                status_msg = download_handler.download_audio(yt_link, path, track_details["song_name"])  
                audio_file = os.path.join("Downloads", f"{track_details["song_name"]}.mp3")
                set_metadata.set_album_cover(audio_file, track_details["album_cover"])
                set_metadata.set_other_fields(audio_file, track_details["song_name"], track_details["artists"], track_details["album_name"])
                st.write(f"{status_msg} : {track_to_download + 1} of {len(list_tracks)}")
            if (track_to_download+1) == len(list_tracks):
                status_msg = f"Downloaded {len(list_tracks)} songs from Mood"
                break
            else:
                track_to_download += 1
        st.write(status_msg)


a = st.button("A", key="a")

if a:
    open_dialog()

