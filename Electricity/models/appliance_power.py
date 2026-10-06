# Appliance Power Database
# Standard power consumption values for common household appliances

APPLIANCE_POWER = {
    # Cooling & Heating
    'AC 0.75 Ton': 800,
    'AC 1 Ton': 1000,
    'AC 1.5 Ton': 1500,
    'AC 2 Ton': 2000,
    'Air Conditioner': 1500,
    'AC': 1500,
    'Ceiling Fan': 75,
    'Table Fan': 50,
    'Exhaust Fan': 40,
    'Fan': 75,
    'Room Heater': 2000,
    'Heater': 2000,
    'Water Heater': 2000,
    'Geyser': 2000,
    
    # Kitchen Appliances
    'Refrigerator': 150,
    'Fridge': 150,
    'Microwave': 1200,
    'Microwave Oven': 1200,
    'Oven': 2000,
    'Electric Stove': 2000,
    'Induction Cooktop': 2000,
    'Mixer Grinder': 500,
    'Mixer': 500,
    'Grinder': 500,
    'Toaster': 800,
    'Electric Kettle': 1500,
    'Kettle': 1500,
    'Coffee Maker': 1000,
    'Dishwasher': 1800,
    'Food Processor': 500,
    
    # Washing & Cleaning
    'Washing Machine': 500,
    'Washer': 500,
    'Dryer': 3000,
    'Clothes Dryer': 3000,
    'Vacuum Cleaner': 1000,
    'Vacuum': 1000,
    'Iron': 1000,
    'Steam Iron': 1000,
    
    # Entertainment
    'TV': 100,
    'LED TV': 100,
    'LCD TV': 150,
    'Television': 100,
    'Smart TV': 120,
    'Home Theater': 300,
    'Sound System': 200,
    'Speaker': 100,
    'Music System': 200,
    'Gaming Console': 150,
    'PlayStation': 150,
    'Xbox': 150,
    
    # Computing
    'Desktop Computer': 200,
    'Desktop': 200,
    'Computer': 200,
    'PC': 200,
    'Laptop': 65,
    'Notebook': 65,
    'Printer': 50,
    'Scanner': 30,
    'WiFi Router': 10,
    'Router': 10,
    'Modem': 10,
    
    # Lighting
    'LED Bulb': 10,
    'LED Light': 10,
    'LED Lights': 60,
    'CFL Bulb': 15,
    'CFL': 15,
    'Tube Light': 40,
    'Incandescent Bulb': 60,
    'Light': 10,
    'Lights': 60,
    'Lamp': 10,
    
    # Other Appliances
    'Electric Motor': 750,
    'Water Pump': 750,
    'Motor': 750,
    'Pump': 750,
    'Aquarium': 50,
    'Fish Tank': 50,
    'Electric Chimney': 200,
    'Chimney': 200,
    'Stabilizer': 50,
    'UPS': 200,
    'Inverter': 100,
    'Air Purifier': 60,
    'Purifier': 60,
    'Humidifier': 50,
    'Dehumidifier': 300,
    'Electric Blanket': 200,
    'Hair Dryer': 1500,
    'Straightener': 100,
    'Curling Iron': 50,
    'Electric Shaver': 15,
    'Shaver': 15,
    'Trimmer': 10,
    'Charger': 10,
    'Phone Charger': 10,
    'Mobile Charger': 10,
}

def get_appliance_power(appliance_name):
    """Get power consumption for an appliance"""
    if not appliance_name:
        return None
    
    name = appliance_name.strip()
    if name in APPLIANCE_POWER:
        return APPLIANCE_POWER[name]
    
    name_lower = name.lower()
    for key, power in APPLIANCE_POWER.items():
        if key.lower() == name_lower:
            return power
    
    for key, power in APPLIANCE_POWER.items():
        if key.lower() in name_lower or name_lower in key.lower():
            return power
    
    return None

def get_all_appliances():
    """Get list of all appliances"""
    return sorted(APPLIANCE_POWER.keys())

def get_appliance_suggestions(query):
    """Get appliance name suggestions based on query"""
    if not query:
        return get_all_appliances()[:20]  # Return top 20
    
    query_lower = query.lower()
    suggestions = []
    
    # Exact matches first
    for name in APPLIANCE_POWER.keys():
        if name.lower().startswith(query_lower):
            suggestions.append(name)
    
    # Partial matches
    for name in APPLIANCE_POWER.keys():
        if query_lower in name.lower() and name not in suggestions:
            suggestions.append(name)
    
    return sorted(suggestions)[:10]  # Return top 10