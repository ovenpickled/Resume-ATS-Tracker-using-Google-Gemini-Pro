import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() # load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

# The following will be the prompt template

input_prompt="""
I want you to act like a skilled and very experienced ATS(Application Tracking System)
with a deep understanding of the tech field, software engineering, data science, data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider that the job market is very competitive and you should provide 
best assistance for improving the resumes. Assign the percentage matching based 
on Jd and the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"Job Description Match" : "%", "MissingKeywords : []", "Profile Summary" : ""}}
"""

#for streamlit

st.title("Smart ATS 🤖")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload your Resume",type="pdf",help="Please upload the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_response(input_prompt)
        st.subheader(response)