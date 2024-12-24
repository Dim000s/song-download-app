import streamlit as st
import streamlit_funcs
import playlist_handler

with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


playlists, search = st.columns([0.3, 0.7], border=True)

playlists.write("PLAYLISTS")
search.write("SEARCH")

playlists_list = playlist_handler.Playlists()
for playlist in playlists_list.playlists:
        playlists.button(label=playlist, use_container_width=True)
if len(playlists_list.playlists) == 0:
    playlists.write("No Playlists")

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
            st.button("➕", key=f"add_song_{index}")
            

if genre == "Album":
    for result in results:
        album_name = results[result]["album_name"]
        artists = "| "
        for artist in results[result]['album_artist']:
            artists = artists + artist + " | "
        search.button(f"{result}: {album_name} by {artists}", use_container_width=True)
