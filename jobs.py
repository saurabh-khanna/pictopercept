import streamlit as st
import pandas as pd
import datetime
import uuid

st.header("🎒 Jobs and occupations")

import random

# List of non-gendered occupations
occupations = ['a doctor', 'a lawyer', 'a nurse', 'an author', 'a teacher', 'an engineer', 'a scientist', 'a chef', 'an artist', 'an architect', 'a pilot', 'a journalist', 'a dentist', 'a therapist', 'an accountant', 'a musician', 'a designer', 'a programmer', 'a pharmacist', 'a plumber', 'an electrician', 'a librarian', 'an analyst', 'a consultant', 'an entrepreneur', 'a researcher', 'a technician', 'an editor', 'a translator', 'a veterinarian', 'a social worker', 'a photographer']

random_occupation = str(random.choice(occupations))

st.write("Who of these is **" + random_occupation + "**?")

if "userid" not in st.session_state:
    st.session_state.userid = str(uuid.uuid4())

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
    
# # Choosing images
imagetuple = random.sample(range(len(st.session_state.data)), 2)

image1_job = "data/fairface/nomargin/" + st.session_state.data.iloc[imagetuple[0]]["file"]
image2_job = "data/fairface/nomargin/" + st.session_state.data.iloc[imagetuple[1]]["file"]

### Main Buttons Display ###

with st.container(border=True):
    col1, col2 = st.columns(2, gap="large")
    with col1:
        button1 = st.button(
            "Person 1", type="primary", key="btn1_job", use_container_width=True
        )
    with col2:
        button2 = st.button(
            "Person 2", type="primary", key="btn2_job", use_container_width=True
        )
    col1.image(image1_job, use_column_width="always")
    col2.image(image2_job, use_column_width="always")

### Check for button presses and record the clicks into some db ###
if button1 or button2:
    clicked_values_job = [1, 0] if button1 else [0, 1]
    current_time = datetime.datetime.now()

    # Generate records for DB
    for idx, clicked in enumerate(clicked_values_job):
        record = {
            "image_file": st.session_state.data.iloc[imagetuple[idx]]["file"],
            "image_age":st.session_state.data.iloc[imagetuple[idx]]["age"],
            "image_gender": st.session_state.data.iloc[imagetuple[idx]]["gender"],
            "image_race": st.session_state.data.iloc[imagetuple[idx]]["race"],
            "imaged_clicked": clicked,
            "click_timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "userid": st.session_state.userid,
            # "item": (current_index // 2) + 1,
        }

    st.rerun()
