import streamlit as st
import pandas as pd
import os
from gpt_api import GPT3
import googlemaps
from dotenv import load_dotenv
import numpy as np

load_dotenv()

# Creates the Streamlit app header with information about the product and sets up the user interface
def header():
    st.markdown('<h1>Insurance Automation</h1>', unsafe_allow_html=True)
    st.write("This is a demo of a chatbot using the GPT-3 model that can answer questions and provide insights about given crash report documents.")
    st.write("-------------------------------------------------")
    st.markdown("## How to use this demo")
    st.write("1. Just upload a JPG file of a crash report document")
    st.write("3. Wait for the analysis to complete")
    st.write("3. Receive a summary, image, location, and more info on the document")
    st.write("-------------------------------------------------")
    uploaded_file = st.file_uploader("Choose a JPG file", type="jpg", accept_multiple_files=False)

    return uploaded_file
    
# Creates the Streamlit app template
def page_setup():
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Intro", "Report Summary", "Report Generated Image", "Crash Site", "Data Extraction"])

    with tab1:
        st.markdown("## How does it work?")
        st.markdown("#### Step 1: Data Extraction")
        st.write("The first step is to extract the data from the crash report docment. This task is completed in four parts:")
        st.write("1. The document is segmented into sections using a pretrained model")
        st.write("2. The writing on the document is converted to text using OCR")
        st.write("3. The check boxes are identified and the corresponding sections are extracted")
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

    with tab3:
        st.markdown("## Report Generated Image")

    with tab4:
        st.markdown("## Crash Site")

    with tab5:
        st.markdown("## Data Extraction")        

    return [tab2, tab3, tab4, tab5]

# Runs the app with the given file and begins the data extraction and GPT-3 model
def run(file, tab2, tab3, tab4, tab5):
    # Checks if file has been uploaded
    if file:
        # Runs the model and displays the results in the various tabs
        with st.spinner("Running the model..."):
            save_uploadedfile(file)
            model_gpt = GPT3()
            # Begins the entire pipeline
            model_gpt.generate_report()

        # Tab 2: Report Summary
        with tab2:
            if not model_gpt.full_report == "":
                st.write(model_gpt.full_report)

        # Tab 3: Report Generated Image
        with tab3:
            model_gpt.generate_image()
            st.write("This might be what the crash site could've looked like")
            st.markdown(f"<img src='{model_gpt.image_url}' alt='No Image Found' style='justify-content: center'/>", unsafe_allow_html=True)

        # Tab 4: Crash Site using Google Maps API
        with tab4:
            location = get_location(model_gpt.data)
            st.map(location)

        # Tab 5: Displaying extracted data
        with tab5:
            st.markdown("#### Segmentation & Handwriting Recognition")
            st.image("images/result.jpg")
            st.markdown("#### Check Boxes")
            st.image("images/checkbox_detected.jpg")
            st.markdown("#### Data Output")
            st.write(model_gpt.data)

# Helper function to save the uploaded file
def save_uploadedfile(uploadedfile):
    with open(os.path.join("images", "input_image.jpg"), "wb") as f:
        f.write(uploadedfile.getbuffer())

# Helper function to search longitude and latitude of a location
def search_lat_lng(data):
    lat_lng_list = []
    for location in data:
        lat_lng = location['geometry']['location']
        lat_lng_list.append((lat_lng['lat'], lat_lng['lng']))
    return lat_lng_list

# Helper function to get the location of the crash site using Google Maps API
def get_location(data, gmaps_key=os.environ.get("GOOGLE_MAPS_API_KEY")):
    df = data
    df_lugar = df[df['campo'] == 'lugar']
    address = df_lugar["text"].values[0]

    gmaps = googlemaps.Client(key=gmaps_key)

    location = gmaps.geocode(address)
    loc_data = search_lat_lng(location)
    
    try:
        st.write("This is an approximate location of the crash site")
        return pd.DataFrame({"latitude": [loc_data[0][0]], "longitude":[loc_data[0][1]]})
    except:
        st.write("No location found. Default location is set to Madrid, Spain")
        return pd.DataFrame({"latitude": [40.4637], "longitude": [-3.7492]})

# Runs entire Streamlit app
if __name__ == "__main__":
    file = header()
    tabs = page_setup()
    run(file, tabs[0], tabs[1], tabs[2], tabs[3])