import streamlit as st
import pandas as pd
import datetime
import uuid
import time

st.header("🎞️ Film cast")

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

# Initialize user ID and DataFrame if not already in session
if "userid" not in st.session_state:
    st.session_state.userid = str(uuid.uuid4())

# Initialize responses DataFrame if not already in session
if "responses_df" not in st.session_state:
    st.session_state.responses_df = pd.DataFrame(columns=['userid', 'item', 'file', 'chosen', 'timestamp'])

# State to track if survey has ended
if "survey_ended" not in st.session_state:
    st.session_state.survey_ended = False
    
# Display the responses DataFrame if survey has ended
def survey_ended():
    st.session_state.survey_ended = True

# Initial state to track if consent has been given
if "consent_given_film" not in st.session_state:
    st.session_state.consent_given_film = False

# Consent button
if not st.session_state.consent_given_film and not st.session_state.survey_ended:
    st.write("""
            In this survey, we show you pictures of two persons at a time, and ask who you might cast as the lead character in your film. You must choose one person, and their profile picture is the only information you have.

            1. Choose the person you want by clicking the relevant button.
            2. Answer as fast as you can — try for 5 seconds or less.

            Trust your instincts!
            """)
    st.write("&nbsp;")
    if st.button("Let us begin!", type="primary", use_container_width=False):
        st.session_state.consent_given_film = True
        st.rerun()


if st.session_state.consent_given_film and not st.session_state.survey_ended:
    
    if "data" not in st.session_state:
        # for first run
        file_paths = ["./data/fairface/label_train.csv", "./data/fairface/label_val.csv"]
        df = pd.concat((pd.read_csv(file) for file in file_paths), ignore_index=True)
        df = df[df["service_test"] == True].drop("service_test", axis=1)
        df = df[~df['age'].isin(['0-2', '3-9', '10-19'])]
        df = df.sample(frac=1).reset_index(drop=True)
        st.session_state.data = df[["file"]]
        st.session_state.index = 0
        
    st.write("Imagine you are a filmmaker. Who would you cast as the lead charater in your film?")
    
    ### Choosing images ###

    current_index = st.session_state.index
    image1 = "data/fairface/nomargin/" + st.session_state.data.iloc[current_index]["file"]
    image2 = "data/fairface/nomargin/" + st.session_state.data.iloc[current_index + 1]["file"]
    
    def save_response(selected):
        current_time = datetime.datetime.now()
        st.session_state.responses_df = pd.concat([
            st.session_state.responses_df,
            pd.DataFrame([
                {'userid': st.session_state.userid, 'item': (current_index // 2) + 1, 'file': image1.replace("data/fairface/nomargin/", ""), 'chosen': selected == 1, 'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S")},
                {'userid': st.session_state.userid, 'item': (current_index // 2) + 1, 'file': image2.replace("data/fairface/nomargin/", ""), 'chosen': selected == 2, 'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S")}
            ])
        ], ignore_index=True)
        # next run now!
        st.session_state.index += 2
    
    ### Main Buttons Display ###

    with st.container(border=True):
        col1, col2 = st.columns(2, gap="large")
        with col1:
            button1 = st.button(
                "Person 1", type="primary", key="btn1", on_click=save_response, args=[1], use_container_width=True
            )
        with col2:
            button2 = st.button(
                "Person 2", type="primary", key="btn2", on_click=save_response, args=[2], use_container_width=True
            )
        
        col1.image(image1, use_column_width="always")
        col2.image(image2, use_column_width="always")


    st.write("&nbsp;")
    progress_bar = st.progress(0, text="⏰ Try to answer as fast as you can.")

    ## Exit button ##
    st.write("&nbsp;")    
    button3 = st.button("End survey and view results!", key="btn3", on_click=survey_ended, use_container_width=True)
    
    # Loop from 1 to 5 seconds to update the progress bar
    for i in range(1, 6):
        # Update the progress bar incrementally (each step is 20% progress)
        if i == 1:
            time.sleep(1)
            progress_text = "⏰ Try to answer as fast as you can. Time taken: " + str(i) + " second"
        elif i == 5:
            progress_text = ":red[⏰ Try to answer as fast as you can. Time taken: More than " + str(i) + " seconds!]"
        else:
            progress_text = "⏰ Try to answer as fast as you can. Time taken: " + str(i) + " seconds"
        progress_bar.progress(i * 20, text=progress_text)  # i goes from 1 to 5, converting to percentage (20, 40, ..., 100)
        time.sleep(1)
    
if st.session_state.survey_ended:
    st.header("# Your report")
    st.write("🚧 Work in progress...")
    st.write(st.session_state.responses_df)
    for key in st.session_state.keys():
        if key != "userid":
            del st.session_state[key]
    st.write("&nbsp;")
    if st.button("Retake this survey", type="primary"):
        st.switch_page("filmcast.py")