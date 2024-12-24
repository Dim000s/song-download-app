import streamlit as st
import download_handler
import os

@st.dialog("Playlist Info")
def open_dialog():
    status_msg = "waiting..."
    can_download = [True, ""]
    for i in range(5):
        a = i + 1
        col1, col2, col3, col4 = st.columns([0.1, 0.3, 0.3, 0.2])
        with col1:
            st.write(a)
        with col2:
            st.markdown(f"""
                <strong>"sdp interlude"</strong>
                <br>
                <sup>Travis Scott</sup>
                """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <sub>Birds in the Trap Sing McKnight</sub>
            """, unsafe_allow_html=True)
        with col4:
            st.button("➖", key=f"button{i}")
    download_button = st.button("Download")
    if download_button:
        audio_file_name = "BURN"
        path_track = os.path.join("Downloads", audio_file_name)
        track_link = download_handler.get_track_ytlink(track_name="BURN kanye west")
        can_download = [False, path_track]
        status_msg = download_handler.download_audio(track_link, path=path_track)
    if status_msg == f"Downloaded {can_download[1]}":
        can_download = [True, can_download[1]]
    st.write(status_msg)
    st.write(can_download)
    

a = st.button("A", key="a")

if a:
    open_dialog()

