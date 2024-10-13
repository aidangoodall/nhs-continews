import streamlit as st
from data_collector import test_data_collector
from news2_algo import calculate_news_score
import json
from streamlit_ui_utils import display_news_score_and_suggestions, render_devices
from demo_data import DEMO_DATA
import time

def initialize_device_states():
    for i in range(4):  # Initialize states for 4 devices
        if f"device_{i}_state" not in st.session_state:
            st.session_state[f"device_{i}_state"] = {
                "news_score": 0,
                "patient_attached": False
            }


def main():
    # Set page title
    st.set_page_config(page_title="NEWS2 Score Calculator", page_icon="🏥")
    # Add a title
    st.title("What's NEW? A&E NEWS Tracker")

    if 'demo_mode' not in st.session_state:
        st.session_state.demo_mode = False
        st.session_state.demo_iteration = 0

    if st.button("Toggle Demo Mode"):
        st.session_state.demo_mode = not st.session_state.demo_mode
        st.session_state.demo_iteration = 0
  
    initialize_device_states()

    # Render devices
    render_devices()

    if st.session_state.demo_mode:
        st.write(f"Demo Mode Active - Iteration {st.session_state.demo_iteration + 1}/5")
        for device_index, device_data in enumerate(DEMO_DATA):
            if st.session_state.demo_iteration < len(device_data):
                data = device_data[st.session_state.demo_iteration]
                news_score, message, param_received_3, params_with_3_points, *_ = calculate_news_score(*data)
                st.session_state[f"device_{device_index}_state"]["news_score"] = news_score
                st.session_state[f"device_{device_index}_state"]["patient_attached"] = True
                st.subheader(f"Device {device_index + 1}")
                display_news_score_and_suggestions(news_score, message, param_received_3, params_with_3_points, *data)

        # Increment demo iteration and rerun after 30 seconds
        if st.session_state.demo_iteration < len(DEMO_DATA[0]) - 1:
            time.sleep(30)
            st.session_state.demo_iteration += 1
            st.experimental_rerun()
        else:
            st.write("Demo completed. Toggle Demo Mode to restart.")

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
                # news_score, message, param_received_3, params_with_3_points, respiration_rate, SpO2_scale1, temperature, pulse, systolic_bp, consciousness, on_oxygen = calculate_news_score(18, 95, 43, 80)
                news_score, message, param_received_3, params_with_3_points, respiration_rate, SpO2_scale1, temperature, pulse, systolic_bp, consciousness, on_oxygen = calculate_news_score(18, 95, 34.9, 80, systolic_bp=350, consciousness='A', on_oxygen=False)
                
                


                # Update the NEWS score in the device state
                st.session_state[f"device_{st.session_state.selected_device}_state"]["news_score"] = news_score
                
                # Display NEWS score and clinical suggestions
                display_news_score_and_suggestions(news_score, message, param_received_3, params_with_3_points,
                                                   respiration_rate, SpO2_scale1, temperature, pulse, systolic_bp,
                                                   consciousness, on_oxygen)

    # Placeholder for future device data display
    st.empty()

if __name__ == "__main__":
    main()
