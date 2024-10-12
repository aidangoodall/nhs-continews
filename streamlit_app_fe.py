import streamlit as st
from data_collector import test_data_collector
import json

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
    # Add a button to fetch Fitbit data
    if st.button("Fetch Fitbit Data and Calculate NEWS Score"):
        with st.spinner("Fetching data from Fitbit..."):
            fitbit_data = test_data_collector()
        
        if fitbit_data:
            st.success("Successfully retrieved Fitbit data!")
            st.json(json.dumps(fitbit_data, indent=2))
            
            # Here you would process the data and calculate the NEWS score
            # For now, we'll just display some basic info
            st.write(f"Patient ID: {fitbit_data['patient_id']}")
            st.write(f"Steps Today: {fitbit_data['steps']['activities-steps'][0]['value']}")
            
            # Display heart rate data (this might need adjustment based on the actual data structure)
            if 'activities-heart-intraday' in fitbit_data['heart_rate']:
                hr_data = fitbit_data['heart_rate']['activities-heart-intraday']['dataset']
                st.write(f"Heart Rate Data Points: {len(hr_data)}")
                if hr_data:
                    st.write(f"Latest Heart Rate: {hr_data[-1]['value']} bpm")
            
            # TODO: Implement NEWS score calculation here
            st.write("NEWS Score calculation not yet implemented.")
        else:
            st.error("Failed to retrieve Fitbit data. Please check the console for more information.")

if __name__ == "__main__":
    main()
