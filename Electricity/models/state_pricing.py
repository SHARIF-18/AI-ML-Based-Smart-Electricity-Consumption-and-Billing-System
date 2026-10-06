# Slab-based electricity tariff for all states
# Format: (max_units_in_slab, rate_per_unit)
# Last slab uses float('inf') for unlimited upper limit

STATE_TARIFF = {
    'Andhra Pradesh': [
        (30, 1.90),
        (45, 3.00),   # 31-75 units (45 more units)
        (50, 4.50),   # 76-125 units (50 more units)
        (100, 6.00),  # 126-225 units (100 more units)
        (float('inf'), 8.00)  # 225+ units
    ],
    'Telangana': [
        (50, 1.50),
        (50, 2.50),
        (100, 4.50),
        (100, 6.00),
        (float('inf'), 8.50)
    ],
    'Karnataka': [
        (30, 2.25),
        (70, 3.75),
        (70, 5.00),
        (100, 6.75),
        (float('inf'), 7.80)
    ],
    'Tamil Nadu': [
        (100, 0.00),   # First 100 units free for domestic
        (100, 2.25),
        (300, 4.50),
        (float('inf'), 6.00)
    ],
    'Maharashtra': [
        (100, 2.65),
        (200, 5.50),
        (200, 7.95),
        (float('inf'), 10.40)
    ],
    'Gujarat': [
        (50, 2.00),
        (50, 3.00),
        (100, 4.50),
        (100, 6.00),
        (float('inf'), 6.50)
    ],
    'Rajasthan': [
        (50, 2.70),
        (100, 3.95),
        (150, 5.40),
        (float('inf'), 6.95)
    ],
    'Delhi': [
        (200, 3.00),
        (200, 4.50),
        (400, 6.50),
        (float('inf'), 8.00)
    ],
    'Kerala': [
        (40, 2.90),
        (60, 3.70),
        (100, 5.00),
        (100, 6.90),
        (float('inf'), 7.90)
    ],
    'West Bengal': [
        (60, 4.50),
        (60, 6.00),
        (100, 7.25),
        (float('inf'), 8.10)
    ],
    'Uttar Pradesh': [
        (150, 3.35),
        (150, 4.70),
        (200, 5.80),
        (float('inf'), 6.55)
    ],
    'Punjab': [
        (100, 3.02),
        (200, 4.82),
        (float('inf'), 6.07)
    ],
    'Haryana': [
        (150, 2.75),
        (150, 4.05),
        (float('inf'), 5.70)
    ],
    'Madhya Pradesh': [
        (100, 3.45),
        (100, 5.40),
        (float('inf'), 6.70)
    ],
    'Bihar': [
        (100, 4.10),
        (100, 4.90),
        (float('inf'), 6.55)
    ],
    'Odisha': [
        (50, 2.80),
        (100, 4.80),
        (float('inf'), 5.40)
    ],
    'Jharkhand': [
        (150, 3.75),
        (150, 4.90),
        (float('inf'), 5.75)
    ],
    'Chhattisgarh': [
        (100, 2.75),
        (200, 4.25),
        (float('inf'), 5.75)
    ],
    'Assam': [
        (30, 3.75),
        (70, 5.40),
        (100, 6.30),
        (float('inf'), 6.75)
    ],
    'Himachal Pradesh': [
        (60, 1.50),
        (125, 2.75),
        (float('inf'), 4.00)
    ],
    'Uttarakhand': [
        (100, 2.35),
        (200, 3.60),
        (float('inf'), 5.15)
    ],
    'Goa': [
        (30, 2.00),
        (170, 3.50),
        (float('inf'), 5.00)
    ],
    'Puducherry': [
        (100, 0.00),
        (200, 3.50),
        (float('inf'), 5.50)
    ],
    'Chandigarh': [
        (150, 2.15),
        (250, 3.90),
        (float('inf'), 5.35)
    ],
    'Jammu and Kashmir': [
        (50, 1.70),
        (100, 3.00),
        (float('inf'), 5.00)
    ],
    # Default slab structure (if state not found)
    'Default': [
        (100, 3.00),
        (100, 5.00),
        (float('inf'), 7.00)
    ]
}


def calculate_bill(units, state):
    """
    Calculate electricity bill using slab-based tariff system
    
    Args:
        units (float): Total units consumed
        state (str): State name
    
    Returns:
        float: Total bill amount in rupees
    
    Example:
        >>> calculate_bill(150, 'Andhra Pradesh')
        # First 30 units: 30 × 1.90 = 57.00
        # Next 45 units: 45 × 3.00 = 135.00
        # Next 50 units: 50 × 4.50 = 225.00
        # Next 25 units: 25 × 6.00 = 150.00
        # Total: 567.00
    """
    if units <= 0:
        return 0.0
    
    # Get tariff slabs for the state
    slabs = STATE_TARIFF.get(state, STATE_TARIFF['Default'])
    
    total_cost = 0.0
    remaining_units = units
    
    for slab_units, rate in slabs:
        if remaining_units <= 0:
            break
        
        # Calculate units to charge in this slab
        units_in_slab = min(remaining_units, slab_units)
        
        # Add cost for this slab
        total_cost += units_in_slab * rate
        
        # Reduce remaining units
        remaining_units -= units_in_slab
    
    return round(total_cost, 2)


def get_effective_rate(units, state):
    """
    Get the effective rate per unit (for display purposes)
    This is just total_cost / units
    
    Args:
        units (float): Total units consumed
        state (str): State name
    
    Returns:
        float: Effective rate per unit
    """
    if units <= 0:
        return 0.0
    
    total_cost = calculate_bill(units, state)
    return round(total_cost / units, 2)


def get_slab_breakdown(units, state):
    """
    Get detailed breakdown of bill by slabs
    
    Args:
        units (float): Total units consumed
        state (str): State name
    
    Returns:
        list: List of dicts with slab details
    
    Example:
        >>> get_slab_breakdown(150, 'Andhra Pradesh')
        [
            {'slab': '1-30', 'units': 30, 'rate': 1.9, 'cost': 57.0},
            {'slab': '31-75', 'units': 45, 'rate': 3.0, 'cost': 135.0},
            {'slab': '76-125', 'units': 50, 'rate': 4.5, 'cost': 225.0},
            {'slab': '126-225', 'units': 25, 'rate': 6.0, 'cost': 150.0}
        ]
    """
    if units <= 0:
        return []
    
    slabs = STATE_TARIFF.get(state, STATE_TARIFF['Default'])
    
    breakdown = []
    remaining_units = units
    cumulative_units = 0
    
    for slab_units, rate in slabs:
        if remaining_units <= 0:
            break
        
        units_in_slab = min(remaining_units, slab_units)
        cost_in_slab = units_in_slab * rate
        
        # Determine slab range
        slab_start = cumulative_units
        slab_end = cumulative_units + slab_units
        
        if slab_units == float('inf'):
            slab_range = f"{slab_start + 1}+"
        else:
            slab_range = f"{slab_start + 1}-{slab_end}"
        
        breakdown.append({
            'slab': slab_range,
            'units': round(units_in_slab, 2),
            'rate': rate,
            'cost': round(cost_in_slab, 2)
        })
        
        remaining_units -= units_in_slab
        cumulative_units += slab_units if slab_units != float('inf') else units_in_slab
    
    return breakdown


# Legacy compatibility - keep for old code that might use it
STATE_ELECTRICITY_RATES = {
    state: calculate_bill(100, state) / 100  # Average rate for 100 units
    for state in STATE_TARIFF.keys()
}