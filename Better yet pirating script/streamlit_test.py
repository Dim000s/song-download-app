import streamlit as st
import streamlit_funcs
import playlist_handler
import download_handler
import os
import set_metadata

def main():
    with open('style.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


    playlists, search = st.columns([0.3, 0.7], border=True)

    playlists.write("PLAYLISTS")
    search.write("SEARCH")


    playlists_list = playlist_handler.Playlists()
    playlists_button_dict = {}
    playlist_name_list = []
    for index, playlist in enumerate(playlists_list.playlists):
            playlists_button_dict[index] = playlists.button(label=playlist, use_container_width=True)
            playlist_name_list.append(playlist)
    if len(playlists_list.playlists) == 0:
        playlists.write("No Playlists")

    @st.dialog("Playlist Info")
    def open_playlist_info(playlist_name):
        playlist = playlists_list.playlists[playlist_name]
        delete_button_list = {}
        for count, track in enumerate(playlist):
            col1, col2, col3, col4 = st.columns([0.1, 0.3, 0.3, 0.2])
            with col1:
                st.write(count + 1)
            with col2:
                st.markdown(f"""
                    <strong>{playlist[track]['song_name']}</strong>
                    <br>
                    <sup>{', '.join(playlist[track]['artists'])}</sup>
                    """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <sub>{playlist[track]['album_name']}</sub>
                """, unsafe_allow_html=True)
            with col4:
                delete_button_list[playlist[track]['song_name']] = st.button("➖", key=f"button{count}")
        for track_name in delete_button_list:
            if delete_button_list[track_name]:
                playlists_list.remove_track(track_name, playlist_name)
        status_msg = "waiting..."
        can_download = [True, ""]
        downloading = False
        download_button = st.button("Download", key="download")
        track_to_download = 0
        list_tracks = []
        for track_name in playlist:
            track = playlist[track_name]
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
        

    for i in range(len(playlists_button_dict)):
        playlist_name = playlist_name_list[i]
        if playlists_button_dict[i]:
            open_playlist_info(playlist_name=playlist_name)        


    playlist_name = playlists.text_input("Enter playlist name: ")

    def create_playlist():
        playlists_list.create_playlist(playlist_name)
    def delete_playlist():
        playlists_list.delete_playlist(playlist_name)
    col1, col2, col3 = playlists.columns([1, 1, 1])
    with col1:
        create_playlist_button = col1.button(label="➕", on_click=create_playlist)
    with col3:
        delete_playlist_button = col3.button(label="➖", on_click=delete_playlist)
    with col2:
        pass



    query = search.text_input(value="Search", label="")
    genre = search.radio(options=["Song", "Album"], label="", horizontal=True)

    search.write(f"Displaying results for {query}...")

    results = {}
    try:
        results = streamlit_funcs.get_item(genre, query)
    except KeyError:
        search.write("Type something")

    if genre == "Song":
        for result in results:
            index = result
            song_name = results[index]['song_name']
            album_name = results[index]['album_name']
            artists = ', '.join(results[index]['artists'])
            col1, col2, col3, col4 = search.columns([0.1, 0.4, 0.3, 0.2], vertical_alignment="center")
            with col1:
                st.write(index)
            with col2:
                st.markdown(f"""
                <strong>{song_name}</strong>
                <br>
                <sup>{artists}</sup>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
            <sub>{album_name}</sub>
            """, unsafe_allow_html=True)
            with col4:
                with st.popover("➕"):
                    playlist_to_add = st.text_input("Enter name of playlist:", key=f"text{index}")
                    playlists_list.add_track(track=results[index], playlist=playlist_to_add)
                    if not playlist_to_add == "":
                        playlist_to_add = ""

                
    if genre == "Album":
        for result in results:
            album_name = results[result]["album_name"]
            artists = ", ".join(results[result]["album_artist"])
            tracks = results[result]['tracks']
            col1, col2, col3 = search.columns([0.2, 0.6, 0.2], vertical_alignment="center")
            with col1:
                st.write(result)
            with col2:
                st.markdown(f"""
                <strong>{album_name}</strong>
                <br>
                <sup>{artists}</sup>
                """, unsafe_allow_html=True)
            with col3:
                with st.popover("➕"):
                    playlist_to_add = st.text_input("Enter name of playlist:", key = f"text{result}")
                    for track in tracks:
                        playlists_list.add_track(track, playlist_to_add)


main()