import streamlit as st
from data_collector import test_data_collector
from news2_algo import calculate_news_score
import json
from streamlit_ui_utils import display_news_score_and_suggestions, render_devices
import time

NEWS_DATA = [
    {"respiration_rate": 18, "SpO2_scale1": 99, "temperature": 36.6, "pulse": 54, "systolic_bp": 123, "consciousness": 'A', "on_oxygen": False},
    {"respiration_rate": 18, "SpO2_scale1": 99, "temperature": 36.6, "pulse": 54, "systolic_bp": 119, "consciousness": 'A', "on_oxygen": False},
    {"respiration_rate": 18, "SpO2_scale1": 99, "temperature": 37, "pulse": 56, "systolic_bp": 123, "consciousness": 'A', "on_oxygen": False},
    {"respiration_rate": 18, "SpO2_scale1": 99, "temperature": 37, "pulse": 57, "systolic_bp": 125, "consciousness": 'A', "on_oxygen": False},
    {"respiration_rate": 18, "SpO2_scale1": 99, "temperature": 37.1, "pulse": 87, "systolic_bp": 168, "consciousness": 'A', "on_oxygen": False},
    {"respiration_rate": 18, "SpO2_scale1": 99, "temperature": 37.1, "pulse": 130, "systolic_bp": 227, "consciousness": 'A', "on_oxygen": False},
    {"respiration_rate": 18, "SpO2_scale1": 99, "temperature": 38.8, "pulse": 149, "systolic_bp": 230, "consciousness": 'A', "on_oxygen": False},
    {"respiration_rate": 18, "SpO2_scale1": 99, "temperature": 39.8, "pulse": 149, "systolic_bp": 230, "consciousness": 'A', "on_oxygen": False},
    {"respiration_rate": 18, "SpO2_scale1": 99, "temperature": 40.6, "pulse": 149, "systolic_bp": 230, "consciousness": 'A', "on_oxygen": False},
    {"respiration_rate": 18, "SpO2_scale1": 99, "temperature": 37, "pulse": 137, "systolic_bp": 230, "consciousness": 'A', "on_oxygen": False},
    {"respiration_rate": 18, "SpO2_scale1": 99, "temperature": 37, "pulse": 154, "systolic_bp": 255, "consciousness": 'A', "on_oxygen": False},
    {"respiration_rate": 18, "SpO2_scale1": 99, "temperature": 37, "pulse": 154, "systolic_bp": 255, "consciousness": 'A', "on_oxygen": False},
    {"respiration_rate": 18, "SpO2_scale1": 99, "temperature": 37, "pulse": 154, "systolic_bp": 255, "consciousness": 'A', "on_oxygen": False},
    {"respiration_rate": 18, "SpO2_scale1": 99, "temperature": 37, "pulse": 80, "systolic_bp": 180, "consciousness": 'A', "on_oxygen": False},
    {"respiration_rate": 18, "SpO2_scale1": 99, "temperature": 37, "pulse": 80, "systolic_bp": 200, "consciousness": 'A', "on_oxygen": False},
    {"respiration_rate": 18, "SpO2_scale1": 95, "temperature": 37, "pulse": 80, "systolic_bp": 220, "consciousness": 'A', "on_oxygen": False},
    {"respiration_rate": 18, "SpO2_scale1": 95, "temperature": 37, "pulse": 80, "systolic_bp": 240, "consciousness": 'A', "on_oxygen": False},
    {"respiration_rate": 18, "SpO2_scale1": 95, "temperature": 37, "pulse": 80, "systolic_bp": 350, "consciousness": 'A', "on_oxygen": False},
    {"respiration_rate": 18, "SpO2_scale1": 95, "temperature": 37, "pulse": 80, "systolic_bp": 350, "consciousness": 'A', "on_oxygen": False},
    {"respiration_rate": 18, "SpO2_scale1": 95, "temperature": 37, "pulse": 80, "systolic_bp": 350, "consciousness": 'A', "on_oxygen": False},
    {"respiration_rate": 18, "SpO2_scale1": 95, "temperature": 37, "pulse": 80, "systolic_bp": 350, "consciousness": 'A', "on_oxygen": False},
    {"respiration_rate": 18, "SpO2_scale1": 95, "temperature": 37, "pulse": 80, "systolic_bp": 350, "consciousness": 'A', "on_oxygen": False},
    {"respiration_rate": 18, "SpO2_scale1": 95, "temperature": 37, "pulse": 80, "systolic_bp": 350, "consciousness": 'A', "on_oxygen": False},
]

def main():
    update_frequency = 5
    # Set page title
    st.set_page_config(page_title="NEWS2 Score Calculator", page_icon="🏥")
    # Add a title
    st.title("What's NEW? A&E NEWS Tracker")

    # Render devices
    render_devices()

    # Display details for the selected device
    if 'selected_device' in st.session_state:
        st.subheader(f"Details for {st.session_state.selected_device}")
        
        # Create two columns for EPR Number and Patient Attached toggle
        col1, col2 = st.columns(2)
        
        # EPR Number input in the left column
        with col1:
            epr_number = st.text_input("EPR Number", key=f"epr_{st.session_state.selected_device}")
        
        # Toggle for attaching/detaching a patient in the right column
        with col2:
            patient_attached = st.toggle("Patient Attached", 
                                         st.session_state[f"device_{st.session_state.selected_device}_state"]["patient_attached"],
                                         key=f"toggle_{st.session_state.selected_device}")
        
        # Update device state based on toggle and EPR Number
        st.session_state[f"device_{st.session_state.selected_device}_state"]["patient_attached"] = patient_attached
        st.session_state[f"device_{st.session_state.selected_device}_state"]["epr_number"] = epr_number
        
        if patient_attached:
            if st.button("Connect device and calculate score"):
                # Create placeholders for our content
                news_placeholder = st.empty()
                spinner_placeholder = st.empty()

                for i, data in enumerate(NEWS_DATA):
                    # Calculate NEWS score
                    news_score, message, param_received_3, params_with_3_points, respiration_rate, SpO2_scale1, temperature, pulse, systolic_bp, consciousness, on_oxygen = calculate_news_score(**data)
                    
                    # Update the NEWS score in the device state
                    st.session_state[f"device_{st.session_state.selected_device}_state"]["news_score"] = news_score
                    
                    # Display NEWS score and clinical suggestions
                    with news_placeholder.container():
                        display_news_score_and_suggestions(news_score, message, param_received_3, params_with_3_points,
                                                           respiration_rate, SpO2_scale1, temperature, pulse, systolic_bp,
                                                           consciousness, on_oxygen, update_frequency)
                    
                    # If it's not the last iteration, show the spinner
                    if i < len(NEWS_DATA) - 1:
                        with spinner_placeholder.container():
                            with st.spinner("Waiting for next reading..."):
                                time.sleep(update_frequency)
                    
                    # Clear both placeholders for the next iteration
                    news_placeholder.empty()
                    spinner_placeholder.empty()

    # Placeholder for future device data display
    st.empty()

if __name__ == "__main__":
    main()
