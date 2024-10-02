import streamlit as st
import pandas as pd
import uuid
import os
import random
import time
import datetime

# Set up the Streamlit page configuration and hide menu, footer, header

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


# Display title and sidebar information

st.title("📷 PictoPercept")
st.sidebar.title("📷 PictoPercept")
st.sidebar.info(
    "**Supported By** \n\n 🌱 Digital Communication Methods Lab, University of Amsterdam \n\n 🌱 Amsterdam School of Communication Research \n\n Reach out to [saurabh.khanna@uva.nl](mailto:saurabh.khanna@uva.nl) for questions/feedback."
)

st.write("&nbsp;")

TEXT = "Welcome to '📷 PictoPercept'! We study human choices in an increasingly digitized world."


def stream_data():
    for word in TEXT.split(" "):
        yield word + " "
        time.sleep(0.1)


# Initialize user ID and DataFrame if not already in session

if "userid" not in st.session_state:
    st.session_state.userid = str(uuid.uuid4())
    st.write_stream(stream_data)
else:
    st.write(TEXT)

st.write("&nbsp;")

tab1, tab2, tab3, tab4 = st.tabs(["Species", "Occupations", "Icons", "Attractiveness"])

with tab1:
    st.write("&nbsp;")
    st.write(
        "Due to climate change, more than 42000 animal species are in danger of disappearing forever."
    )
    st.write(
        "If you had the power to save one of the two animals shown below, WHO WILL YOU SAVE?"
    )
    st.session_state.index = 0

    image_files = [f for f in os.listdir("data/animals/") if f.endswith("_1.jpg")]
    random.shuffle(image_files)

    # Choosing images
    current_index = st.session_state.index
    image1 = "data/animals/" + image_files[current_index]
    image2 = "data/animals/" + image_files[current_index + 1]

    ### Main Buttons Display ###

    with st.container(border=True):
        col1, col2 = st.columns(2, gap="large")
        with col1:
            button1 = st.button(
                "Animal 1", type="primary", key="btn1_species", use_container_width=True
            )
        with col2:
            button2 = st.button(
                "Animal 2", type="primary", key="btn2_species", use_container_width=True
            )
        col1.image(image1, use_column_width="always")
        col2.image(image2, use_column_width="always")

    ### Check for button presses and record the clicks into some db ###

    # Main button click handling and DB writing logic

    if button1 or button2:
        clicked_values = [1, 0] if button1 else [0, 1]
        current_time = datetime.datetime.now()

        # Generate records for Firestore
        for idx, clicked in enumerate(clicked_values):
            record = {
                "file": st.session_state.data.iloc[current_index + idx]["file"],
                "clicked": clicked,
                "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "userid": st.session_state.userid,
                "item": (current_index // 2) + 1,
            }

        st.session_state.index += 2
        st.rerun()


with tab2:
    st.write("&nbsp;")
    st.write("🚧 Under Construction!")


with tab4:
    st.write("&nbsp;")
    st.write("🚧 Under Construction!")


with tab3:
    st.write("&nbsp;")
    st.write(
        "Today, we show you pictures of two persons at a time, and ask who you might follow on social media. You must choose one person, and their profile picture is the only information you have. Who will you choose?"
    )

    if "data" not in st.session_state:
        file_paths = [
            "./data/fairface/label_train.csv",
            "./data/fairface/label_val.csv",
        ]
        df = pd.concat((pd.read_csv(file) for file in file_paths), ignore_index=True)
        df = df[df["service_test"] == True].drop("service_test", axis=1)
        df = df[~df["age"].isin(["0-2", "3-9", "10-19"])]
        df = df.sample(frac=1).reset_index(drop=True)
        st.session_state.data = df
        st.session_state.index = 0

    # Choosing images
    current_index = st.session_state.index
    image1 = (
        "data/fairface/nomargin/" + st.session_state.data.iloc[current_index]["file"]
    )
    image2 = (
        "data/fairface/nomargin/"
        + st.session_state.data.iloc[current_index + 1]["file"]
    )

    ### Main Buttons Display ###

    with st.container(border=True):
        col1, col2 = st.columns(2, gap="large")
        with col1:
            button1 = st.button(
                "Person 1", type="primary", key="btn1", use_container_width=True
            )
        with col2:
            button2 = st.button(
                "Person 2", type="primary", key="btn2", use_container_width=True
            )
        col1.image(image1, use_column_width="always")
        col2.image(image2, use_column_width="always")

    ### Check for button presses and record the clicks into some db ###

    # Main button click handling and Firestore writing logic
    if button1 or button2:
        clicked_values = [1, 0] if button1 else [0, 1]
        current_time = datetime.datetime.now()

        # Generate records for Firestore
        for idx, clicked in enumerate(clicked_values):
            record = {
                "image_file": st.session_state.data.iloc[current_index + idx]["file"],
                "image_age": st.session_state.data.iloc[current_index + idx]["age"],
                "image_gender": st.session_state.data.iloc[current_index + idx]["gender"],
                "image_race": st.session_state.data.iloc[current_index + idx]["race"],
                "imaged_clicked": clicked,
                "click_timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "userid": st.session_state.userid,
                "item": (current_index // 2) + 1,
            }
            # write_to_firestore(record)

        # Move to the next pair of images
        st.session_state.index += 2
        st.rerun()