#!/usr/bin/env python3
"""
Test Data Generator for Smart Electricity System
This script creates sample usage data for testing analytics and features
"""

import sqlite3
import json
from datetime import datetime, timedelta
import random

def generate_test_data(user_id=1, days=14):
    """Generate test usage data for a user"""
    
    db = sqlite3.connect('data/electricity.db')
    cursor = db.cursor()
    
    # Check if user exists
    cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,))
    if not cursor.fetchone():
        print(f"Error: User with ID {user_id} not found!")
        print("Please login first to create a user account.")
        db.close()
        return
    
    print(f"Generating {days} days of test data for user {user_id}...")
    
    # Sample appliances with their typical power consumption
    appliances_pool = [
        {'name': 'LED TV', 'power': 100, 'hours_range': (3, 8)},
        {'name': 'Refrigerator', 'power': 150, 'hours_range': (24, 24)},
        {'name': 'AC 1.5 Ton', 'power': 1500, 'hours_range': (4, 10)},
        {'name': 'Ceiling Fan', 'power': 75, 'hours_range': (8, 14)},
        {'name': 'LED Lights', 'power': 60, 'hours_range': (5, 10)},
        {'name': 'Laptop', 'power': 65, 'hours_range': (6, 12)},
        {'name': 'Washing Machine', 'power': 500, 'hours_range': (1, 2)},
        {'name': 'Water Heater', 'power': 2000, 'hours_range': (0.5, 2)},
    ]
    
    electricity_rate = 6.0  # ₹ per unit
    
    for day_offset in range(days):
        date = (datetime.now() - timedelta(days=days - day_offset)).strftime('%Y-%m-%d')
        
        # Select 4-6 random appliances for this day
        num_appliances = random.randint(4, 6)
        selected = random.sample(appliances_pool, num_appliances)
        
        appliances = []
        total_units = 0
        total_cost = 0
        
        for app_template in selected:
            # Add some randomness to hours
            min_hours, max_hours = app_template['hours_range']
            hours = round(random.uniform(min_hours, max_hours), 1)
            
            # Calculate units and cost
            power = app_template['power']
            units = (power * hours) / 1000
            cost = units * electricity_rate
            
            appliances.append({
                'name': app_template['name'],
                'power': power,
                'hours': hours,
                'units': units,
                'cost': cost
            })
            
            total_units += units
            total_cost += cost
        
        # Check if entry already exists
        cursor.execute('''
            SELECT id FROM daily_usage 
            WHERE user_id = ? AND date = ?
        ''', (user_id, date))
        
        if cursor.fetchone():
            # Update existing
            cursor.execute('''
                UPDATE daily_usage
                SET appliance_data = ?, total_units = ?, total_cost = ?, electricity_rate = ?
                WHERE user_id = ? AND date = ?
            ''', (json.dumps(appliances), total_units, total_cost, electricity_rate, user_id, date))
            print(f"  Updated: {date} - ₹{total_cost:.2f}")
        else:
            # Insert new
            cursor.execute('''
                INSERT INTO daily_usage (user_id, date, appliance_data, total_units, total_cost, electricity_rate)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, date, json.dumps(appliances), total_units, total_cost, electricity_rate))
            print(f"  Created: {date} - ₹{total_cost:.2f}")
    
    db.commit()
    db.close()
    
    print(f"\n✓ Successfully generated {days} days of test data!")
    print("\nNow you can:")
    print("  1. View Analytics - All 4 charts will display")
    print("  2. Check AI Predictions - Forecasts available")
    print("  3. See Suggestions - Personalized tips generated")
    print("  4. Download PDFs - With AI recommendations")

def main():
    print("="*60)
    print("Smart Electricity System - Test Data Generator")
    print("="*60)
    print()
    
    # Check if database exists
    import os
    if not os.path.exists('data/electricity.db'):
        print("Error: Database not found!")
        print("Please run: python3 init_system.py")
        return
    
    # Get user input
    try:
        user_id_input = input("Enter user ID (default: 1): ").strip()
        user_id = int(user_id_input) if user_id_input else 1
        
        days_input = input("How many days of data? (default: 14): ").strip()
        days = int(days_input) if days_input else 14
        
        if days < 1 or days > 365:
            print("Error: Days must be between 1 and 365")
            return
        
        print()
        generate_test_data(user_id, days)
        
    except ValueError as e:
        print(f"Error: Invalid input - {e}")
    except KeyboardInterrupt:
        print("\n\nCancelled by user")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()