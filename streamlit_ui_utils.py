# This file will contain utility functions and helper methods used across the application.


from datetime import datetime
import streamlit as st


def render_devices():
    st.header("Devices")
    cols = st.columns(4)
    for i in range(4):
        device_id = f"Device{i+1}"

        if f"device_{device_id}_state" not in st.session_state:
            st.session_state[f"device_{device_id}_state"] = {"patient_attached": False}

        with cols[i % 4]:
            button_color = "green" if st.session_state[f"device_{device_id}_state"]["patient_attached"] else "gray"
            if st.button(f"Device {i+1}", key=f"device_button_{i}",
                         help="Click to view device details",
                         type="primary" if button_color == "green" else "secondary"):
                st.session_state.selected_device = device_id


def display_news_score_and_suggestions(news_score, message, param_received_3, params_with_3_points,
                                       respiration_rate, SpO2_scale1, temperature, pulse, systolic_bp,
                                       consciousness, on_oxygen):
    # Determine color based on NEWS score
    if news_score == 0:
        color = "green"
    elif 1 <= news_score <= 4:
        color = "gray"
    elif news_score == 5 or news_score == 6:
        color = "orange"  # Using orange for amber
    else:  # 7 or more
        color = "red"

    st.markdown(f"<h3 style='color: {color};'>{message}</h3>", unsafe_allow_html=True)

    last_reading_time = datetime(2024, 10, 12, 21, 41)  # 12 Oct 2024 21:41
    current_time = datetime.now()
    time_difference = current_time - last_reading_time
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes = remainder // 60

    st.markdown(f"**Last reading taken at:** {last_reading_time.strftime('%d %b %Y %H:%M')}")
    st.markdown(f"**Time since last reading:** {hours} hours and {minutes} minutes")

    st.markdown("#### Clinical suggestion based on NEWS score")
    if news_score == 0:
        monitoring = "Minimum 12 hourly"
        response = "Continue routine NEWS monitoring"
    elif 1 <= news_score <= 4:
        monitoring = "Minimum 4–6 hourly"
        response = "• Inform registered nurse, who must assess the patient \n • Registered nurse decides whether increased frequency of monitoring and/or escalation of care is required"
    elif news_score == 5 or news_score == 6:
        monitoring = "Minimum 1 hourly"
        response = "• Registered nurse to immediately inform the medical team caring for the patient \n • Registered nurse to request urgent assessment by a clinician or team with core competencies in the care of acutely ill patients \n • Provide clinical care in an environment with monitoring facilities"
    else:  # 7 or more
        monitoring = "Continuous monitoring of vital signs"
        response = "• Registered nurse to immediately inform the medical team caring for the patient – this should be at least at specialist registrar level \n• Emergency assessment by a team with critical care competencies, including practitioner(s) with advanced airway management skills \n• Consider transfer of care to a level 2 or 3 clinical care facility, ie higher-dependency unit or ICU\n• Clinical care in an environment with monitoring facilities"

    st.markdown(f"**Frequency of monitoring:** {monitoring}")
    st.markdown(f"**Clinical response:** {response}")

    st.markdown("#### Vitals readings")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"**Respiratory Rate:** {respiration_rate} breaths/min" + (" 🚨" if "respiration_rate" in params_with_3_points else ""))
        st.markdown(f"**Oxygen Saturation:** {SpO2_scale1}%" + (" 🚨" if "SpO2" in params_with_3_points else ""))
        st.markdown(f"**Systolic Blood Pressure:** {systolic_bp} mmHg" + (" 🚨" if "systolic_bp" in params_with_3_points else ""))

    with col2:
        st.markdown(f"**Pulse:** {pulse} bpm" + (" 🚨" if "pulse" in params_with_3_points else ""))
        st.markdown(f"**Temperature:** {temperature}°C" + ("" if "temperature" in params_with_3_points else ""))
        st.markdown(f"**Consciousness Level:** {consciousness}" + (" 🚨" if "consciousness" in params_with_3_points else ""))

    st.markdown(f"**Supplemental Oxygen:** {'Yes' if on_oxygen else 'No'}")

    if param_received_3:
        st.markdown("### ⚠️ Critical Alert")
        st.markdown("The following parameters received a score of 3:")
        for param in params_with_3_points:
            st.markdown(f"- {param.replace('_', ' ').title()}")
        st.markdown("**Clinical Response:** Registered nurse to inform medical team caring for the patient, who will review and decide whether escalation of care is necessary.")