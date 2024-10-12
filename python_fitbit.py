import os
import fitbit

client_id = os.getenv('FITBIT_CLIENT_ID')
client_secret = os.getenv('FITBIT_CLIENT_SECRET')
access_token=os.getenv('FITBIT_ACCESS_TOKEN')
refresh_token=os.getenv('FITBIT_REFRESH_TOKEN')

# unauth_client = fitbit.Fitbit('client_id', 'client_secret')
# certain methods do not require user keys
# unauth_client.food_units()


# You'll have to gather the tokens on your own, or use
# ./gather_keys_oauth2.py
# authd_client = fitbit.Fitbit(client_id, client_secret,
                            #  access_token, refresh_token)
# authd_client.sleep()


import os
from fitbit import Fitbit
from fitbit.api import FitbitOauth2Client
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError
from dotenv import load_dotenv

load_dotenv()

class DataCollectorFitbit:
    def __init__(self):
        self.client_id = os.getenv('FITBIT_CLIENT_ID')
        self.client_secret = os.getenv('FITBIT_CLIENT_SECRET')
        self.redirect_uri = 'https://localhost:8501/'
        self.client = None
        self.user_id = None

    def get_user_id(self):
        if not self.client:
            raise Exception("Not authorized. Please authorize first.")
        
        if not self.user_id:
            try:
                profile = self.client.user_profile_get()
                self.user_id = profile['user']['encodedId']
            except TokenExpiredError:
                self.refresh_token()
                profile = self.client.user_profile_get()
                self.user_id = profile['user']['encodedId']
        
        return self.user_id

    def get_auth_url(self):
        oauth = FitbitOauth2Client(self.client_id, self.client_secret)
        return oauth.authorize_token_url(redirect_uri=self.redirect_uri, scope=['activity', 'heartrate', 'sleep', 'profile'])[0]

    def complete_authorization(self, auth_code):
        oauth = FitbitOauth2Client(self.client_id, self.client_secret)
        token = oauth.fetch_access_token(auth_code, self.redirect_uri)
        self.client = Fitbit(self.client_id, self.client_secret, oauth2=True, access_token=token['access_token'], refresh_token=token['refresh_token'])
        return token

    def subscribe_to_updates(self):
        if not self.client:
            raise Exception("Not authorized. Please authorize first.")
        
        try:
            user_id = self.get_user_id()
            # The subscription ID should be unique for each subscription
            subscription_id = f"sub_{user_id}"
            response = self.client.subscription(subscription_id, 'activities')
            return user_id, response
        except TokenExpiredError:
            self.refresh_token()
            return self.subscribe_to_updates()
        except Exception as e:
            print(f"Subscription error: {e}")
            raise


    def get_patient_data(self, patient_id):
        if not self.client:
            raise Exception("Not authorized. Please authorize first.")

        try:
            # Fetch heart rate data
            heart_rate_data = self.client.intraday_time_series('activities/heart', detail_level='1min')

            # Fetch steps data
            steps_data = self.client.time_series('activities/steps', period='1d')

            # You can add more data points as needed

            return {
                'patient_id': patient_id,
                'heart_rate': heart_rate_data,
                'steps': steps_data,
            }
        except TokenExpiredError:
            self.refresh_token()
            return self.get_patient_data(patient_id)

    def refresh_token(self):
        token = self.client.client.refresh_token()
        self.client.client.session.token = token

def test_data_collector_fitbit():
    collector = DataCollectorFitbit()
    auth_url = collector.get_auth_url()
    print(f"Please visit this URL to authorize: {auth_url}")
    auth_code = input("Enter the authorization code: ")
    token = collector.complete_authorization(auth_code)
    if token:
        try:
            user_id, subscription_response = collector.subscribe_to_updates()
            print(f"Subscribed to updates for user ID: {user_id}")
            print(f"Subscription response: {subscription_response}")
            data = collector.get_patient_data(user_id)
            print("Latest data:", data)
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Authorization failed.")

if __name__ == "__main__":
    test_data_collector_fitbit()
