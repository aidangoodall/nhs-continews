import streamlit as st
import os
import requests
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import warnings
import json

# Disable SSL-related warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# Load environment variables
load_dotenv()

class DataCollector:
    def __init__(self):
        self.client_id = os.getenv('FITBIT_CLIENT_ID')
        self.client_secret = os.getenv('FITBIT_CLIENT_SECRET')
        self.redirect_uri = 'http://localhost:8501/'
        self.token = None
        self.oauth = OAuth2Session(self.client_id, redirect_uri=self.redirect_uri,
                                   scope=["activity", "heartrate", "sleep", "profile"])

    def authorize(self):
        try:
            authorization_url, _ = self.oauth.authorization_url('https://www.fitbit.com/oauth2/authorize')
            st.write(f'Please visit this URL to authorize the application: {authorization_url}')
            authorization_response = st.text_input('Enter the full callback URL:')
            if authorization_response:
                self.token = self.oauth.fetch_token('https://api.fitbit.com/oauth2/token',
                                                    authorization_response=authorization_response,
                                                    client_secret=self.client_secret,
                                                    verify=False)
                return self.token
        except Exception as e:
            st.error(f"Error during authorization: {e}")
            raise

    def get_patient_data(self, patient_id):
        if not self.token:
            st.error("You need to authorize first.")
            return None

        try:
            # Fetch heart rate data
            heart_rate_url = 'https://api.fitbit.com/1/user/-/activities/heart/date/today/1d/1min.json'
            heart_rate_response = self.oauth.get(heart_rate_url)
            heart_rate_data = heart_rate_response.json()

            # Fetch steps data
            steps_url = 'https://api.fitbit.com/1/user/-/activities/steps/date/today/1d.json'
            steps_response = self.oauth.get(steps_url)
            steps_data = steps_response.json()

            return {
                'patient_id': patient_id,
                'heart_rate': heart_rate_data,
                'steps': steps_data,
            }

        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching data: {e}")
            return None

def main():
    # Set page title
    st.set_page_config(page_title="NEWS2 Score Calculator", page_icon="🏥")

    # Add a title
    st.title("Welcome to the NEWS2 Score Calculator")

    # Add some information about NEWS2
    st.write("""
    The National Early Warning Score 2 (NEWS2) is a tool developed by the Royal College of Physicians
    to improve the detection and response to clinical deterioration in adult patients.
    
    This application helps calculate the NEWS2 score based on vital signs data from your Fitbit device.
    """)

    collector = DataCollector()

    if 'authorized' not in st.session_state:
        st.session_state.authorized = False

    if not st.session_state.authorized:
        if st.button("Authorize Fitbit"):
            collector.authorize()
            st.session_state.authorized = True

    if st.session_state.authorized:
        if st.button("Check NEWS Score"):
            patient_id = "TEST001"  # You might want to make this dynamic
            data = collector.get_patient_data(patient_id)
            if data:
                st.success("Successfully retrieved data!")
                st.json(json.dumps(data, indent=2))
                
                # Here you would process the data and calculate the NEWS score
                # For now, we'll just display some basic info
                st.write(f"Patient ID: {data['patient_id']}")
                st.write(f"Steps Today: {data['steps']['activities-steps'][0]['value']}")
                
                # Display heart rate data (this might need adjustment based on the actual data structure)
                if 'activities-heart-intraday' in data['heart_rate']:
                    hr_data = data['heart_rate']['activities-heart-intraday']['dataset']
                    st.write(f"Heart Rate Data Points: {len(hr_data)}")
                    if hr_data:
                        st.write(f"Latest Heart Rate: {hr_data[-1]['value']} bpm")
            else:
                st.error("Failed to retrieve data")

if __name__ == "__main__":
    main()
