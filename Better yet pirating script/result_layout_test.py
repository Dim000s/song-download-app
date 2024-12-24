import streamlit as st

st.markdown("""<style>.stColumn{
    text-align: center;
}</style>""", unsafe_allow_html=True)


col1, col2, col3, col4 = st.columns([0.1, 0.4, 0.3, 0.2])
with col1:
    st.write("1")
with col2:
    st.markdown("""
    <strong>BURN</strong>
    <br>
    <sup>YE, Kanye West, Ty Dolla Sign</sup>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
<sub>VULTURES 1</sub>
""", unsafe_allow_html=True)
with col4:
    st.button("➕", key="temp")