import openai
import os 
from etl_input import ETLInput
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

class GPT3:

    def __init__(self, data, key=os.environ.get("OPENAI_API_KEY")):
        self.__api_key = key
        self.data_path = data
        self.example = "example_out.txt"
        self.cont = ""
        self.report = ""
        self.summary = ""
        self.image_url = ""
        self.full_report = ""
    
    def generate_response(self, prompt):
        openai.api_key = self.__api_key
        completion=openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'system', "content": str(self.cont)},
                {'role': 'user', 'content': str(prompt)}],
            n=1,
            stop=None,
            temperature=1.0,
        )

        selection = completion.choices[0].message.content

        return selection

    def generate_report(self):
        # Read the data
        with open(self.example, "r") as f:
            example_out = f.read()
        input_file = pd.read_csv(self.data_path)

        # ETL
        data_pre = ETLInput.elt_format_input(input_file)
        input = ETLInput.etl_input_checkbox(data_pre)

        # Report and summary
        self.cont = "Pretend you are an accident report analsyst in charge of performing a review on accident reports. Your objective is to make a full professional report, structured in accident summary, bullet points of each driver, being direct and conlusion and a 300 words detail summary, by no circumstance make up any information. The data you will be provided is in spanish, the variables describe both of the persons involded in the accident as well as information about it. You will deliver a full report in english  as well as a summary. "
        prompt = "You are given 66 features involving the accident, remember the data is given in spanish. Here is the provided data is in json format: " + str(input) + ". Please return the output like the output of the initial example " + str(example_out) + " , stay in the same format as much as possible. Do not make up any information, use the data provided."

        self.full_report = self.generate_response(prompt)

        # Get the report and the summary
        report = self.full_report.split('Summary')[0]
        summary = self.full_report.split('Summary')[1]

        self.report = report
        self.summary = summary

    def generate_image(self):
        # Image generation
        self.cont_img = "Pretend your are an designer to create an image representation of an accident you just saw 100 meters away. Your objective is to make a simple but detailed description of the image being direct and clear. Your return will be given to DAll-E to generate an image. By no circumstance make up any information."
        prompt_img = f'You are given 300 word summary of the accident. Here is the provided data, {self.summary}. Please return a simple description in 20 words mentioning the situation without any personal information. By no circumstance make up any information.'
        
        image_prompt = self.generate_response(prompt_img)

        openai.api_key = self.__api_key
        response = openai.Image.create(
            prompt=image_prompt,
            n=1,
            size="512x512")

        image_url = response['data'][0]['url']

        self.image_url = image_url