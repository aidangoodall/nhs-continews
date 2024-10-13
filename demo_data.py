def generate_specific_demo_data():
    # Initialize data for 4 devices
    data = [[] for _ in range(4)]
    
    # Initial values for each device
    initial_values = [
        (18, 95, 37.0, 70),  # Device 0
        (16, 98, 36.5, 65),  # Device 1
        (20, 97, 37.2, 75),  # Device 2
        (17, 96, 36.8, 68),  # Device 3
    ]
    
    # Generate data for 5 iterations (0 to 2 minutes, every 30 seconds)
    for i in range(5):
        for device in range(4):
            if device == 2:  # Device 3 (index 2) with increasing heart rate
                respiration_rate, spo2, temperature, pulse = initial_values[device]
                pulse = min(130, pulse + 15 * i)  # Increase by 15 every 30 seconds, max 130
                data[device].append((respiration_rate, spo2, temperature, pulse))
            else:
                # Other devices keep the same values
                data[device].append(initial_values[device])
    
    return data

DEMO_DATA = generate_specific_demo_data()