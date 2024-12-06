"""
This Streamlit application, "PensieveAI", provides a user interface for uploading
and analyzing qualitative data using OpenAI's GPT 4o-mini models. Users 
authenticate with a passcode and, upon successful entry, can upload multiple text-based 
files (.txt, .docx, .pdf). The app sends these transcripts to the OpenAI API to identify 
major themes along with excerpts that illuminate these themes.

Features:
- User authentication with a passcode.
- File uploads (txt, docx, pdf).
- Thematic analysis of uploaded transcripts using OpenAI GPT models.
- Custom instructions to guide thematic analysis.
- Display of analysis results and option to download a PDF report.
- Simple word count and file size constraints included.
"""

# import all required packages

import streamlit as st # For web interface and UI elements
from openai import OpenAI 
import docx # For reading .docx files
import PyPDF2  # For reading .pdf files
import markdown2 # For converting Markdown to HTML
from xhtml2pdf import pisa # For converting HTML to PDF
import os
import tempfile
import io
import re


# Set the OpenAI API key from secrets.toml file
open_ai_api_key = st.secrets["open_ai_api_key"]  
# GOTCHA: For st.secrets["key_name"], key_name should match what you have in secrets.toml file


# Set page configuration for Streamlit
st.set_page_config(
    page_title="PensieveAI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Set the secret passcode that users must enter to access the dashboard
PASSCODE = 'Portkey'  

# Initialize session state for tracking authentication status
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Function to display the passcode entry page
def passcode_entry():
    """
    Display the landing page where the user is prompted to enter the passcode.
    
    If the user provides the correct passcode, `authenticated` in the session state is 
    set to True and the dashboard is displayed. Otherwise, an error message is shown.

    The page also includes stylized HTML and CSS for a clean and thematic look.
    """
    
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

    # Page title and description 
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

    # Validate passcode and update session state
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
    """
    Save the uploaded file into a temporary directory.

    Args:
        uploaded_file (UploadedFile): The file object uploaded by the user.
        temp_dir (str): The path to the temporary directory where the file should be saved.
    
    Returns:
        str or None: The directory path if successful, otherwise None.

    """

    try:
        save_path = os.path.join(temp_dir, uploaded_file.name) # Create a full path for the file

        # Write the file to the temporary directory
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return temp_dir # Return the folder path so that all documentes inside it can be read
    except Exception as e:
        st.error(f"Error saving uploaded file in temporary directory'{uploaded_file.name}': {e}")
        return None

# Function to read .txt files
def read_txt(file_path):
    """
    Read the contents of a .txt file.

    Args:
        file_path (str): The path to the .txt file.
    
    Returns:
        str: The contents of the .txt file as a string.
    """

    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
# Function to read .docx files
def read_docx(file_path):
    """
    Read the contents of a .docx file using python-docx.

    Args:
        file_path (str): The path to the .docx file.
    
    Returns:
        str: The combined text of all paragraphs in the .docx file.
    """

    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

# Function to read .pdf files using PyPDF2
def read_pdf(file_path):
    """
    Read the contents of a .pdf file using PyPDF2.

    Args:
        file_path (str): The path to the PDF file.
    
    Returns:
        str: Extracted text content from the entire PDF.
    """

    pdf_text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            pdf_text += page.extract_text()
    return pdf_text

# Function to load multiple transcript files (supporting txt, docx, pdf)
def load_transcripts(folder_path):
    """
    Load transcripts from a folder, reading supported file formats (.txt, .docx, .pdf).

    Args:
        folder_path (str): Path to the folder containing transcript files.
    
    Returns:
        list of str: A list of transcript texts.
    """

    transcripts = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check extension and call corresponding read function
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
    """
    Generate a prompt for the OpenAI API that includes transcripts and user instructions for analysis.
    The prompt will ask the AI to identify major themes, provide descriptions, 
    and include excerpts from participants.

    Args:
        transcripts (list of str): A list of transcripts to be analyzed.
        instruction (str): Additional user-provided instructions for the analysis.
    
    Returns:
        str: A prompt string ready for the OpenAI API.
    """

    prompt = "Here are the transcripts:\n\n"
    
    for i, transcript in enumerate(transcripts):
        prompt += f"Transcript {i+1}:\n{transcript}\n\n"
    
    prompt += "Please provide the major themes along with their descriptions. In each description, include one or more excerpts from participants that align with the theme."
    
    # Include the instruction provided by the user in the prompt to allow customization in analysis
    prompt += instruction

    return prompt

# Function to calculate word count for displaying word count of uploaded text files
def calculate_word_count(text):
    """
    Calculate the word count of a given text.

    Args:
        text (str): The input text.
    
    Returns:
        int: The number of words in the text.
    """

    return len(text.split())

# Define a function that sends prompt to OpenAI API
def analyze_transcripts_with_openai(prompt):
    """
    Send the generated prompt to the OpenAI API for thematic analysis using the "gpt-4o-mini" model.

    Args:
        prompt (str): The prompt containing transcripts and instructions.
    
    Returns:
        str: The text content returned by the OpenAI API, representing the thematic analysis.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[
            {"role": "system", "content": "You are an expert qualitative data analyst. Your task is to analyze the following interview transcripts and identify the major themes along with detailed descriptions."},
            {"role": "user", "content": prompt}
    ],
        temperature=0,  # Controls creativity level foe less random outputs
    )
    return response.choices[0].message.content

# Instantiate a Python API client that configures the environment for communicating with OpenAI api
client = OpenAI(
        api_key=open_ai_api_key
    )

def markdown_to_pdf(markdown_text):
    """
    Convert Markdown text to a PDF file (in-memory).

    Args:
        markdown_text (str): The text content in Markdown format.
    
    Returns:
        BytesIO or None: A bytes buffer object containing the PDF, or None if an error occurred.
    """

    html_body = markdown2.markdown(markdown_text) # Convert markdown to HTML

    # Create a HTML document with custom styles to adjust the font size and styling of PDF output
    html_content = f"""
    <html>
    <head>
    <style>
    body {{
        font-size: 12pt;
        font-family: Arial, sans-serif;
    }}
    h1 {{
        font-size: 18pt;
        font-weight: bold;
    }}
    h2 {{
        font-size: 16pt;
        font-weight: bold;
    }}
    h3 {{
        font-size: 14pt;
        font-weight: bold;
    }}
    h4, h5, h6 {{
        font-size: 12pt;
        font-weight: bold;
    }}
    p {{
        font-size: 12pt;
    }}
    /* Adjust styles for lists */
    ul, ol {{
        font-size: 12pt;
        margin-left: 20px;
    }}
    li {{
        margin-bottom: 5px;
    }}
    /* You can add more styles as needed */
    </style>
    </head>
    <body>
    {html_body}
    </body>
    </html>
    """
    
    # Create an in-memory bytes buffer
    pdf_buffer = io.BytesIO()
    
    # Convert HTML to PDF in-memory
    pisa_status = pisa.CreatePDF(
        src=html_content,  # the HTML to convert
        dest=pdf_buffer  # file handle to receive the result
    )
    
    # Check for conversion errors
    if pisa_status.err:
        return None
    
    # Move the buffer position to the beginning
    pdf_buffer.seek(0)
    
    return pdf_buffer

# Function to display the dashboard page
def dashboard():
    """
    Display the dashboard page where authenticated users can:
    - Upload files for thematic analysis.
    - Enter additional instructions for analysis.
    - View results and download them as a PDF.

    The dashboard includes custom CSS styles for a clean interface.
    """

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
        
    # Header section
    st.markdown('<div class="dashboard-header">', unsafe_allow_html=True)
    st.markdown('<h1>Pensieve<span class="highlight">AI</span> Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="welcome">Unlock the magic within your qualitative data with PensieveAI!<br><br>Just like a wizard&#39;s Pensieve, this platform reveals hidden themes within your data instantly. Not only that, you get rich excerpts for each theme that bring your findings to life. Add your own instructions to personalize the analysis and create a research experience that&#39;s truly magical.<br><br>Read the results here or download a PDF report.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # File uploader section
    st.markdown('<div class="file-uploader">', unsafe_allow_html=True)

    # Create a form to allow multiple file uploads for .txt, .pdf, and .txt files
    with st.form("file_upload_form"):
        uploaded_files = st.file_uploader(
            label="Upload Your Files:",
            key="upload_success",
            accept_multiple_files=True,
            type=['pdf', 'docx', 'txt'],
            #on_change=process_file
        )
        
        # An optional text area for additional user instructions
        instruction = st.text_area("Enter additional instructions (optional):", height=100)

        submit_files = st.form_submit_button("Analyze")

    # Display the maximum word limit for the text files
    st.markdown('<p class="welcome">Total word limit for uploaded text files: 85,000</p>', unsafe_allow_html=True)

    if submit_files:
        if uploaded_files:
            st.markdown('<div class="file-info">', unsafe_allow_html=True)

            # Create a temporary directory for uploaded files
            temp_dir = tempfile.mkdtemp()

            # Process each uploaded file
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

                # Calculate the word count of the prompt
                prompt_word_count = calculate_word_count(prompt)
                
                # Display the prompt word count
                if prompt_word_count <= 85000:
                    st.info(f"{prompt_word_count} words used out of 85,000 word limit.")
                else:
                    st.info(f"{prompt_word_count} words used out of 85,000 word limit. Please keep the word count below 85,000 words.")


                # Display a message indicating that analysis is in progress
                st.info("Analyzing transcripts... Please wait.")


                # Call the OpenAI API
                try:
                    result = analyze_transcripts_with_openai(prompt)
                    st.success("Analysis Complete!")

                    # Print the results
                    st.markdown("### Thematic Analysis Results:")
                    st.markdown(result)

                    # Generate a amrkdown results to PDF
                    pdf_buffer = markdown_to_pdf(result) # convert markdown output from OpenAI to PDF

                    # Provide a download button for the PDF results
                    st.download_button(
                        label="Download Results as PDF",
                        data=pdf_buffer.getvalue(),
                        file_name="analysis_results.pdf",
                        mime="application/pdf"
                    )

                except Exception as e:
                    st.error(f"Error interacting with OpenAI API: {e}")

                    
        else:
            st.warning("Please upload at least one file before submitting.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown('<div class="footer">© 2024 PensieveAI. All rights reserved.</div>', unsafe_allow_html=True)

# Main application flow
if st.session_state.authenticated:
    # If user is authenticated, show the dashboard
    dashboard()
else:
    # Otherwise, show the passcode entry page
    passcode_entry()