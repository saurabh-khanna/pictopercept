import streamlit as st
import uuid
import time

def stream_data():
    for word in TEXT.split(" "):
        yield word + " "
        time.sleep(0.1)

col1, col2 = st.columns([1, 1])

with col1:
    TEXT = """
    Welcome to PictoPercept! We study human preferences in an increasingly digitized world.
    
    We create choice scenarios, where we can make choices by comparing two images 👀. Try some scenarios out...
    """

    # Initialize user ID and display text
    if "userid" not in st.session_state:
        st.session_state.userid = str(uuid.uuid4())
        st.write(stream_data)
    else:
        st.write(TEXT)
    
    # Create a "Go" button to navigate to the selected page
    if st.button("🎒 Jobs and occupations"):
        st.switch_page("jobs.py")
    if st.button("🤩 Social media icons"):
        st.switch_page("icons.py")
    if st.button("🐙 Non-human species"):
        st.switch_page("species.py")
    if st.button("🦋 Attraction"):
        st.switch_page("attraction.py")
    if st.button("🎞️ Film casts"):
        st.switch_page("filmcast.py")

with col2:
    with st.container(border=True):
        st.image("changeface.gif")