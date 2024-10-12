# data_collector.py

import os
import requests
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import warnings

# Disable SSL-related warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')


load_dotenv()  # Load environment variables from .env file

class DataCollector:
    def __init__(self):
        self.client_id = os.getenv('FITBIT_CLIENT_ID')
        self.client_secret = os.getenv('FITBIT_CLIENT_SECRET')
        self.redirect_uri = 'https://localhost/8501'
        self.token = None
        self.oauth = OAuth2Session(self.client_id, redirect_uri=self.redirect_uri,
                                   scope=["activity", "heartrate", "sleep", "profile"])

    def authorize(self):
        try:
            authorization_url, _ = self.oauth.authorization_url('https://www.fitbit.com/oauth2/authorize')
            print(f'Authorization URL: {authorization_url}')
            print(f'Client ID: {self.client_id}')
            print(f'Redirect URI: {self.redirect_uri}')
            authorization_response = input('Enter the full callback URL: ')
            
            self.token = self.oauth.fetch_token('https://api.fitbit.com/oauth2/token',
                                                authorization_response=authorization_response,
                                                client_secret=self.client_secret,
                                                verify=False)
            return self.token
        except Exception as e:
            print(f"Error during authorization: {e}")
            raise
    
    
    def get_patient_data(self, patient_id):
        """Fetch and return the latest health data for a given patient."""
        if not self.token:
            raise Exception("You need to authorize first. Call authorize() method.")

        try:
            # Fetch heart rate data
            heart_rate_url = 'https://api.fitbit.com/1/user/-/activities/heart/date/today/1d/1min.json'
            heart_rate_response = self.oauth.get(heart_rate_url)
            heart_rate_data = heart_rate_response.json()

            # Fetch steps data
            steps_url = 'https://api.fitbit.com/1/user/-/activities/steps/date/today/1d.json'
            steps_response = self.oauth.get(steps_url)
            steps_data = steps_response.json()

            # Process and return the data
            return {
                'patient_id': patient_id,
                'heart_rate': heart_rate_data,
                'steps': steps_data,
            }

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
        


def test_data_collector():
    collector = DataCollector()
    collector.authorize()
    data = collector.get_patient_data("TEST001")
    if data:
        print("Successfully retrieved data:")
        print(f"Patient ID: {data['patient_id']}")
        print(data)
        print(f"Heart Rate Data Points: {len(data['heart_rate'])}")
        # print(f"Heart Rate Data Points: {len(data['heart_rate']['activities-heart-intraday']['dataset'])}")
        print(f"Steps Today: {data['steps']['activities-steps'][0]['value']}")
    else:
        print("Failed to retrieve data")

if __name__ == "__main__":
    test_data_collector()