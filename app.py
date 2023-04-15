import streamlit as st
import openai
from geopy.geocoders import Nominatim
import pandas as pd
import os
from gpt_api import GPT3
import googlemaps
# from dotenv import load_dotenv

# load_dotenv()

st.markdown('<h1>Insurance Automation</h1>', unsafe_allow_html=True)
st.write("This is a demo of a chatbot using the GPT-3 model that can answer questions and provide insights about given crash report documents.")
st.write("-------------------------------------------------")
st.markdown("## How to use this demo")
st.write("1. Just upload a JPG file of a crash report document")
st.write("3. Open the Report Summary tab and wait for the analysis to complete")
st.write("3. Receive a summary, image, location, and more info on the document")
st.write("-------------------------------------------------")

uploaded_file = st.file_uploader("Choose a JPG file", type="jpg")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Intro", "Report Summary", "Report Generated Image", "Crash Site", "Data Extraction"])

def search_lat_lng(data):
    lat_lng_list = []
    for location in data:
        lat_lng = location['geometry']['location']
        lat_lng_list.append((lat_lng['lat'], lat_lng['lng']))
    return lat_lng_list

def get_location(data):
    df = pd.read_csv(data)
    df_lugar = df[df['campo'] == 'lugar']
    df_localizacion = df[df['campo'] == 'localizacion pais']
    df = pd.concat([df_lugar, df_localizacion])
    address = df["text"].values[0] + ", " + df["text"].values[1]

    gmaps_key = os.getenv("GOOGLE_MAPS_API_KEY")
    gmaps = googlemaps.Client(key=gmaps_key)

    location = gmaps.geocode(address)
    loc_data = search_lat_lng(location)
    
    loc_data = pd.DataFrame({"latitude": [loc_data[1][0]], "longitude":[loc_data[1][1]]})

    return loc_data

with tab1:
    st.markdown("## How does it work?")
    st.markdown("#### Step 1: Data Extraction")
    st.write("The first step is to extract the data from the crash report docment. This task is completed in four parts:")
    st.write("1. The document is segmented into sections using a pretrained model")
    st.write("2. The check boxes are identified and the corresponding sections are extracted")
    st.write("3. The writing on the document is converted to text using OCR")
    st.write("4. Finally, The data from all three models is combined into readable data")
    st.markdown("#### Step 2: Prompt Engineering")
    st.write("The second step is to create a prompt for the GPT-3 model. This is done by combining the extracted data with a prompt template. The template is then given to the model which is capable of highlighting and presenting the output in a concise and standardized manner.")
    st.markdown("#### Step 3: GPT-3")
    st.write("The final step is to pass the prompt to the GPT-3 model. The model will then answer the questions in the prompt. The answers are then displayed to the user.")
    st.write("-------------------------------------------------")
    st.markdown("""<ul>
                        <h4>Contributors:<h4>
                        <a href="https://www.linkedin.com/in/ismael-doukkali/"><li>Ismael Doukkali</li></a>
                        <a href="https://www.linkedin.com/in/bartoszrzycki/"><li>Bartosz Rzycki</li></a>
                        <a href="https://www.linkedin.com/in/juan-jos%C3%A9-rubiales-villegas-31882a1b6/"><li>Juan Rubiales</li></a>
                        <a href="https://www.linkedin.com/in/francisco-heshiki-de-las-casas-46a3491b5/"><li>Francisco Heshiki</li></a>
                        <br />
                        <a href="https://github.com/paches00/insurance-automation"<h4>Github Repo</h4></a>
                    <ul>
                """, unsafe_allow_html=True)
    
with tab2:
    st.markdown("## Report Summary")

if uploaded_file:
    with st.spinner("Running the model, this might take a minute..."):
        model = GPT3("./data_trials/data2.csv", os.environ.get("OPENAI_API_KEY"))
        model.generate_report()

    with tab2:
        
        if not model.report == "" or not model.summary == "":
            st.write(model.full_report)

    with tab3:
        st.markdown("## Report Generated Image")
        start_image = st.button("Start Image Generation")
        if start_image:
            model.generate_image()
            start_image = False
            st.markdown(f"<img src='{model.image_url}' alt='No Image Found' style='justify-content: center'/>", unsafe_allow_html=True)

    with tab4:
        st.markdown("## Crash Site")
        st.write("This is an approximate location of the crash site")

        location = get_location(model.data_path)

        if type(location) == str:
            st.write("No location found for '" + location.upper() + "'")
        else:
            st.map(location)


    with tab5:
        st.markdown("## Data Extraction")
        st.markdown("#### Segmentation")
        st.markdown("#### Check Boxes")
        st.markdown("#### Handwritten Text")
        st.markdown("#### Data Aggregation")