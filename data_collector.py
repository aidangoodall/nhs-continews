# data_collector.py

import os
import requests
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import warnings
import streamlit as st

# Disable SSL-related warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')


load_dotenv()  # Load environment variables from .env file

class DataCollector:
    def __init__(self):
        self.client_id = os.getenv('FITBIT_CLIENT_ID')
        self.client_secret = os.getenv('FITBIT_CLIENT_SECRET')
        self.redirect_uri = 'https://nhs-continews.streamlit.app/'
        self.token_url = 'https://api.fitbit.com/oauth2/token'
        self.auth_url = 'https://www.fitbit.com/oauth2/authorize'
        self.scope = ["activity", "heartrate", "sleep", "profile"]

    def get_oauth_session(self):
        return OAuth2Session(self.client_id, redirect_uri=self.redirect_uri, scope=self.scope)

    def authorize(self):
        if 'fitbit_token' not in st.session_state:
            oauth = self.get_oauth_session()
            if 'code' not in st.experimental_get_query_params():
                authorization_url, _ = oauth.authorization_url(self.auth_url)
                st.markdown(f'[Click here to authorize with Fitbit]({authorization_url})')
                st.stop()
            else:
                code = st.experimental_get_query_params()['code'][0]
                try:
                    token = oauth.fetch_token(
                        self.token_url,
                        code=code,
                        client_secret=self.client_secret,
                        include_client_id=True,
                        auth=requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)
                    )
                    st.session_state.fitbit_token = token
                except Exception as e:
                    st.error(f"Error fetching token: {str(e)}")
                    return None
        return st.session_state.fitbit_token

    def get_patient_data(self, patient_id):
        token = self.authorize()
        if not token:
            return None

        headers = {'Authorization': f'Bearer {token["access_token"]}'}
        
        try:
            # Fetch heart rate data
            heart_rate_url = 'https://api.fitbit.com/1/user/-/activities/heart/date/today/1d/1min.json'
            heart_rate_response = requests.get(heart_rate_url, headers=headers)
            heart_rate_data = heart_rate_response.json()

            # Fetch steps data
            steps_url = 'https://api.fitbit.com/1/user/-/activities/steps/date/today/1d.json'
            steps_response = requests.get(steps_url, headers=headers)
            steps_data = steps_response.json()

            return {
                'patient_id': patient_id,
                'heart_rate': heart_rate_data,
                'steps': steps_data,
            }
        except Exception as e:
            st.error(f"Error fetching patient data: {str(e)}")
            return None



def test_data_collector():
    collector = DataCollector()
    token = collector.authorize()
    if token:
        return collector.get_patient_data("TEST001")
    return None
    
if __name__ == "__main__":
    print(test_data_collector())
