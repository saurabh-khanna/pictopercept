import streamlit as st
import pandas as pd
import uuid
import time
import os

# Set up the Streamlit page configuration and hide menu, footer, header
st.set_page_config(page_icon="📷", page_title="PictoPercept")
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Display title and sidebar information
st.title("📷 PictoPercept")
st.sidebar.title("📷 PictoPercept")
st.sidebar.info("**Supported By** \n\n 🌱 Digital Communication Methods Lab, University of Amsterdam \n\n 🌱 Amsterdam School of Communication Research \n\n Reach out to [saurabh.khanna@uva.nl]() for questions/feedback.")

st.write("&nbsp;")

TEXT = """
    Welcome to _PictoPercept_!

    Who are you likely to follow on social media? Click either button to choose.
"""

countries = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia",
    "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium",
    "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei",
    "Bulgaria", "Burkina Faso", "Burundi", "Côte d'Ivoire", "Cabo Verde", "Cambodia", "Cameroon", "Canada",
    "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo (Congo-Brazzaville)",
    "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czechia (Czech Republic)", "Democratic Republic of the Congo",
    "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador",
    "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini (fmr. Swaziland)", "Ethiopia", "Fiji", "Finland",
    "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea",
    "Guinea-Bissau", "Guyana", "Haiti", "Holy See", "Honduras", "Hungary", "Iceland", "India", "Indonesia",
    "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya",
    "Kiribati", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya",
    "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali",
    "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco",
    "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar (formerly Burma)", "Namibia", "Nauru", "Nepal",
    "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia",
    "Norway", "Oman", "Pakistan", "Palau", "Palestine State", "Panama", "Papua New Guinea", "Paraguay",
    "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis",
    "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe",
    "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia",
    "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka",
    "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste",
    "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda",
    "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu",
    "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
]


def stream_data():
    for word in TEXT.split(" "):
        yield word + " "
        time.sleep(0.1)

# Initialize user ID and DataFrame if not already in session
if 'userid' not in st.session_state:
    st.session_state.userid = str(uuid.uuid4())
    st.write_stream(stream_data)
else:
    st.write(TEXT)

st.write("&nbsp;")

if 'data' not in st.session_state:
    df = pd.read_csv("./data/fairface/label_train.csv")
    df = df[df['service_test'] == True].drop('service_test', axis=1)
    df = df[~df['age'].isin(['0-2', '3-9', '10-19'])].sample(frac=1).reset_index(drop=True)
    st.session_state.data = df
    st.session_state.index = 0

csv_file_path = "./data/user_selections.csv"

# Show images
current_index = st.session_state.index
image1 = "data/fairface/nomargin/" + st.session_state.data.iloc[current_index]['file']
image2 = "data/fairface/nomargin/" + st.session_state.data.iloc[current_index + 1]['file']

col1, col2 = st.columns(2, gap="large")

with col1:
    button1 = st.button("Person 1", type = "primary", key="1", use_container_width = True)
    st.image(image1, use_column_width="always")
with col2:
    button2 = st.button("Person 2", type = "primary", key="2", use_container_width = True)
    st.image(image2, use_column_width="always")

# Check for button presses and record the clicks
if button1 or button2:
    clicked_values = [1, 0] if button1 else [0, 1]
    st.session_state.data.loc[current_index, 'clicked'] = clicked_values[0]
    st.session_state.data.loc[current_index+1, 'clicked'] = clicked_values[1]
    
    st.session_state.data.loc[current_index:current_index+1, 'userid'] = st.session_state.userid
    st.session_state.data.loc[current_index:current_index+1, 'item'] = (current_index // 2) + 1
    
    selected_data = st.session_state.data.iloc[current_index:current_index+2]
    selected_data.to_csv(csv_file_path, mode='a', header=not os.path.exists(csv_file_path), index=False)

    # Move to the next pair of images
    st.session_state.index += 2
    st.rerun()




st.write("&nbsp;")
# Persistent state to track if the form should be disabled
if 'form_submitted' not in st.session_state:
    st.session_state['form_submitted'] = False

# Toggle widget
enable_form = st.toggle("Wish to generate a personal report? _[Note: More persons selected → More accurate reports]_", value=False, disabled=st.session_state['form_submitted'])

# Function to handle form submission
def form_complete():
    if not all([st.session_state['age'], st.session_state['gender'], st.session_state['ethnicity'], st.session_state['nationality']]):
        st.toast("Some questions are unanswered...", icon='👀')
    else:
        st.session_state['form_submitted'] = True
    
if enable_form and not st.session_state['form_submitted']:
    with st.form("user_form"):
        # Use temporary variables to capture input and only save them on submission
        gender = st.selectbox("Your Gender", ["Male", "Female", "Non-binary", "Other"], key='gender', index=None)
        ethnicity = st.selectbox("Your Ethnicity", ["Black", "East Asian", "Indian", "Latino or Hispanic", "Middle Eastern", "Southeast Asian", "White", "Other"], key='ethnicity', index=None)
        nationality = st.selectbox("Your Nationality", countries, key='nationality', index=None)
        age = st.slider("Your Age", min_value=0, max_value=125, step=1, key='age')
        submit_button = st.form_submit_button("Generate report", on_click=form_complete)

if st.session_state['form_submitted']:
    with st.container(border=True):
        st.write("Report is generated here.")
        df_report = st.session_state.data
        df_report = df_report[df_report['clicked'] == 1]
        st.bar_chart(df_report['gender'].value_counts())
        st.bar_chart(df_report['race'].value_counts())
        st.bar_chart(df_report['age'].value_counts())


st.write("&nbsp;")
st.write("&nbsp;")
st.write("&nbsp;")
st.write("&nbsp;")
with st.expander("For internal use"):
    st.write(st.session_state.data)
    # st.write(st.session_state.data.iloc[current_index:current_index+2])
