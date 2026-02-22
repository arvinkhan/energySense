POWER = {
    "lights": 12,
    "fan": 60,
    "projector": 200
}

def calculate_waste(appliances):
    total_watts = sum(POWER[a] for a in appliances)
    units_per_hour = total_watts / 1000
    return total_watts, units_per_hour
