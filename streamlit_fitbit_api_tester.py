import streamlit as st
import requests
import os
import base64
import hashlib
import random
import string
from dotenv import load_dotenv
from urllib.parse import quote, parse_qs, urlparse
from datetime import date, timedelta

# Load environment variables from .env file
load_dotenv()

# Function to generate a code verifier and code challenge
def generate_code_verifier_and_challenge():
    # Generate a random code verifier
    code_verifier = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(43, 128)))
    # Create a SHA-256 hash of the code verifier
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).decode().rstrip('=')
    return code_verifier, code_challenge

# Streamlit app layout
st.title("Fitbit API Tester")

# Generate code verifier and challenge
if 'code_verifier' not in st.session_state:
    code_verifier, code_challenge = generate_code_verifier_and_challenge()
    st.session_state.code_verifier = code_verifier
    st.session_state.code_challenge = code_challenge

st.write(f"Code Verifier: {st.session_state.code_verifier}")
st.write(f"Code Challenge: {st.session_state.code_challenge}")

# Determine the environment
if os.environ.get('ENV') == 'production':
    redirect_uri = 'https://nhs-continews.streamlit.app/'  # Production URI
else:
    redirect_uri = 'http://localhost:8501/'  # Local development URI

client_id = os.getenv('FITBIT_CLIENT_ID')
st.write(f"Client ID: {client_id}")

# Define the scope and URL-encode it
scope = 'activity heartrate location oxygen_saturation temperature'
encoded_scope = quote(scope)

# Request authorization
auth_url = f"https://www.fitbit.com/oauth2/authorize?client_id={client_id}&response_type=code&code_challenge={st.session_state.code_challenge}&code_challenge_method=S256&scope={encoded_scope}&redirect_uri={quote(redirect_uri)}"
st.write("Please authorize the application by clicking the link below:")
st.markdown(f"[Authorize Fitbit]({auth_url})")

# User input for authorization code
st.write("After authorization, please enter the authorization code you received:")
auth_code = st.text_input("Authorization Code")

if st.button("Exchange Code for Tokens"):
    st.write("Button clicked!")  # Debug statement
    if auth_code:
        st.write(f"Attempting to exchange code: {auth_code}")
        
        # Extract the actual code if the full URL was pasted
        parsed_url = urlparse(auth_code)
        if parsed_url.query:
            query_params = parse_qs(parsed_url.query)
            auth_code = query_params.get('code', [auth_code])[0]
        
        # Exchange the authorization code for access and refresh tokens
        token_url = 'https://api.fitbit.com/oauth2/token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'client_id': client_id,
            'grant_type': 'authorization_code',
            'code': auth_code,
            'code_verifier': st.session_state.code_verifier,
            'redirect_uri': redirect_uri,
        }
        
        st.write("Debug: Token Request Details")
        st.write(f"Token URL: {token_url}")
        st.write(f"Headers: {headers}")
        st.write(f"Data: {data}")
        st.write(f"Redirect URI: {redirect_uri}")
        st.write(f"Client ID: {client_id}")
        
        try:
            response = requests.post(token_url, headers=headers, data=data)
            st.write(f"Response status code: {response.status_code}")
            st.write(f"Response content: {response.text}")
            
            if response.status_code == 200:
                tokens = response.json()
                st.success("Successfully obtained tokens!")
                
                # Store access token in session state
                st.session_state.access_token = tokens['access_token']
                
                # Function to make authenticated GET requests
                def authenticated_get(url):
                    headers = {'Authorization': f'Bearer {st.session_state.access_token}'}
                    response = requests.get(url, headers=headers)
                    if response.status_code == 200:
                        return response.json()
                    else:
                        st.error(f"Failed to retrieve data from {url}")
                        st.write(f"Status Code: {response.status_code}")
                        st.write(response.text)
                        return None

                # Get today's date and yesterday's date
                today = date.today().isoformat()
                yesterday = (date.today() - timedelta(days=1)).isoformat()

                # Fetch and display temperature data
                temp_url = f'https://api.fitbit.com/1/user/-/temp/core/date/{yesterday}/{today}.json'
                temp_data = authenticated_get(temp_url)
                if temp_data and 'tempCore' in temp_data:
                    st.subheader("Temperature Data")
                    for day in temp_data['tempCore']:
                        st.write(f"Date: {day['dateTime']}, Temperature: {day['value'].get('nightlyRelative', 'N/A')}°C")
                else:
                    st.write("No temperature data available")

                # Fetch and display activity data
                activity_url = f'https://api.fitbit.com/1/user/-/activities/date/{today}.json'
                activity_data = authenticated_get(activity_url)
                if activity_data and 'summary' in activity_data:
                    st.subheader("Activity Data")
                    summary = activity_data['summary']
                    st.write(f"Steps: {summary.get('steps', 'N/A')}")
                    st.write(f"Calories Burned: {summary.get('caloriesOut', 'N/A')}")
                    st.write(f"Active Minutes: {summary.get('veryActiveMinutes', 'N/A')}")

                # Fetch and display SpO2 data
                spo2_url = f'https://api.fitbit.com/1/user/-/spo2/date/{yesterday}/{today}.json'
                spo2_data = authenticated_get(spo2_url)
                if spo2_data and 'value' in spo2_data:
                    st.subheader("SpO2 Data")
                    for day in spo2_data['value']:
                        st.write(f"Date: {day['dateTime']}, Average: {day['value'].get('avg', 'N/A')}%")

                # Fetch and display breathing rate data
                breathing_url = f'https://api.fitbit.com/1/user/-/br/date/{yesterday}/{today}.json'
                breathing_data = authenticated_get(breathing_url)
                if breathing_data and 'br' in breathing_data:
                    st.subheader("Breathing Rate Data")
                    for day in breathing_data['br']:
                        st.write(f"Date: {day['dateTime']}, Rate: {day['value'].get('breathingRate', 'N/A')} breaths/min")

                # Fetch and display heart rate data
                heart_rate_url = f'https://api.fitbit.com/1/user/-/activities/heart/date/{today}/1d.json'
                heart_rate_data = authenticated_get(heart_rate_url)
                if heart_rate_data and 'activities-heart' in heart_rate_data:
                    st.subheader("Heart Rate Data")
                    for day in heart_rate_data['activities-heart']:
                        if 'value' in day and 'restingHeartRate' in day['value']:
                            st.write(f"Date: {day['dateTime']}, Resting Heart Rate: {day['value']['restingHeartRate']} bpm")

                # Fetch and display HRV data
                hrv_url = f'https://api.fitbit.com/1/user/-/hrv/date/{yesterday}/{today}.json'
                hrv_data = authenticated_get(hrv_url)
                if hrv_data and 'hrv' in hrv_data:
                    st.subheader("HRV Data")
                    for day in hrv_data['hrv']:
                        st.write(f"Date: {day['dateTime']}, Daily RMSSD: {day['value'].get('dailyRmssd', 'N/A')}")
                else:
                    st.write("No HRV data available")

            else:
                st.error(f"Failed to obtain tokens. Status Code: {response.status_code}")
                st.write(response.text)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Display session state for debugging
st.write("Session State:")
st.write(st.session_state)
