def calculate_news_score(respiration_rate, SpO2_scale1, temperature, systolic_bp, pulse, consciousness):
    """
    Calculate the NEWS (National Early Warning Score) based on the six key physiological parameters.
    
    Parameters:
    - respiration_rate: breaths per minute
    - SpO2_scale1: percentage (%)
    - temperature: degrees Celsius
    - systolic_bp: mmHg
    - pulse: beats per minute
    - consciousness: 'A' for Alert, 'V' for Voice, 'P' for Pain, 'U' for Unresponsive
    
    Returns:
    - NEWS score (integer)
    """
    score = 0
    
    # Respiratory rate
    if respiration_rate <= 8 or respiration_rate >= 25:
        score += 3
    elif 21 <= respiration_rate <= 24:
        score += 2
    elif 9 <= respiration_rate <= 11:
        score += 1
    elif 12 <= respiration_rate <= 20:
        score += 0
    
    # Oxygen saturation
    if SpO2_scale1 <= 91:
        score += 3
    elif 92 <= SpO2_scale1 <= 93:
        score += 2
    elif 94 <= SpO2_scale1 <= 95:
        score += 1
    elif SpO2_scale1 >= 96:
        score += 0
    
    # Temperature
    if temperature <= 35.0:
        score += 3
    elif 35.1 <= temperature <= 36.0:
        score += 1
    elif 36.1 <= temperature <= 38.0:
        score += 0
    elif 38.1 <= temperature <= 39.0:
        score += 1
    elif temperature >= 39.1:
        score += 2
    
    # Systolic blood pressure
    if systolic_bp <= 90 or systolic_bp >= 220:
        score += 3
    elif 91 <= systolic_bp <= 100:
        score += 2
    elif 101 <= systolic_bp <= 110:
        score += 1
    elif 111 <= systolic_bp <= 219:
        score += 0
    
    # Pulse
    if pulse <= 40 or pulse >= 131:
        score += 3
    elif 111 <= pulse <= 130:
        score += 2
    elif 41 <= pulse <= 50 or 91 <= pulse <= 110:
        score += 1
    elif 51 <= pulse <= 90:
        score += 0
    
    # Consciousness
    if consciousness.upper() == 'A':
        score += 0
    else:
        score += 3
    
    return score

# Example usage
if __name__ == "__main__":
    news_score = calculate_news_score(
        respiration_rate=18,
        SpO2_scale1=95,
        temperature=37.5,
        systolic_bp=499,
        pulse=80,
        consciousness='A'
    )
    print(f"NEWS Score: {news_score}")