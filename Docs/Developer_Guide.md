# PensieveAI Developer's Guide

This document is a technical reference for developers tasked with maintaining or enhancing **PensieveAI**. It includes an overview, technical architecture, implementation details, known issues, and suggestions for future expansions.

---

## Table of Contents
1. [Overview](#overview)
2. [User Interaction Flow](#user-interaction-flow)
3. [Code Flow and Functions](#code-flow-and-functions)
3. [Installation, Deployment, and Admin Details](#installation-deployment-and-admin-details)
4. [Known Issues](#known-issues)
5. [Future Work](#future-work)

---

## Overview

**PensieveAI** is a web-based platform designed to automate thematic analysis of qualitative textual data. By leveraging OpenAI's GPT-4o mini API, the platform identifies themes, descriptions, and relevant excerpts, saving researchers time and effort. The different types of text data used to analyse with this tool are interview transcripts, focus-group transcripts, open-ended survey feedback, customer reviews, etc.
<img width="1424" alt="A screenshot of landing page of PensieveAI where you have to enter a passcode to access the main tool." src="https://github.com/user-attachments/assets/df36bfba-9555-4356-81eb-1c2ab708a8be">

### Target Users
- **Social Science Researchers**: Sociologists, anthropologists, and educators.
- **UX Researchers**: Professionals analyzing user interviews and focus groups.
- **Market Researchers**: Teams reviewing consumer feedback or focus groups.
- **Novice Researchers**: Students and beginners in qualitative research.
- **Businesses**: Organizations analyzing feedback or employee interviews.

### Problem Solved
Manual thematic analysis is time-intensive, prone to human error, and challenging for novice researchers. PensieveAI provides an automated starting point with a preliminary thematic analysis, saving significant time and effort.

### Key Features
- Password-protected access using a single passcode.
- Upload and process multiple file formats: `.pdf`, `.docx`, and `.txt`.
- Option to provide user-defined instructions for customized analysis.
- Integration with OpenAI GPT API for thematic analysis.
- Display results in the UI and allow downloading as PDF reports.

### What's Implemented vs. Initial Specs
The initial specification included thematic analysis, user instructions, handling multiple file formats, OpenAI integration, word limits, PDF export, and secure key management. All these features are currently implemented.

---

## User Interaction Flow

1. **Landing Page (Passcode Entry)**:  
   The user first encounters a passcode entry screen. They input a passcode to gain access. If the passcode is correct, the user is authenticated and redirected to the dashboard.  

2. **Dashboard (File Upload and Analysis)**:  
   Once authenticated, the user sees a dashboard where they can:
   - Upload multiple transcript files (`.txt`, `.docx`, `.pdf`).
   - Provide optional additional instructions in a text area.
   - Initiate the analysis by clicking the "Analyze" button.
   - After they submit, the code processes the files, sends them to the OpenAI API for thematic analysis, and displays the results.
   - The user can then download a PDF report of the analysis.
   - If users click the Logout button, they return to the passcode screen.

## Code Flow and Functions

### Code Flow
1. **User Access (Passcode Entry)**  
   The app starts by displaying a passcode page (`passcode_entry()`). When the user enters the correct passcode, `st.session_state.authenticated` is set to `True`, and the user is rerouted to the main dashboard.

2. **Dashboard Display**  
   If authenticated, `dashboard()` is called. This function shows the file uploader and an optional instruction textbox. The user can upload `.txt`, `.docx`, or `.pdf` transcripts and submit them for analysis.

3. **File Handling**  
   Upon form submission in `dashboard()`, each uploaded file is saved to a temporary directory by `save_uploaded_file()`. `load_transcripts()` then reads and extracts text from each file using `read_txt()`, `read_docx()`, or `read_pdf()`, depending on the file format.

4. **Prompt Generation and Analysis**  
   Once all transcripts are loaded, `generate_prompt()` merges them into a single prompt along with any user instructions. This prompt is sent to the OpenAI API via `analyze_transcripts_with_openai()` to perform the thematic analysis. The resulting analysis is then displayed in the Streamlit UI.

5. **Report Generation**  
   Users can download the thematic analysis results as a PDF. `markdown_to_pdf()` converts the Markdown-formatted response from the OpenAI API into a PDF for easy offline viewing.

In summary, the code flow is: 
**User Authentication → File Upload → Text Extraction → Prompt Creation → OpenAI Analysis → Results Display and PDF Download**

### Functions and Their Roles

1. **`passcode_entry()`**:  
  **Purpose**: Displays the initial passcode input page.   
  **Key Steps**:  
    - Renders HTML/CSS styled UI.
    - Validates user input.
    - If correct, sets `st.session_state.authenticated = True` and triggers a page rerun.

2. **`dashboard()`**:  
  **Purpose**: Main post-authentication interface.  
  **Key Steps**:  
    - Provides file uploader interface.
    - Displays an optional instruction text area.
    - On submission, triggers file handling and analysis process.
    - Shows analysis results and download option.

3. **`save_uploaded_file(uploaded_file, temp_dir)`**:  
  **Purpose**: Writes uploaded files to a temporary directory.  
  **Key Steps**:  
    - Ensures file buffers are saved for subsequent reading.
    - Handles file I/O operations (write mode).

4. **`load_transcripts(folder_path)`**:  
  **Purpose**: Identifies all files in the temp directory and calls the appropriate read functions based on file extension.  
  **Key Steps**:  
    - Iterates through each file.
    - Checks extension: `.txt` -> `read_txt()`, `.docx` -> `read_docx()`, `.pdf` -> `read_pdf()`.
    - Aggregates all transcripts into a list.

5. **`read_txt(file_path)`**, **`read_docx(file_path)`**, **`read_pdf(file_path)`**:  
  **Purpose**: Extracts raw text from respective file formats.  
  **Key Steps**:  
    - Use `open()` for `.txt`.
    - Use `docx.Document()` for `.docx`.
    - Use `PyPDF2.PdfReader()` for `.pdf`.
    - Return the extracted string to be combined later.

5. **`generate_prompt(transcripts, instruction)`**:  
  **Purpose**: Combines all transcripts and optional user instructions into a single prompt string.  
  **Key Steps**:  
    - Iterates through transcripts and concatenates their text.
    - Appends user instructions if provided.
    - Returns a robust prompt for thematic analysis.

6. **`analyze_transcripts_with_openai(prompt)`**:  
  **Purpose**: Sends the prompt to the OpenAI API and receives thematic analysis.  
  **Key Steps**:  
    - Uses the `openai` client to call `chat.completions.create()`.
    - Receives and returns the model’s response.

7. **`markdown_to_pdf(markdown_text)`**:  
  **Purpose**: Converts the returned analysis (in Markdown) to a downloadable PDF.  
  **Key Steps**:  
    - Converts Markdown to HTML via `markdown2`.
    - Uses `xhtml2pdf` (pisa) to generate an in-memory PDF file.
    - Returns the PDF buffer for download.

### File and Module Structure

- All code exists in a single `.py` file (e.g., `app_streamlit.py`). There are no classes or module hierarchies, but the structure is amenable to future refactoring into multiple modules (e.g., a module for file reading, a module for prompt generation and API calls, etc.).
- The `Transcripts` folder has some samples of transcripts from a project I have done in the past. Feel free to use them as sample data to run the application.

### Potential Enhancements

- Introduce object-oriented design by encapsulating transcripts, analysis, and PDF generation into classes.
- Separate UI code (e.g., `dashboard()`, `passcode_entry()`) from logic (file reading and analysis functions).

## Installation, Deployment, and Admin Details
### Prerequisites:
- Python 3.9+ (or a recent version)
- Pip-installed dependencies (`requirements.txt` or `pip install streamlit openai docx PyPDF2 markdown2 xhtml2pdf` and others as listed below)
- Access to OpenAI API with a valid API key

### Dependencies:
- `streamlit` for the web interface
- `openai` for integrating with OpenAI's API
- `docx` (python-docx) for reading `.docx` files
- `PyPDF2` for reading `.pdf` files
- `markdown2` for converting markdown to HTML
- `xhtml2pdf` (pisa) for converting HTML to PDF

### Configuration:
- Place your OpenAI API key in `secrets.toml` file inside `.streamlit` folder (not checked into version control):
- In `secrets.toml` file, `open_ai_api_key="YOUR_API_KEY_HERE"`

Note: This information is explained in detail in the Readme file.

### Deployment
All the details for running the platform locally are in the Readme file. If you wish to deploy the app in the Streamlit community cloud for better access, there are a few more steps involved.
1. **Prepare a GitHub Repository**:  
   - Create a new GitHub repository and push your Streamlit application’s code.

2. **Add Your OpenAI API Key to Streamlit Secrets**:  
   - On your local machine or repository, do not commit the `secrets.toml` with the API key.
   - Instead, go to [Streamlit Community Cloud](https://share.streamlit.io/) and log in.
   - After you create a new app deployment (described below), navigate to **Settings → Secrets** on your Streamlit app page.
   - Add your OpenAI API key as:
     ```
     open_ai_api_key = "YOUR_OPENAI_API_KEY"
     ```

3. **Create a New Streamlit App on Streamlit Cloud**:  
   - From the Streamlit Cloud dashboard, click **Create app**.
   - Select the repository and branch where your code is stored.
   - Specify the Python file that contains your Streamlit code (e.g., `app_streamlit.py`).

4. **Set Up Requirements**:  
   - Streamlit Cloud will automatically install packages listed in `requirements.txt`.
   - Ensure that all dependencies are listed in a `requirements.txt` file. All the dependencies for the current version are in the requirements.txt file. If you make changes to the application, check if that creates new dependencies and update the `requirements.txt` file accordingly.

5. **Deploy the App**:  
   - Click **Deploy**.
   - Streamlit Cloud will build and run your application.
   - Once deployed, you’ll get a unique URL for your app (e.g., `https://your-app-name.streamlit.app`).

6. **Test the Deployment**:  
   - Open the provided URL.
   - You should see your passcode entry page first.
   - Enter the correct passcode to proceed to the dashboard.
   - Upload files and run the analysis as usual.

7. **Update and Redeploy**:  
   - Any time you push new changes to the configured branch of your GitHub repo, Streamlit Cloud will automatically redeploy.
   - Manage secrets, logs, and performance through the Streamlit Cloud dashboard.

**Note**:  
Ensure that your OpenAI usage limits are managed and that you have adequate OpenAI credits or a billing arrangement, as each request made by the app will count towards your OpenAI API quota.

### Admin Notes
- Make sure that secrets.toml is secured and not pushed to any public repository.
- If deploying on a platform like Streamlit Cloud, add the secrets.toml configuration via the platform’s secrets manager.
- Adjust the PASSCODE variable in the code if you need to change the user-facing authentication key.
- The app currently uses 'gpt-4o-mini' as the model. Verify that this model is available on your OpenAI plan or adjust the model name as needed.

## Known Issues
### Minor Issues:
- Some error handling (e.g., unsupported file formats) only prints warnings rather than returning a graceful message to the user.  
  *Fix:* Improve error messaging and handle exceptions more gracefully.

- The user interface styling is somewhat static. Improving CSS or making the app responsive could be desirable but is not critical.

### Major Issues:
- If the user inputs extremely large transcripts exceeding model context limits, the analysis fails.  

### Performance / Scalability:
- The code reads entire transcripts into memory.  
- The analysis can take some time to complete.

## Future Work
- **Chunking Large Transcripts:** Implement logic to handle transcripts in sections and combine partial analyses.
- **Enhanced Analysis:** Allow users to request more focused analyses.
- **User Authentication Upgrade:** Replace the simple passcode with a more robust authentication system.
- **More Formats and Integrations:** Support other text formats (HTML, CSV) or integrate with transcription services.

