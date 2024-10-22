import streamlit as st # pip install streamlit --upgrade
from openai import OpenAI # pip install openai on terminal
from keys import open_ai_api_key # import OpenAI Key from keys.py
import docx # pip install python-docx on terminal
import PyPDF2  # pip install PyPDF2 on terminal
from io import BytesIO

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
            text-align: center;
        }
        .dashboard-header {
            text-align: center;
            padding: 50px 0;
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
            margin-bottom: 40px;
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

    # Header
    st.markdown('<div class="dashboard-header">', unsafe_allow_html=True)
    st.markdown('<h1>Pensieve<span class="highlight">AI</span> Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Logout button
    logout = st.button("Logout", key="logout")
    if logout:
        st.session_state.authenticated = False
        st.rerun()

    # File uploader section
    st.markdown('<div class="file-uploader">', unsafe_allow_html=True)
    #st.subheader("Upload Your Files")

    # Create a form with a submit button
    with st.form("file_upload_form"):
        uploaded_files = st.file_uploader(
            label="Upload Your Files Here:",
            #key="upload_success",
            accept_multiple_files=True,
            type=['pdf', 'docx', 'txt'],
        )
        # Additional instruction input
        instruction = st.text_area("Enter additional instructions (optional):", height=100)
        submit_files = st.form_submit_button("Submit Files")

    if submit_files:
        if uploaded_files:
            st.markdown('<div class="file-info">', unsafe_allow_html=True)
            transcripts = []
            for uploaded_file in uploaded_files:
                file_size_mb = uploaded_file.size / (1024 * 1024)
                st.write(f"**Filename:** {uploaded_file.name}", f"| **File size:** {file_size_mb:.2f} MB")
            
                # Check file size limit (100 MB)
                if file_size_mb > 100:
                    st.error(f"File '{uploaded_file.name}' exceeds the 100 MB size limit and will not be processed.")
                    continue  # Skip processing this file
                else:
                    # Read and process the file
                    if uploaded_file.type == "text/plain":
                        content = read_txt(uploaded_file)
                    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        content = read_docx(uploaded_file)
                    elif uploaded_file.type == "application/pdf":
                        content = read_pdf(uploaded_file)
                    else:
                        st.error(f"Unsupported file format: {uploaded_file.name}")
                        continue
                transcripts.append(content)
        st.markdown('</div>', unsafe_allow_html=True)


        if transcripts:
            # Generate the prompt
            prompt = generate_prompt(transcripts, instruction)
            
            # Display a message to the user
            st.info("Analyzing transcripts... Please wait.")
            
            # Analyze the transcripts using OpenAI API
            try:
                result = analyze_transcripts_with_openai(prompt)
                st.success("Thematic Analysis Results:")
                st.text_area("Results:", result, height=400)
            except Exception as e:
                st.error(f"An error occurred while processing: {e}")
        else:
            st.warning("No valid transcripts were processed.")
    else:
        st.warning("Please upload at least one file before submitting.")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown('<div class="footer">© 2024 PensieveAI. All rights reserved.</div>', unsafe_allow_html=True)

    client = OpenAI(
        api_key=open_ai_api_key
    )

    # Function to read .txt files
    def read_txt(file):
        return file.read().decode('utf-8')

    # Function to read .docx files
    def read_docx(file):
        doc = docx.Document(file)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)

    # Function to read .pdf files using PyPDF2
    def read_pdf(file):
        pdf_text = ""
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            pdf_text += page.extract_text()
        return pdf_text
    
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

if st.session_state.authenticated:
    dashboard()
else:
    passcode_entry()