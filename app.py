import streamlit as st
import openai
from geopy.geocoders import Nominatim

st.markdown('<h1>Insurance Automation</h1>', unsafe_allow_html=True)
st.write("This is a demo of a chatbot using the GPT-3 model that can answer questions and provide insights about given crash report documents.")
st.write("-------------------------------------------------")
st.markdown("## How to use this demo")
st.write("1. Enter your OpenAI API key")
st.write("2. Upload a JPG file of a crash report document")
st.write("3. Open the Report Summary tab and start the analysis")
st.write("3. Receive a summary and analytics of the document")
st.write("-------------------------------------------------")

api= st.text_input("OpenAI API key, How to get it [here](https://platform.openai.com/account/api-keys)", type = "password")
uploaded_file = st.file_uploader("Choose a JPG file", type="jpg")

tab1, tab2, tab3, tab4 = st.tabs(["Intro", "Report Summary", "Crash Site", "Data Extraction"])

flag = False

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
                    <ul>
                    <br />
                    <a href="https://github.com/paches00/insurance-automation"<h4>Github Repo</h4></a>
                """, unsafe_allow_html=True)

with tab2:
    st.markdown("## Report Summary")
    if uploaded_file and api:
        start_analysis = st.button("Start Analysis") 

    # st.write("This is a summary taken from the crash report document")
    # st.write("-------------------------------------------------")

        openai.api_key = api  
        if start_analysis:
            response = openai.Completion.create(
                engine="davinci",
                prompt="This is a prompt",
                temperature=0.9,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.6,
                stop=["\n", " Human:", " AI:"]
            )
            st.write(response["choices"][0]["text"])
            flag = True


with tab3:
    st.markdown("## Crash Site")
    st.write("This is a map of the crash site")
    locator = Nominatim(user_agent="myGeocoder")
    loc_data = locator.geocode("Champ de Mars, Paris, France")
    location = [loc_data.latitude, loc_data.longitude]
    st.map(location)


with tab4:
    st.markdown("## Data Extraction")
    st.markdown("#### Segmentation")
    st.markdown("#### Check Boxes")
    st.markdown("#### Handwritten Text")
    st.markdown("#### Data Aggregation")