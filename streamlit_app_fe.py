import streamlit as st
from data_collector import test_data_collector
from news2_algo import calculate_news_score
import json
from streamlit_ui_utils import display_news_score_and_suggestions, render_devices

def main():
    # Set page title
    st.set_page_config(page_title="NEWS2 Score Calculator", page_icon="🏥")
    # Add a title
    st.title("What's NEW? A&E NEWS Tracker")

    # Render devices
    render_devices()

    # Display details for the selected device
    if 'selected_device' in st.session_state:
        st.subheader(f"Details for {st.session_state.selected_device}")
        
        # Toggle for attaching/detaching a patient
        patient_attached = st.toggle("Patient Attached", 
                                     st.session_state[f"device_{st.session_state.selected_device}_state"]["patient_attached"],
                                     key=f"toggle_{st.session_state.selected_device}")
        
        # Update device state based on toggle
        st.session_state[f"device_{st.session_state.selected_device}_state"]["patient_attached"] = patient_attached
        
        if patient_attached:
            if st.button("Fetch data and calculate NEWS"):
                # Calculate NEWS score using news2_algo.py
                news_score, message, param_received_3, params_with_3_points, respiration_rate, SpO2_scale1, temperature, pulse, systolic_bp, consciousness, on_oxygen = calculate_news_score(18, 95, 37.5, 80, systolic_bp=350, consciousness='A', on_oxygen=False)
                
                # Display NEWS score and clinical suggestions
                display_news_score_and_suggestions(news_score, message, param_received_3, params_with_3_points,
                                                   respiration_rate, SpO2_scale1, temperature, pulse, systolic_bp,
                                                   consciousness, on_oxygen)

        # Placeholder for future device data display
        st.empty()

if __name__ == "__main__":
    main()
