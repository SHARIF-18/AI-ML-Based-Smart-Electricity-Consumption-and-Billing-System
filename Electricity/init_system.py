#!/usr/bin/env python3
"""
Smart Electricity System - Initialization Script
Run this script once to set up the database and directories
"""

import os
import sqlite3
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    directories = [
        'data',
        'data/reports',
        'static/images/profiles'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def initialize_database():
    """Initialize SQLite database with tables"""
    db_path = 'data/electricity.db'
    
    # Connect to database (creates if doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            phone TEXT,
            profile_picture TEXT,
            house_type TEXT,
            city TEXT,
            state TEXT,
            electricity_board TEXT,
            meter_number TEXT,
            connection_type TEXT,
            monthly_budget REAL DEFAULT 1000,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✓ Created users table")
    
    # Daily usage table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            appliance_data TEXT NOT NULL,
            total_units REAL NOT NULL,
            total_cost REAL NOT NULL,
            electricity_rate REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    print("✓ Created daily_usage table")
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print(f"✓ Database initialized: {db_path}")

def create_default_profile():
    """Create default profile SVG image"""
    profile_path = 'static/images/profiles/default.svg'
    
    svg_content = '''<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="50" fill="#3b82f6"/>
  <circle cx="50" cy="40" r="15" fill="white"/>
  <path d="M 25 70 Q 50 55 75 70" fill="white"/>
</svg>'''
    
    with open(profile_path, 'w') as f:
        f.write(svg_content)
    
    print(f"✓ Created default profile image: {profile_path}")

def main():
    """Main initialization function"""
    print("\n" + "="*60)
    print("Smart Electricity System - Initialization")
    print("="*60 + "\n")
    
    print("Step 1: Creating directories...")
    create_directories()
    
    print("\nStep 2: Initializing database...")
    initialize_database()
    
    print("\nStep 3: Creating default assets...")
    create_default_profile()
    
    print("\n" + "="*60)
    print("✓ Initialization complete!")
    print("="*60)
    print("\nYou can now run the application:")
    print("  python app.py")
    print("\nOr use the startup script:")
    print("  ./start.sh")
    print()

if __name__ == '__main__':
    main()
