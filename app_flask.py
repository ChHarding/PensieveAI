# Import necessary modules from the Flask framework and the os module
from flask import Flask, request, redirect, render_template, session, url_for
import os

# Create an instance of the Flask application
app = Flask(__name__)

# Set a secret key for the session to enable secure session management
app.secret_key = 'r@ndom'  # I have a question about this, I did put this code based on internet forum and ChatGPT suggestion, but I do not know why this is necessary

# Define the static passcode that users must enter to access the application
PASSCODE = 'Portkey'  # You remember a Portkey from Harry Potter?

# Define the route for the root URL ('/') and specify that it accepts GET and POST methods
@app.route('/', methods=['GET', 'POST'])
def passcode():
    if request.method == 'POST':
        # Retrieve the passcode entered by the user from the form data using request method
        entered_passcode = request.form['passcode']
        # Check if the entered passcode matches the predefined 'PASSCODE'
        if entered_passcode == PASSCODE:
            # If the passcode is correct, set a session variable to indicate the user is authenticate
            session['authenticated'] = True
            # Redirect the user to the main dashboard page
            return redirect(url_for('dashboard'))
        else:
            # If the passcode is incorrect, prepare an error message
            error = "Incorrect password. Please try again."
            # Render the passcode page again and display the error message
            return render_template('passcode.html', error=error)
    # For GET requests, render the passcode entry page
    return render_template('passcode.html')

# Define the route for the dashboard page
@app.route('/dashboard')
def dashboard():
    # Check if the user is authenticated by verifying the session variable
    if session.get('authenticated'):
        # If authenticated, render the dashboard page (main application interface)
        return render_template('dashboard.html')  # Main application interface
    else:
        # If not authenticated, redirect the user back to the passcode entry page
        return redirect(url_for('passcode'))

# Optional, will remove later if does not make sense
# Define the route for logging out
@app.route('/logout')
def logout():
    # Remove the 'authenticated' session variable to log the user out
    session.pop('authenticated', None)
    # Redirect the user back to the passcode entry page
    return redirect(url_for('passcode'))

# Run the application
if __name__ == '__main__':
    # Get the absolute path of the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Change the working directory to the script directory
    os.chdir(script_dir)
    # Start the Flask development server with debugging enabled
    app.run(debug=True)