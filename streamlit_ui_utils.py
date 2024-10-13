# This file will contain utility functions and helper methods used across the application.


from datetime import datetime
import streamlit as st


def render_devices():
    st.header("Devices")
    cols = st.columns(4)
    for i in range(12):
        device_id = f"Device{i+1}"

        if f"device_{device_id}_state" not in st.session_state:
            st.session_state[f"device_{device_id}_state"] = {"patient_attached": False, "news_score": None}

        with cols[i % 4]:
            button_color = "green" if st.session_state[f"device_{device_id}_state"]["patient_attached"] else "gray"
            news_score = st.session_state[f"device_{device_id}_state"].get("news_score")
            
            button_label = f"Device {i+1}"
            if news_score is not None:
                button_label += f" (NEWS: {news_score})"
            
            if st.button(button_label, key=f"device_button_{i}",
                         help="Click to view device details",
                         type="primary" if button_color == "green" else "secondary"):
                st.session_state.selected_device = device_id


def display_news_score_and_suggestions(news_score, message, param_received_3, params_with_3_points,
                                       respiration_rate, SpO2_scale1, temperature, pulse, systolic_bp,
                                       consciousness, on_oxygen, update_frequency):
    # Determine color based on NEWS score
    if news_score == 0:
        color = "green"
    elif 1 <= news_score <= 4:
        color = "gray"
    elif news_score == 5 or news_score == 6:
        color = "orange"  # Using orange for amber
    else:  # 7 or more
        color = "red"

    # Create two columns for NEWS Score and Clinical Suggestions
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"<h3 style='color: {color};'>{message}</h3>", unsafe_allow_html=True)

        # Update this section to use the current time
        last_reading_time = datetime.now()
        st.markdown(f"**Last reading taken at:** {last_reading_time.strftime('%d %b %Y %H:%M:%S')}")
        st.markdown(f"**Updated every:** {update_frequency} seconds")

    with col2:
        st.markdown("#### Guideline suggestion")
        
        # Create an empty container
        suggestion_container = st.empty()
        
        # Prepare the content
        if news_score == 0:
            monitoring = "Minimum 12 hourly"
            response = "Continue routine NEWS monitoring"
        elif 1 <= news_score <= 4:
            monitoring = "Minimum 4–6 hourly"
            response = "Inform registered nurse, who must assess the patient"
        elif news_score == 5 or news_score == 6:
            monitoring = "Minimum 1 hourly"
            response = "Urgent assessment by a clinician"
        else:  # 7 or more
            monitoring = "Continuous monitoring of vital signs"
            response = "Emergency registrar assessment, consider level 2/3"

        # Update the container with the new content
        suggestion_container.markdown(f"""
        <div class="fixed-height-container">
            <div class="min-height-content top-aligned-content">
                <p><strong>Monitoring:</strong> {monitoring}</p>
                <p>{response}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### Vitals readings")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"##### Respiratory Rate: {respiration_rate} breaths/min" + (" 🚨" if "respiration_rate" in params_with_3_points else ""))
        st.markdown(f"##### Oxygen Saturation: {SpO2_scale1}%" + (" 🚨" if "SpO2" in params_with_3_points else ""))
        st.markdown(f"##### Systolic Blood Pressure: {systolic_bp if systolic_bp is not None else 'Unknown'} {'mmHg' if systolic_bp is not None else ''}" + (" 🚨" if "systolic_bp" in params_with_3_points else ""))

    with col2:
        st.markdown(f"##### Pulse: {pulse} bpm" + (" 🚨" if "pulse" in params_with_3_points else ""))
        st.markdown(f"##### Temperature: {temperature}°C" + (" 🚨" if "temperature" in params_with_3_points else ""))
        st.markdown(f"##### Consciousness Level: {consciousness if consciousness is not None else 'Unknown'}" + (" 🚨" if "consciousness" in params_with_3_points else ""))
    st.markdown(f"##### Supplemental Oxygen: {'Yes' if on_oxygen else 'No' if on_oxygen is not None else 'Unknown'}")

    # Create the critical alert placeholder here
    critical_alert_placeholder = st.empty()

    if param_received_3:
        critical_alert_content = "#### ⚠️ Critical Alert - parameters with a score of 3:\n\n"
        for param in params_with_3_points:
            critical_alert_content += f"- {param.replace('_', ' ').title()}\n"
        critical_alert_content += "\n**Clinical Response:** Registered nurse immediately informs medical team to decide on escalation."
        
        # Update the placeholder with the critical alert content
        critical_alert_placeholder.markdown(critical_alert_content)
    else:
        # Clear the placeholder if there's no critical alert
        critical_alert_placeholder.empty()
