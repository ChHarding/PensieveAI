# Description: 
# In this temporary Py file, I will test the interaction between OpenAI API with transcripts in the 'Transcripts' folder.
# This file has functions to read txt, docx, and pdf files: read_txt(), read_docx(), and read_pdf().
# The 'load_transcripts' function uses these functions to create a list of strings that contains text data from each transcript.
# The 'generate_prompt' function appends the individual transcripts that can be sent via OpenAI API
# The 'analyze_transcripts_with_openai' function gives a Qualitative Data Analyst role to 'gpt-4o-mini' model and passes the prompt to analyse the text data

# The next step would be to code that allows a workflow to allow users to upload the text files on the app dashboard, pre-process the files, send suitable prompt with text
# from the transcripts to OpenAI, have the model do thematic analysis on the transcripts, and return the themes in text box or downloadable format.

# import needed modules and functions
import os
from openai import OpenAI # pip install openai on terminal
from keys import open_ai_api_key # import OpenAI Key from keys.py
import docx # pip install python-docx on terminal
import PyPDF2  # pip install PyPDF2 on terminal

# Function to read .txt files
def read_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
# Function to read .docx files
def read_docx(file_path):
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

# Function to read .pdf files using PyPDF2
def read_pdf(file_path):
    pdf_text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            pdf_text += page.extract_text()
    return pdf_text

# Function to load multiple transcript files (supporting txt, docx, pdf)
def load_transcripts(folder_path):
    transcripts = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith(".txt"):
            transcripts.append(read_txt(file_path))
        elif filename.endswith(".docx"):
            transcripts.append(read_docx(file_path))
        elif filename.endswith(".pdf"):
            transcripts.append(read_pdf(file_path))  
        else:
            print(f"Unsupported file format: {filename}")
    return transcripts

# Define function to generate a prompt for thematic analysis
def generate_prompt(transcripts, instruction):
    prompt = "Here are the transcripts:\n\n"
    
    for i, transcript in enumerate(transcripts):
        prompt += f"Transcript {i+1}:\n{transcript}\n\n"
    
    prompt += "Please provide the major themes along with their descriptions. In each description, include one or more excerpts from participants that align with the theme. Also, if any, return any unusual excerpts containing comment from any participant that does not align none of the themes."
    
    # Include the instruction provided by the user in the prompt to allow customization in analysis
    prompt += instruction

    return prompt

# Define a function that sends prompt to OpenAI API for analysis using "gpt-4o-mini"
def analyze_transcripts_with_openai(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Using gpt-4o-mini model for thematic analysis
        messages=[
            {"role": "system", "content": "You are an expert qualitative data analyst. Your task is to analyze the following interview transcripts and identify the major themes along with detailed descriptions."},
            {"role": "user", "content": prompt}
    ],
        max_tokens=16384,  # This is the max limit for token limits
        temperature=0,  # Controls creativity level
    )
    return response.choices[0].message.content

# Instantiate a Python API client that configures the environment for communicating with OpenAI api
client = OpenAI(
        api_key=open_ai_api_key
    )

def main():

    # Create a loop to allow multiple attempts
    while True:
        # Get the folder path from the user
        folder_path = input("Please enter the relative path to the folder containing the transcripts (txt, docx, pdf):")
        # Ask for additional instruction from user to analyze the data
        instruction = input("Enter additional instructions:")

        # Load the transcripts from the folder
        try:
            text = load_transcripts(folder_path)
            if not text:
                print("No valid transcript files found in the folder. Please try again.")
                continue
        except Exception as e:
            print(f"Error loading transcripts: {e}")
            continue

        # Generate a prompt that merges the transcript content
        prompt = generate_prompt(text,instruction)
        #len_prompt = len(prompt)
        #est_tokens = len_prompt/4

        # Print a message to inform the user that the analysis is being performed
        print("Analyzing transcripts... Please wait.")

        # Use OpenAI API to analyze the transcripts
        try:
            result = analyze_transcripts_with_openai(prompt)
            print("\nThematic Analysis Results:\n")
            print(result)
        except Exception as e:
            print(f"Error interacting with OpenAI API: {e}")
            continue

        # Ask if the user wants to process another folder
        retry = input("\nWould you like to analyze more transcripts? (yes/no): ").strip().lower()
        if retry != 'yes':
            print("Exiting. Thank you!")
            break

main()