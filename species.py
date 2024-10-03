import streamlit as st
import os
import random
import datetime

st.write("&nbsp;")

st.header("🐙 Non-human species")


st.write(
    "Due to climate change, more than 42000 animal species are in danger of disappearing forever. If you had the power to save one of the two animals shown below, **who will you save**?"
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
if button1 or button2:
    clicked_values = [1, 0] if button1 else [0, 1]
    current_time = datetime.datetime.now()

    # Generate records for Firestore or other databases
    for idx, clicked in enumerate(clicked_values):
        record = {
            "file": image_files[current_index + idx],
            "clicked": clicked,
            "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "userid": st.session_state.userid,
            "item": (current_index // 2) + 1,
        }

    st.session_state.index += 2
    st.rerun()