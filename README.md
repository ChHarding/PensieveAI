# PensieveAI
Pensieve AI is a web-based platform that leverages OpenAI's GPT-4o mini API designed to automate thematic analysis of qualitative textual data. Users can upload their text files and view thematic analysis results. Users can also provide additional instructions for analyzing the data and download thematic analysis results as a PDF using the tool.

## For Qualitative Researchers 
If you are a qualitative researcher who only wants to use the tool and not replicate it yourself, you can use it via [PensieveAI](https://pensieve.streamlit.app/). 

_Disclaimer, if this app had not been active for a long time, it takes a few minutes to open the app. Please be patient if that happens._

### Login Page
<img width="1424" alt="A screenshot of landing page of PensieveAI where you have to enter a passcode to access the main tool." src="https://github.com/user-attachments/assets/df36bfba-9555-4356-81eb-1c2ab708a8be">

You have to enter a passcode on this landing page to access the main tool. The passcode is `Portkey`.

### Main Dashboard
<img width="1424" alt="Screenshot that shows main dashboard page" src="https://github.com/user-attachments/assets/28377ba9-07c8-4338-8ba1-894fbf9dee4d">

### Upload Files
<img width="1424" alt="Screenshots for uploading file" src="https://github.com/user-attachments/assets/c2bb3472-aac1-4ea1-96bc-675a9491bb55">

You can upload multiple text files in PDF, DOCX, and TXT formats. The maximum number of total words in the documents should be 85,000.

### Optional: Add Instructions
<img width="1424" alt="Screenshot of additional instructions form" src="https://github.com/user-attachments/assets/1a1aa7fa-0190-4a79-a720-d943e9441107">

While you can get thematic analysis for your uploaded data directly, you can also provide additional instructions to customize your analysis e.g., using a theoretical framework.

### Results
<img width="1424" alt="Screenshot of displayed results" src="https://github.com/user-attachments/assets/58ee0fd5-d76b-4385-bacc-d5e177706145">

The results will contain the description of the emergent themes and examples of excerpts for each theme.

### Download PDF Version
<img width="1424" alt="Screenshot to download the pdf" src="https://github.com/user-attachments/assets/85fe51e9-1945-4ade-a410-e18406e249d9">

Download the PDF version to save it for future reference.

## For Developers

### Before You Start: Setup OpenAI API Key
#### Get OpenAI API Key
The tool uses OpenAI API to analyze the text data, so you should first sign up for an OpenAI API key. There are no free ways of doing this (at least at present). However, a $5 credit goes a long way if you're utilizing the GPT-4o mini model. If you haven't done it yet, please refer to [this tutorial](https://medium.com/@lorenzozar/how-to-get-your-own-openai-api-key-f4d44e60c327).

<img width="1424" alt="image" src="https://github.com/user-attachments/assets/f281f7c1-060f-4ad2-a3c2-02631d7501aa">

#### Make a Secrets.toml file
![secrets_toml](https://github.com/user-attachments/assets/1eec1bd0-51bf-4647-be6f-df5c12c8f902)
Under a folder `.streamlit`, add a `secrets.toml` file and assign your API key to a variable.

Disclaimer🔴: You must make sure this file is added to your .gitignore file.
<img width="1438" alt="image" src="https://github.com/user-attachments/assets/f087fd0b-c7b2-47c1-9cf9-9fb123c03e86">

Find more information on [Streamlit Documentation](https://docs.streamlit.io/develop/concepts/connections/secrets-management).

### Extract the API Key on Main App File
Make sure to match variable name for API key on secrets.toml file when you extract the key on main app file. e.g., "open_ai_api_key".
<img width="1178" alt="image" src="https://github.com/user-attachments/assets/169c3d13-3e83-4c2b-a286-25cf2686b3d7">

### Install Pre-requisite Packages
I am currently using on Python code (3.12 version) for the application. Make sure you have the latest version of Python installed on your device. If you don't have Python installed already, download from [here](https://www.python.org/downloads/). Then, download the non-standard python packages that are required to run app_streamlit.py.

On your terminal, run the `pip install --upgrade -r requirements.txt` command.

<img width="1435" alt="image" src="https://github.com/user-attachments/assets/c9f881c7-4044-4e31-bcf0-ef4cf196b992">

### Run App Locally
Now, to run the app locally, use command `streamlit run app_streamlit.py` on the terminal.
<img width="1435" alt="image" src="https://github.com/user-attachments/assets/27c95d7d-3bc5-4f9a-9381-c28b3f9a5e12">

This command will open the app on your local host.
![image](https://github.com/user-attachments/assets/c9b425e8-a39d-4261-80d7-128f22fbbb16)

Congratulations! Now, you have your own qualitative data analyzer. If you want to customize the tool for yourself and want to get yourself familiar with the code, check the Developer's documentation.
<br>
If you need guidance in using the app, go to the top of this Readme file and view directions for qualitative researchers.
