## load all the environment variables
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

##Function to load Gemini Pro Vision
model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input_prompt, image_data, text_prompt):
    #content = {"parts": [{"blob": image_data}]}
    response = model.generate_content([input_prompt, image_data[0], text_prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        #Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,    # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
## initialize our streamlit app
st.set_page_config(page_title = "Multi Language Invoice Extractor")

st.header("Multi Language Invoice Extractor")

input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image of the invoice...", type = ["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the invoice")

input_prompt = """
You are an expert in understanding invoices. We will upload an invoice as image and 
you will have to answer any questions based on the uploaded invoice image
"""

## If submit button is clicked
if submit:
    image_data = input_image_details(uploaded_file)
    #print(f"Image data dictionary: {image_data}")
    response = get_gemini_response(input_prompt, image_data, input) 

    st.subheader("The Response is:")
    st.write(response)