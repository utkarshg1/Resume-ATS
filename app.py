from dotenv import load_dotenv

load_dotenv()

import streamlit as st 
import os 
from PIL import Image
import pdf2image 
import google.generativeai as genai 
import io 
import base64

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):

    if uploaded_file is not None:
        # Convert pdf to image
        images = pdf2image.convert_from_bytes(uploaded_file.read(),poppler_path="poppler-23.11.0/Library/bin")

        first_page = images[0]

        # Convert to bytes
        img_byte_array = io.BytesIO()
        first_page.save(img_byte_array, format='JPEG')
        img_byte_array = img_byte_array.getvalue()

        # pdf parts
        pdf_parts = [
            {
                "mime_type":"image/jpeg",
                "data":base64.b64encode(img_byte_array).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file Uploaded")
    
# Streamlit app
st.set_page_config(page_title="ATS Resume - Utkarsh Gaikwad")
st.header("ATS Resume")
input_text = st.text_area("Job Description : ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF File Uploaded Successfully!")

submit1 = st.button("Tell me about the resume")

submit2 = st.button("Percentage match")

input_prompt1 = """ You are an experience Human Resource Manager with Technology experience in field of Data Science, Full Stack web developer,
                    Big Data Engineering, Data Analyst and Devops. Your task is to review the provided resume against the job description for
                    this profile. Please share your professional evaluation on whether the candidate's profile aligns with the role. 
                    Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements."""

input_propmt2 = """You are a skilled ATS (Application Tracking System) scanner with deep understanding of data science,Full Stack web developer,
                    Big Data Engineering, Data Analyst, Devops and deep ATS functionality. Your task is to evaluate the resume against the provided job description.
                    give me the percentage of match if the resume matches the job description. First the output should come as percentage and 
                    then keywords missing and last final thoughts."""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is : ")
        st.write(response)
    else:
        st.write("Please upload a pdf file of your resume.")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_propmt2, pdf_content, input_text)
        st.subheader("The Response is : ")
        st.write(response)
    else:
        st.write("Please upload a pdf file of your resume.")