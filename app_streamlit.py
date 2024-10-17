import streamlit as st # pip install streamlit --upgrade

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
    st.markdown('<p class="welcome">Welcome to the dashboard! Upload files for analysis:</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Logout button
    logout = st.button("Logout", key="logout")
    if logout:
        st.session_state.authenticated = False
        st.rerun()

    # File uploader section
    st.markdown('<div class="file-uploader">', unsafe_allow_html=True)
    st.subheader("Upload Your Files")
    uploaded_files = st.file_uploader("Choose files to upload", accept_multiple_files=True)
    
    if uploaded_files:
        st.markdown('<div class="file-info">', unsafe_allow_html=True)
        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.read()
            st.write(f"**Filename:** {uploaded_file.name}")
            st.write(f"**File size:** {len(bytes_data)/1024} KB")
            # You can add code here to process the file as needed
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Add handling for other file types as needed


    # Footer
    st.markdown('<div class="footer">© 2024 PensieveAI. All rights reserved.</div>', unsafe_allow_html=True)

# Main application logic
if st.session_state.authenticated:
    dashboard()
else:
    passcode_entry()
