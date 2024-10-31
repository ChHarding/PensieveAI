import streamlit as st # pip install streamlit --upgrade
import os
import tempfile
from openai import OpenAI # pip install openai on terminal
from keys import open_ai_api_key # import OpenAI Key from keys.py
import docx # pip install python-docx on terminal
import PyPDF2  # pip install PyPDF2 on terminal

# Set page configuration
st.set_page_config(
    page_title="PensieveAI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Set the secret passcode
PASSCODE = 'Portkey'  # The passcode users must enter

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Function to display the passcode entry page
def passcode_entry():
    # Apply custom CSS styles
    st.markdown(
        """
        <style>
        /* Import the Roboto font */
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');

        body {
            font-family: 'Roboto', sans-serif;
            background-color: #d8cbe5;
            color: #2f023c;
            text-align: center;
            padding: 20px;
        }
        .title {
            font-size: 64px;
            color: #5c538f;
            margin-bottom: 20px;
        }
        .highlight {
            color: #9575cd;
        }
        .description {
            font-size: 14px;
            margin: 0 auto 40px auto;
            max-width: 800px;
            line-height: 1.5;
            color: #2f023c;
            padding: 0 20px;
        }
        
        .instructions {
            font-size: 16px;
            margin-bottom: 20px;
            color: #5c538f;
        }
        .error {
            color: #ff5252;
            margin-bottom: 20px;
            font-weight: bold;
        }
        .footer {
            text-align: center;
            margin-top: 50px;
            color: #2f023c;
            font-size: 14px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Page Title and Description outside the container
    st.markdown('<h1 class="title">✨Pensieve<span class="highlight">AI</span></h1>', unsafe_allow_html=True)
    st.markdown(
        '''
        <p class="description">
            Welcome, Wizard! By leveraging the magic of GenAI, PensieveAI helps qualitative researchers dive deep into their "memories" (data) and uncover hidden patterns, all with the precision and ease of a well-cast spell.
        </p>
        ''',
        unsafe_allow_html=True
    )

    # Instruction for entering the password
    st.markdown('<p class="instructions">⚡️ Prove you are not a muggle to get in the magical world of PensieveAI ⚡️ </p>', unsafe_allow_html=True)

    # Passcode input form
    with st.form("passcode_form"):
        passcode = st.text_input("Enter the passcode:", type="password") # input field
        st.form_submit_button('Submit') #submit button
        st.write("No, 'Alohomora' won't work here!")

    # If passcode is entered, check if it's correct
    if passcode:
        if passcode == PASSCODE:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.markdown('<p class="error">Incorrect password. Please try again.</p>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown('<div class="footer">© 2024 PensieveAI. All rights reserved.</div>', unsafe_allow_html=True)

# Function to save uploaded file in a temporary directory
def save_uploaded_file(uploaded_file, temp_dir):
    try:
        # Create a full path for the file
        save_path = os.path.join(temp_dir, uploaded_file.name)
        # Write the file to the temporary directory
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        #st.success(f"File '{uploaded_file.name}' saved to {temp_dir}")
        #st.success("Upload is successful.")
        
        # Return the folder path so that all documentes inside it can be read
        return temp_dir
    except Exception as e:
        st.error(f"Error saving file '{uploaded_file.name}': {e}")
        return None

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

# Function to display the dashboard page
def dashboard():
    # Apply custom CSS styles
    st.markdown(
        """
        <style>
        /* Import the Roboto font */
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');

        body {
            font-family: 'Roboto', sans-serif;
            background-color: #d8cbe5;
            color: #f0f0f0;
            text-align: left;
        }
        .dashboard-header {
            text-align: center;
            padding: 10px 0;
        }
        h1 {
            font-size: 48px;
            color: #5c538f;
            margin-bottom: 10px;
            text-align: center;
        }
        .highlight {
            color: #9575cd;
        }
        .welcome {
            font-size: 16px;
            color: #2f023c;
            margin-bottom: 20px;
            text-align: center;
        }

        .footer {
            text-align: center;
            margin-top: 50px;
            color: #2f023c;
            font-size: 14px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # Logout button
    logout = st.button("Logout", key="logout")
    if logout:
        st.session_state.authenticated = False
        st.rerun()
        
    # Header
    st.markdown('<div class="dashboard-header">', unsafe_allow_html=True)
    st.markdown('<h1>Pensieve<span class="highlight">AI</span> Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="welcome">Welcome to the dashboard!</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # File uploader section
    st.markdown('<div class="file-uploader">', unsafe_allow_html=True)

    # Create a form with a submit button
    with st.form("file_upload_form"):
        uploaded_files = st.file_uploader(
            label="Upload Your Files:",
            key="upload_success",
            accept_multiple_files=True,
            type=['pdf', 'docx', 'txt'],
            #on_change=process_file
        )
        
        # Input for additional instructions
        instruction = st.text_area("Enter additional instructions (optional):", height=100)

        submit_files = st.form_submit_button("Submit Files")

    if submit_files:
        if uploaded_files:
            st.markdown('<div class="file-info">', unsafe_allow_html=True)

            # Create a temporary directory
            temp_dir = tempfile.mkdtemp()
            #st.info(f"Temporary directory created at {temp_dir}")

            for uploaded_file in uploaded_files:
                bytes_data = uploaded_file.read()
                file_size_mb = len(bytes_data) / (1024 * 1024)
            
                # Check file size limit (200 MB)
                if file_size_mb > 200:
                    st.error(f"File '{uploaded_file.name}' exceeds the 200 MB size limit and will not be processed.")
                    continue  # Skip processing this file

                # Save each uploaded file in a temporary directory
                folder_path = save_uploaded_file(uploaded_file, temp_dir)

                # Reset the file pointer to the beginning
                uploaded_file.seek(0)

                #Display file name and size after upload
                st.write(f"**File name:** {uploaded_file.name}", f"| **File size:** {file_size_mb:.2f} MB")

            st.markdown('</div>', unsafe_allow_html=True)

            # Load transcripts from the temporary directory
            transcripts = load_transcripts(temp_dir)
            if not transcripts:
                st.error("No valid transcript files found in the uploaded files.")
            else:
                # Generate the prompt
                prompt = generate_prompt(transcripts, instruction)
                
                # Display a message indicating that analysis is in progress
                st.info("Analyzing transcripts... Please wait.")

                # Call the OpenAI API
                try:
                    result = analyze_transcripts_with_openai(prompt)
                    st.success("Analysis Complete!")
                    st.markdown("### Thematic Analysis Results:")
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Error interacting with OpenAI API: {e}")
                    
        else:
            st.warning("Please upload at least one file before submitting.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown('<div class="footer">© 2024 PensieveAI. All rights reserved.</div>', unsafe_allow_html=True)

# Main application logic
if st.session_state.authenticated:
    dashboard()
else:
    passcode_entry()