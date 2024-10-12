def calculate_news_score(respiration_rate, SpO2_scale1, temperature, pulse, systolic_bp=None, consciousness=None, on_oxygen=None):
    """
    Calculate the NEWS (National Early Warning Score) based on the available physiological parameters.
    
    Parameters:
    - respiration_rate: breaths per minute
    - SpO2_scale1: percentage (%)
    - temperature: degrees Celsius
    - pulse: beats per minute
    - systolic_bp: mmHg (optional)
    - consciousness: 'A' for Alert, 'V' for Voice, 'P' for Pain, 'U' for Unresponsive (optional)
    - on_oxygen: boolean (optional)
    
    Returns:
    - Tuple: (score, message, param_received_3, params_with_3_points, respiration_rate, SpO2_scale1, temperature, pulse, systolic_bp, consciousness, on_oxygen)
    """
    required_params = [respiration_rate, SpO2_scale1, temperature, pulse]
    if any(param is None for param in required_params):
        return None, "Missing too many parameters, couldn't calculate NEWS score"

    # Error checking for required parameters
    if not isinstance(respiration_rate, (int, float)) or respiration_rate < 0:
        raise ValueError("Respiration rate must be a non-negative number")
    if not isinstance(SpO2_scale1, (int, float)) or not 0 <= SpO2_scale1 <= 100:
        raise ValueError("SpO2 must be a number between 0 and 100")
    if not isinstance(temperature, (int, float)):
        raise ValueError("Temperature must be a number")
    if not isinstance(pulse, (int, float)) or pulse < 0:
        raise ValueError("Pulse must be a non-negative number")

    score = 0
    param_received_3 = False
    params_with_3_points = []
    
    # Scoring logic for required parameters
    # Respiratory rate
    if respiration_rate <= 8 or respiration_rate >= 25:
        score += 3
        param_received_3 = True
        params_with_3_points.append("respiration_rate")
    elif 21 <= respiration_rate <= 24:
        score += 2
    elif 9 <= respiration_rate <= 11:
        score += 1
    elif 12 <= respiration_rate <= 20:
        score += 0
    else:
        print(f"Error: Unexpected value for respiration rate: {respiration_rate}")
    
    # Oxygen saturation
    if SpO2_scale1 <= 91:
        score += 3
        param_received_3 = True
        params_with_3_points.append("SpO2")
    elif 92 <= SpO2_scale1 <= 93:
        score += 2
    elif 94 <= SpO2_scale1 <= 95:
        score += 1
    elif SpO2_scale1 >= 96:
        score += 0
    else:
        print(f"Error: Unexpected value for SpO2: {SpO2_scale1}")
    
    # Temperature
    if temperature <= 35.0:
        score += 3
        param_received_3 = True
        params_with_3_points.append("temperature")
    elif 35.1 <= temperature <= 36.0:
        score += 1
    elif 36.1 <= temperature <= 38.0:
        score += 0
    elif 38.1 <= temperature <= 39.0:
        score += 1
    elif temperature >= 39.1:
        score += 2
    else:
        print(f"Error: Unexpected value for temperature: {temperature}")
    
    # Pulse
    if pulse <= 40 or pulse >= 131:
        score += 3
        param_received_3 = True
        params_with_3_points.append("pulse")
    elif 111 <= pulse <= 130:
        score += 2
    elif 41 <= pulse <= 50 or 91 <= pulse <= 110:
        score += 1
    elif 51 <= pulse <= 90:
        score += 0
    else:
        print(f"Error: Unexpected value for pulse: {pulse}")

    # Systolic blood pressure (optional)
    bp_consciousness_missing = []
    if systolic_bp is not None:
        if not isinstance(systolic_bp, (int, float)) or systolic_bp < 0:
            raise ValueError("Systolic blood pressure must be a non-negative number")
        if systolic_bp <= 90 or systolic_bp >= 220:
            score += 3
            param_received_3 = True
            params_with_3_points.append("systolic_bp")
        elif 91 <= systolic_bp <= 100:
            score += 2
        elif 101 <= systolic_bp <= 110:
            score += 1
        elif 111 <= systolic_bp <= 219:
            score += 0
        else:
            print(f"Error: Unexpected value for systolic blood pressure: {systolic_bp}")
    else:
        bp_consciousness_missing.append("bp")

    # Consciousness (optional)
    if consciousness is not None:
        if not isinstance(consciousness, str) or consciousness.upper() not in ['A', 'V', 'P', 'U']:
            raise ValueError("Consciousness must be 'A', 'V', 'P', or 'U'")
        if consciousness.upper() == 'A':
            score += 0
        elif consciousness.upper() in ['V', 'P', 'U']:
            score += 3
            param_received_3 = True
            params_with_3_points.append("consciousness")
        else:
            print(f"Error: Unexpected value for consciousness: {consciousness}")
    else:
        bp_consciousness_missing.append("consciousness")

    # Prepare the result message
    if not bp_consciousness_missing:
        message = f"NEWS2 Score is: {score}"
    else:
        missing = " and ".join(bp_consciousness_missing)
        message = f"NEWS2 Score is: {score} (excluding {missing})"

    return score, message, param_received_3, params_with_3_points, respiration_rate, SpO2_scale1, temperature, pulse, systolic_bp, consciousness, on_oxygen

# Example usage
if __name__ == "__main__":
    # Test with all parameters
    score, message, param_received_3, params_with_3_points, *_ = calculate_news_score(18, 95, 37.5, 80, 120, 'A', False)
    print(message)
    print(f"Any parameter received 3 points: {param_received_3}")
    print(f"Parameters that received 3 points: {params_with_3_points}")

    # Test with high respiration rate
    score, message, param_received_3, params_with_3_points, *_ = calculate_news_score(26, 95, 37.5, 80, 120, 'A', False)
    print(message)
    print(f"Any parameter received 3 points: {param_received_3}")
    print(f"Parameters that received 3 points: {params_with_3_points}")

    # Test without blood pressure
    score, message = calculate_news_score(18, 99, 37.5, 80, consciousness='A', on_oxygen=True)
    print(message)

    # Test without consciousness
    score, message = calculate_news_score(18, 95, 41, 80, systolic_bp=120, on_oxygen=False)
    print(message)

    # Test without both blood pressure and consciousness
    score, message = calculate_news_score(11, 95, 37.5, 80, on_oxygen=True)
    print(message)

    # Test without oxygen status
    score, message = calculate_news_score(18, 95, 37.5, 80, systolic_bp=120, consciousness='A')
    print(message)

    # Test with missing required parameter
    score, message = calculate_news_score(None, 95, 37.5, 80)
    print(message)
