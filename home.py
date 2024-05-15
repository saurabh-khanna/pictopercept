import streamlit as st
import pandas as pd
import numpy as np
import uuid
import time
import datetime
import os
import json
from google.cloud import firestore
from google.oauth2 import service_account
import streamlit_analytics2 as streamlit_analytics

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
    "**Supported By** \n\n 🌱 Digital Communication Methods Lab, University of Amsterdam \n\n 🌱 Amsterdam School of Communication Research \n\n Reach out to [saurabh.khanna@uva.nl]() for questions/feedback."
)


# Check if the JSON file exists
if os.path.exists('analytics.json'):
    with open('analytics.json', 'r') as file:
        json_data = file.read()
    data = json.loads(json_data)
    global_responses = data['widgets']['Person 1'] + data['widgets']['Person 2']
    st.sidebar.info(f"Global responses till date: {global_responses}")


st.sidebar.info(
    """**🐙 Team** \n\n [Saurabh Khanna](https://saurabh-khanna.github.io/) \n\n [Irene van Driel](https://www.uva.nl/profiel/d/r/i.i.vandriel/i.i.van-driel.html) \n\n [Sindy Sumter](https://www.uva.nl/en/profile/s/u/s.r.sumter/s.r.sumter.html) \n\n [Chei Billedo](https://www.uva.nl/profiel/b/i/c.j.billedo/c.j.billedo.html) \n\n [Lauren Taylor](https://www.uva.nl/en/profile/t/a/l.n.taylor/l.n.taylor.html) \n\n [Olga Eisele](https://www.uva.nl/profiel/e/i/o.e.eisele/o.e.eisele.html)"""
)

st.write("&nbsp;")

TEXT = """
    Welcome to '📷 PictoPercept'! We study how humans make choices when navigating the internet.

    Today, we show you pictures of two persons at a time, and ask who you might follow on social media. You must choose one person, and their profile picture is the only information you have. Who will you choose?
"""

countries = [
    "Afghanistan",
    "Albania",
    "Algeria",
    "Andorra",
    "Angola",
    "Antigua and Barbuda",
    "Argentina",
    "Armenia",
    "Australia",
    "Austria",
    "Azerbaijan",
    "Bahamas",
    "Bahrain",
    "Bangladesh",
    "Barbados",
    "Belarus",
    "Belgium",
    "Belize",
    "Benin",
    "Bhutan",
    "Bolivia",
    "Bosnia and Herzegovina",
    "Botswana",
    "Brazil",
    "Brunei",
    "Bulgaria",
    "Burkina Faso",
    "Burundi",
    "Côte d'Ivoire",
    "Cabo Verde",
    "Cambodia",
    "Cameroon",
    "Canada",
    "Central African Republic",
    "Chad",
    "Chile",
    "China",
    "Colombia",
    "Comoros",
    "Congo (Congo-Brazzaville)",
    "Costa Rica",
    "Croatia",
    "Cuba",
    "Cyprus",
    "Czechia (Czech Republic)",
    "Democratic Republic of the Congo",
    "Denmark",
    "Djibouti",
    "Dominica",
    "Dominican Republic",
    "Ecuador",
    "Egypt",
    "El Salvador",
    "Equatorial Guinea",
    "Eritrea",
    "Estonia",
    "Eswatini (fmr. Swaziland)",
    "Ethiopia",
    "Fiji",
    "Finland",
    "France",
    "Gabon",
    "Gambia",
    "Georgia",
    "Germany",
    "Ghana",
    "Greece",
    "Grenada",
    "Guatemala",
    "Guinea",
    "Guinea-Bissau",
    "Guyana",
    "Haiti",
    "Holy See",
    "Honduras",
    "Hungary",
    "Iceland",
    "India",
    "Indonesia",
    "Iran",
    "Iraq",
    "Ireland",
    "Israel",
    "Italy",
    "Jamaica",
    "Japan",
    "Jordan",
    "Kazakhstan",
    "Kenya",
    "Kiribati",
    "Kuwait",
    "Kyrgyzstan",
    "Laos",
    "Latvia",
    "Lebanon",
    "Lesotho",
    "Liberia",
    "Libya",
    "Liechtenstein",
    "Lithuania",
    "Luxembourg",
    "Madagascar",
    "Malawi",
    "Malaysia",
    "Maldives",
    "Mali",
    "Malta",
    "Marshall Islands",
    "Mauritania",
    "Mauritius",
    "Mexico",
    "Micronesia",
    "Moldova",
    "Monaco",
    "Mongolia",
    "Montenegro",
    "Morocco",
    "Mozambique",
    "Myanmar (formerly Burma)",
    "Namibia",
    "Nauru",
    "Nepal",
    "Netherlands",
    "New Zealand",
    "Nicaragua",
    "Niger",
    "Nigeria",
    "North Korea",
    "North Macedonia",
    "Norway",
    "Oman",
    "Pakistan",
    "Palau",
    "Palestine State",
    "Panama",
    "Papua New Guinea",
    "Paraguay",
    "Peru",
    "Philippines",
    "Poland",
    "Portugal",
    "Qatar",
    "Romania",
    "Russia",
    "Rwanda",
    "Saint Kitts and Nevis",
    "Saint Lucia",
    "Saint Vincent and the Grenadines",
    "Samoa",
    "San Marino",
    "Sao Tome and Principe",
    "Saudi Arabia",
    "Senegal",
    "Serbia",
    "Seychelles",
    "Sierra Leone",
    "Singapore",
    "Slovakia",
    "Slovenia",
    "Solomon Islands",
    "Somalia",
    "South Africa",
    "South Korea",
    "South Sudan",
    "Spain",
    "Sri Lanka",
    "Sudan",
    "Suriname",
    "Sweden",
    "Switzerland",
    "Syria",
    "Tajikistan",
    "Tanzania",
    "Thailand",
    "Timor-Leste",
    "Togo",
    "Tonga",
    "Trinidad and Tobago",
    "Tunisia",
    "Turkey",
    "Turkmenistan",
    "Tuvalu",
    "Uganda",
    "Ukraine",
    "United Arab Emirates",
    "United Kingdom",
    "United States",
    "Uruguay",
    "Uzbekistan",
    "Vanuatu",
    "Venezuela",
    "Vietnam",
    "Yemen",
    "Zambia",
    "Zimbabwe",
    "Other",
]


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

if "data" not in st.session_state:
    file_paths = ["./data/fairface/label_train.csv", "./data/fairface/label_val.csv"]
    df = pd.concat((pd.read_csv(file) for file in file_paths), ignore_index=True)
    df = df[df["service_test"] == True].drop("service_test", axis=1)
    df = df[~df['age'].isin(['0-2', '3-9', '10-19'])]
    df = df.sample(frac=1).reset_index(drop=True)
    st.session_state.data = df
    st.session_state.index = 0

if "df_demographics" not in st.session_state:
    st.session_state.df_demographics = pd.DataFrame(
        columns=[
            "userid",
            "your_age",
            "your_gender",
            "your_ethnicity",
            "your_nationality",
            "your_socialmedia",
            "your_email",
        ]
    )

if "n_images" not in st.session_state:
    st.session_state["n_images"] = np.nan

# Persistent state to track if the report form should be disabled
if "form_submitted" not in st.session_state:
    st.session_state["form_submitted"] = False

# csv_file_path = "./data/user_selections.csv"

# Choosing images
current_index = st.session_state.index
image1 = "data/fairface/nomargin/" + st.session_state.data.iloc[current_index]["file"]
image2 = (
    "data/fairface/nomargin/" + st.session_state.data.iloc[current_index + 1]["file"]
)

### Main Buttons Display ###

with st.container(border=True):
    col1, col2 = st.columns(2, gap="large")
    with streamlit_analytics.track(load_from_json="analytics.json", save_to_json="analytics.json"):
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

st.write("&nbsp;")

### Report generation ###


# Function to handle form submission
def form_complete():
    if not all(
        [
            st.session_state["age"],
            st.session_state["gender"],
            st.session_state["ethnicity"],
            st.session_state["nationality"],
            st.session_state["email"],
            st.session_state["socialmedia"],
        ]
    ):
        st.toast("Some questions are unanswered!", icon="👀")
    else:
        st.session_state["form_submitted"] = True
        demog_data = {
            "userid": st.session_state.userid,
            "your_age": st.session_state.age,
            "your_gender": st.session_state.gender,
            "your_ethnicity": st.session_state.ethnicity,
            "your_nationality": st.session_state.nationality,
            "your_socialmedia": ", ".join(st.session_state.socialmedia),
            "your_email": st.session_state.email,
        }
        st.session_state.df_demographics = pd.DataFrame([demog_data])


# Toggle widget
enable_form = st.toggle(
    "Wish to receive a free personalized report?",
    value=False,
    disabled=st.session_state["form_submitted"],
)

if enable_form and not st.session_state["form_submitted"]:
    with st.form("user_form"):
        # Use temporary variables to capture input and only save them on submission
        st.info(
            "The more persons you choose above, the more accurate your will report be. You can continue selecting persons even after requesting this report. Your report will be based on all your selections."
        )
        age = st.slider("Your age", min_value=0, max_value=125, step=1, key="age")
        email = st.text_input("Your email", key="email")
        socialmedia = st.multiselect(
            "Social media used (more than one possible)",
            [
                "Facebook",
                "Instagram",
                "Twitter",
                "Snapchat",
                "TikTok",
                "LinkedIn",
                "Pinterest",
                "Reddit",
                "Truth Social",
                "YouTube",
                "WhatsApp",
            ],
            placeholder="Choose one or more options",
            key="socialmedia",
        )
        nationality = st.selectbox(
            "Your nationality", countries, key="nationality", index=None
        )
        gender = st.selectbox(
            "Your gender",
            ["Male", "Female", "Non-binary", "Other"],
            key="gender",
            index=None,
        )
        ethnicity = st.selectbox(
            "Your ethnicity",
            [
                "Black",
                "East Asian",
                "Indian",
                "Latino or Hispanic",
                "Middle Eastern",
                "Southeast Asian",
                "White",
                "Other",
            ],
            key="ethnicity",
            index=None,
        )
        submit_button = st.form_submit_button(
            "Please prepare my report", on_click=form_complete
        )

if st.session_state["form_submitted"]:
    st.info(
        "Thanks! We will work on your report and revert back soon. You can continue making your choices above, and they will all be included in the report."
    )


### Upload images ###

upload_toggle = st.toggle("Wish to help us improve?")
if upload_toggle:
    st.write(
        "Help us improve by uploading one or more images of social media icons you follow."
    )
    imagelist = st.file_uploader(
        "Upload image(s).",
        type=["jpg", "jpeg", "png", "gif", "bmp", "tiff", "svg"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        help="You can choose one or more images to upload.",
    )
    st.session_state["n_images"] = len(imagelist)


### Check for button presses and record the clicks into db ###

# authenticate to Firestore with own credentials
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="pictopercept")

# Firestore collection reference
user_selections_col = db.collection('user_selections')

def write_to_firestore(record):
    """ Function to write a record to Firestore """
    doc_ref = user_selections_col.document()  # Create a new document in Firestore
    doc_ref.set(record)  # Set the document with the data from the record

# Main button click handling and Firestore writing logic
if button1 or button2:
    clicked_values = [1, 0] if button1 else [0, 1]
    current_time = datetime.datetime.now()
    
    # Generate records for Firestore
    for idx, clicked in enumerate(clicked_values):
        if len(st.session_state.df_demographics) > 0:
            demographics_data = {
                "your_age": int(st.session_state.df_demographics.iloc[0]["your_age"]),
                "your_gender": st.session_state.df_demographics.iloc[0]["your_gender"],
                "your_ethnicity": st.session_state.df_demographics.iloc[0]["your_ethnicity"],
                "your_nationality": st.session_state.df_demographics.iloc[0]["your_nationality"],
                "your_socialmedia": ", ".join(st.session_state.df_demographics.iloc[0]["your_socialmedia"].split(",")),
                "your_email": st.session_state.df_demographics.iloc[0]["your_email"],
            }
        else:
            demographics_data = {
                "your_age": np.nan,
                "your_gender": np.nan,
                "your_ethnicity": np.nan,
                "your_nationality": np.nan,
                "your_socialmedia": np.nan,
                "your_email": np.nan,
            }
        record = {
            "file": st.session_state.data.iloc[current_index + idx]["file"],
            "age": st.session_state.data.iloc[current_index + idx]["age"],
            "gender": st.session_state.data.iloc[current_index + idx]["gender"],
            "race": st.session_state.data.iloc[current_index + idx]["race"],
            "clicked": clicked,
            "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "userid": st.session_state.userid,
            "item": (current_index // 2) + 1,
            "form_submitted": st.session_state["form_submitted"],
            "n_images": st.session_state["n_images"],
            **demographics_data
        }
        write_to_firestore(record)
    
    # Move to the next pair of images
    st.session_state.index += 2
    st.rerun()