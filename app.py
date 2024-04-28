# Importing required librabies
from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai


# Loading all the environment variables from .env
load_dotenv()  


# Loading Gemini Pro Vision model
genai.configure(api_key="AIzaSyB8iSqVbUcsOQLi--ghQpCnoyLj2ArDoII")
model = genai.GenerativeModel('gemini-pro-vision')


# Function to generate response for query using Gemini Pro Vision
def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text


# Funtion to preprocess image 
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        iamge_parts = [
            {
                'mime_type' : uploaded_file.type,
                'data' : bytes_data
            }
        ]
        return iamge_parts
    else:
        raise FileNotFoundError("No file uploaded")



# Initialize streamlit app
    
# Title
st.set_page_config(page_title="MultiLanguage Invoice Extractor")
st.header("MultiLanguage Invoice Extractor")

# Inputs
input = st.text_input("Input Prompt: ", key='input')
uploaded_file = st.file_uploader("Choose an image of the invoice...",type=['jpg', 'jpeg', 'png', ])
image = ""

# Display the image
if uploaded_file is not None:
    image  = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

# Creating submit button
submit = st.button("Tell me about the invoice")

# Prompt
input_prompt = """
    You are an expert in understanding invoices. We will upload a image invoice and 
    you will have to answer any questions based on the uploaded invoice image
    """

# If submit button is clicked... (Calling the function to generate response)
if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The Response is")
    st.write(response)