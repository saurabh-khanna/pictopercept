import streamlit as st

# Set up the Streamlit page configuration and hide the menu, footer, and header
st.set_page_config(page_icon="📷", page_title="PictoPercept", layout="centered")

st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📷 PictoPercept")
st.write("&nbsp;")

home_page = st.Page("home.py", title="Home")
jobs_page = st.Page("jobs.py", title="Jobs and occupations", icon="🎒")
icons_page = st.Page("icons.py", title="Social media icons", icon="🤩")
species_page = st.Page("species.py", title="Non-human species", icon="🐙")
attraction_page = st.Page("attraction.py", title="Attraction", icon="🦋")
filmcast_page = st.Page("filmcast.py", title="Film cast", icon="🎞️")

pg = st.navigation([home_page, jobs_page, icons_page, species_page, attraction_page, filmcast_page])

st.sidebar.info(
    "**Supported By** \n\n 🌱 Digital Communication Methods Lab, University of Amsterdam \n\n 🌱 Amsterdam School of Communication Research \n\n Reach out to [saurabh.khanna@uva.nl](mailto:saurabh.khanna@uva.nl) for questions/feedback/collaboration."
)

pg.run()