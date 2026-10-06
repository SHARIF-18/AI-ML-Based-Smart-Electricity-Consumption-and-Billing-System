from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
import sqlite3
import os
import hashlib
from datetime import datetime, timedelta
from functools import wraps
import json
from models.ml_predictor import ElectricityPredictor
from models.pdf_generator import generate_pdf_report
from models.state_pricing import calculate_bill, get_effective_rate, get_slab_breakdown, STATE_TARIFF
from models.appliance_power import get_appliance_power, get_appliance_suggestions, APPLIANCE_POWER

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'
app.config['DATABASE'] = 'data/electricity.db'
app.config['UPLOAD_FOLDER'] = 'static/images/profiles'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_db():
    """Get database connection"""
    db = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Initialize database with tables"""
    db = get_db()
    cursor = db.cursor()
    
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
    
    db.commit()
    db.close()

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User signup"""
    if request.method == 'POST':
        try:
            data = request.form
            
            # Handle profile picture upload
            profile_pic = None
            if 'profile_picture' in request.files:
                file = request.files['profile_picture']
                if file.filename:
                    filename = f"{data['email'].replace('@', '_').replace('.', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    profile_pic = filename
            
            db = get_db()
            cursor = db.cursor()
            
            # Check if user exists
            cursor.execute('SELECT id FROM users WHERE email = ?', (data['email'],))
            if cursor.fetchone():
                return jsonify({'success': False, 'message': 'Email already registered'})
            
            # Insert new user
            cursor.execute('''
                INSERT INTO users (email, password, full_name, phone, profile_picture,
                                 house_type, city, state, electricity_board, meter_number,
                                 connection_type, monthly_budget)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['email'],
                hash_password(data['password']),
                data['full_name'],
                data.get('phone', ''),
                profile_pic,
                data.get('house_type', ''),
                data.get('city', ''),
                data.get('state', ''),
                data.get('electricity_board', ''),
                data.get('meter_number', ''),
                data.get('connection_type', ''),
                float(data.get('monthly_budget', 1000))
            ))
            
            db.commit()
            db.close()
            
            return jsonify({'success': True, 'message': 'Registration successful!'})
            
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        data = request.json
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('SELECT id, password FROM users WHERE email = ?', (data['email'],))
        user = cursor.fetchone()
        
        if user and user['password'] == hash_password(data['password']):
            session['user_id'] = user['id']
            db.close()
            return jsonify({'success': True})
        
        db.close()
        return jsonify({'success': False, 'message': 'Invalid credentials'})
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    return render_template('dashboard.html')

@app.route('/api/user-profile')
@login_required
def get_user_profile():
    """Get user profile data"""
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],))
    user = cursor.fetchone()
    
    db.close()
    
    return jsonify({
        'full_name': user['full_name'],
        'email': user['email'],
        'phone': user['phone'],
        'profile_picture': user['profile_picture'],
        'house_type': user['house_type'],
        'city': user['city'],
        'state': user['state'],
        'electricity_board': user['electricity_board'],
        'meter_number': user['meter_number'],
        'connection_type': user['connection_type'],
        'monthly_budget': user['monthly_budget']
    })

@app.route('/api/dashboard-stats')
@login_required
def get_dashboard_stats():
    """Get dashboard statistics"""
    db = get_db()
    cursor = db.cursor()
    
    # Get user budget and state
    cursor.execute('SELECT monthly_budget, state FROM users WHERE id = ?', (session['user_id'],))
    user = cursor.fetchone()
    monthly_budget = user['monthly_budget']
    
    # Get current month data
    current_month = datetime.now().strftime('%Y-%m')
    cursor.execute('''
        SELECT SUM(total_cost) as month_total, SUM(total_units) as month_units
        FROM daily_usage
        WHERE user_id = ? AND date LIKE ?
    ''', (session['user_id'], f'{current_month}%'))
    
    month_data = cursor.fetchone()
    month_total = month_data['month_total'] or 0
    month_units = month_data['month_units'] or 0
    
    # Get today's data
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('''
        SELECT total_cost, total_units
        FROM daily_usage
        WHERE user_id = ? AND date = ?
    ''', (session['user_id'], today))
    
    today_data = cursor.fetchone()
    today_cost = today_data['total_cost'] if today_data else 0
    today_units = today_data['total_units'] if today_data else 0
    
    db.close()
    
    remaining = monthly_budget - month_total
    budget_percentage = (month_total / monthly_budget * 100) if monthly_budget > 0 else 0
    
    return jsonify({
        'today_cost': round(today_cost, 2),
        'today_units': round(today_units, 2),
        'month_total': round(month_total, 2),
        'monthly_budget': monthly_budget,
        'remaining_balance': round(remaining, 2),
        'budget_percentage': round(budget_percentage, 2),
        'budget_exceeded': month_total > monthly_budget
    })

@app.route('/api/save-daily-usage', methods=['POST'])
@login_required
def save_daily_usage():
    """Save daily electricity usage"""
    try:
        data = request.json
        
        db = get_db()
        cursor = db.cursor()
        
        # Get user's state for electricity calculation
        cursor.execute('SELECT state FROM users WHERE id = ?', (session['user_id'],))
        user = cursor.fetchone()
        state = user['state'] or 'Default'
        
        # Recalculate total cost using slab system
        total_units = data['total_units']
        total_cost = calculate_bill(total_units, state)
        effective_rate = get_effective_rate(total_units, state)
        
        # Check if entry exists for this date
        cursor.execute('''
            SELECT id FROM daily_usage WHERE user_id = ? AND date = ?
        ''', (session['user_id'], data['date']))
        
        existing = cursor.fetchone()
        
        if existing:
            # Update existing entry
            cursor.execute('''
                UPDATE daily_usage
                SET appliance_data = ?, total_units = ?, total_cost = ?, electricity_rate = ?
                WHERE id = ?
            ''', (
                json.dumps(data['appliances']),
                total_units,
                total_cost,
                effective_rate,
                existing['id']
            ))
        else:
            # Insert new entry
            cursor.execute('''
                INSERT INTO daily_usage (user_id, date, appliance_data, total_units, total_cost, electricity_rate)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                session['user_id'],
                data['date'],
                json.dumps(data['appliances']),
                total_units,
                total_cost,
                effective_rate
            ))
        
        db.commit()
        db.close()
        
        return jsonify({
            'success': True,
            'message': 'Usage saved successfully!',
            'total_cost': total_cost,
            'effective_rate': effective_rate
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/usage-history')
@login_required
def get_usage_history():
    """Get usage history dates"""
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('''
        SELECT date, total_units, total_cost
        FROM daily_usage
        WHERE user_id = ?
        ORDER BY date DESC
        LIMIT 30
    ''', (session['user_id'],))
    
    history = [dict(row) for row in cursor.fetchall()]
    db.close()
    
    return jsonify(history)

@app.route('/api/usage-details/<date>')
@login_required
def get_usage_details(date):
    """Get usage details for a specific date"""
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('''
        SELECT appliance_data, total_units, total_cost, electricity_rate
        FROM daily_usage
        WHERE user_id = ? AND date = ?
    ''', (session['user_id'], date))
    
    data = cursor.fetchone()
    db.close()
    
    if data:
        return jsonify({
            'appliances': json.loads(data['appliance_data']),
            'total_units': data['total_units'],
            'total_cost': data['total_cost'],
            'electricity_rate': data['electricity_rate']
        })
    
    return jsonify({'appliances': []})

@app.route('/api/analytics-data')
@login_required
def get_analytics_data():
    """Get analytics data for charts"""
    db = get_db()
    cursor = db.cursor()
    
    # Last 30 days data
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    cursor.execute('''
        SELECT date, total_cost, total_units, appliance_data
        FROM daily_usage
        WHERE user_id = ? AND date >= ?
        ORDER BY date ASC
    ''', (session['user_id'], thirty_days_ago))
    
    daily_data = [dict(row) for row in cursor.fetchall()]
    
    # Monthly trends (last 6 months)
    six_months_ago = (datetime.now() - timedelta(days=180)).strftime('%Y-%m')
    cursor.execute('''
        SELECT substr(date, 1, 7) as month, SUM(total_cost) as total
        FROM daily_usage
        WHERE user_id = ? AND date >= ?
        GROUP BY month
        ORDER BY month ASC
    ''', (session['user_id'], six_months_ago))
    
    monthly_data = [dict(row) for row in cursor.fetchall()]
    
    # Appliance-wise consumption
    appliance_totals = {}
    for day in daily_data:
        appliances = json.loads(day['appliance_data'])
        for app in appliances:
            name = app['name']
            if name in appliance_totals:
                appliance_totals[name]['units'] += app['units']
                appliance_totals[name]['cost'] += app['cost']
            else:
                appliance_totals[name] = {'units': app['units'], 'cost': app['cost']}
    
    db.close()
    
    return jsonify({
        'daily': daily_data,
        'monthly': monthly_data,
        'appliances': appliance_totals
    })

@app.route('/api/predict-costs')
@login_required
def predict_costs():
    """Predict tomorrow's cost and monthly bill using ML"""
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Get historical data
        cursor.execute('''
            SELECT date, total_cost
            FROM daily_usage
            WHERE user_id = ?
            ORDER BY date ASC
        ''', (session['user_id'],))
        
        historical_data = [dict(row) for row in cursor.fetchall()]
        db.close()
        
        if len(historical_data) < 7:
            return jsonify({
                'success': False,
                'message': 'Need at least 7 days of data for prediction'
            })
        
        predictor = ElectricityPredictor()
        predictions = predictor.predict(historical_data)
        
        return jsonify({
            'success': True,
            'tomorrow_cost': round(predictions['tomorrow'], 2),
            'monthly_estimate': round(predictions['monthly'], 2),
            'confidence': predictions['confidence']
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/ai-suggestions')
@login_required
def get_ai_suggestions():
    """Get AI-powered energy saving suggestions"""
    db = get_db()
    cursor = db.cursor()
    
    # Get recent usage data
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    cursor.execute('''
        SELECT appliance_data, total_cost
        FROM daily_usage
        WHERE user_id = ? AND date >= ?
        ORDER BY date DESC
    ''', (session['user_id'], thirty_days_ago))
    
    recent_data = [dict(row) for row in cursor.fetchall()]
    
    # Get monthly budget
    cursor.execute('SELECT monthly_budget FROM users WHERE id = ?', (session['user_id'],))
    user = cursor.fetchone()
    monthly_budget = user['monthly_budget']
    
    db.close()
    
    suggestions = []
    
    if not recent_data:
        return jsonify([])
    
    # Analyze appliance usage
    appliance_usage = {}
    total_daily_avg = sum(day['total_cost'] for day in recent_data) / len(recent_data)
    
    for day in recent_data:
        appliances = json.loads(day['appliance_data'])
        for app in appliances:
            name = app['name']
            if name in appliance_usage:
                appliance_usage[name]['count'] += 1
                appliance_usage[name]['total_cost'] += app['cost']
                appliance_usage[name]['total_hours'] += app['hours']
            else:
                appliance_usage[name] = {
                    'count': 1,
                    'total_cost': app['cost'],
                    'total_hours': app['hours'],
                    'power': app['power']
                }
    
    # Generate suggestions
    for name, data in appliance_usage.items():
        avg_daily_cost = data['total_cost'] / len(recent_data)
        avg_hours = data['total_hours'] / data['count']
        
        # High power consumption appliances
        if data['power'] > 1500 and avg_hours > 4:
            suggestions.append({
                'type': 'warning',
                'title': f'High Power Device: {name}',
                'message': f'{name} consumes {data["power"]}W and runs {avg_hours:.1f} hours/day on average. Consider reducing usage by 1-2 hours to save ₹{(avg_daily_cost * 0.25 * 30):.2f}/month.',
                'potential_saving': avg_daily_cost * 0.25 * 30
            })
        
        # AC/Heater specific
        if 'AC' in name.upper() or 'AIR CONDITIONER' in name.upper():
            suggestions.append({
                'type': 'info',
                'title': 'AC Optimization',
                'message': f'Set AC to 24-25°C instead of lower temperatures. Use timer function. Potential saving: ₹{(avg_daily_cost * 0.20 * 30):.2f}/month.',
                'potential_saving': avg_daily_cost * 0.20 * 30
            })
        
        # Refrigerator
        if 'FRIDGE' in name.upper() or 'REFRIGERATOR' in name.upper():
            suggestions.append({
                'type': 'tip',
                'title': 'Refrigerator Efficiency',
                'message': 'Keep refrigerator at optimal temperature (3-5°C). Defrost regularly and ensure door seals are tight.',
                'potential_saving': avg_daily_cost * 0.10 * 30
            })
    
    # Budget-based suggestions
    projected_monthly = total_daily_avg * 30
    if projected_monthly > monthly_budget * 0.9:
        suggestions.append({
            'type': 'alert',
            'title': 'Budget Alert',
            'message': f'Current usage projects ₹{projected_monthly:.2f}/month, approaching your budget of ₹{monthly_budget:.2f}. Reduce usage by {((projected_monthly - monthly_budget) / projected_monthly * 100):.1f}%.',
            'potential_saving': projected_monthly - monthly_budget
        })
    
    # General tips
    suggestions.append({
        'type': 'success',
        'title': 'Peak Hour Savings',
        'message': 'Shift heavy appliance usage (washing machine, dishwasher) to off-peak hours (10 PM - 6 AM) if you have time-of-use pricing.',
        'potential_saving': total_daily_avg * 0.15 * 30
    })
    
    suggestions.append({
        'type': 'info',
        'title': 'LED Replacement',
        'message': 'Replace incandescent bulbs with LED lights to reduce lighting costs by up to 75%.',
        'potential_saving': total_daily_avg * 0.10 * 30
    })
    
    # Sort by potential savings
    suggestions.sort(key=lambda x: x.get('potential_saving', 0), reverse=True)
    
    return jsonify(suggestions[:5])  # Return top 5 suggestions

@app.route('/api/download-report/<date>')
@login_required
def download_report(date):
    """Download PDF report for a specific date"""
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Get user info
        cursor.execute('SELECT full_name, email, state, monthly_budget FROM users WHERE id = ?', (session['user_id'],))
        user = cursor.fetchone()
        
        # Get usage data
        cursor.execute('''
            SELECT appliance_data, total_units, total_cost, electricity_rate
            FROM daily_usage
            WHERE user_id = ? AND date = ?
        ''', (session['user_id'], date))
        
        usage = cursor.fetchone()
        
        if not usage:
            db.close()
            return jsonify({'success': False, 'message': 'No data found for this date'})
        
        # Get recent usage for AI suggestions
        thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT appliance_data, total_cost
            FROM daily_usage
            WHERE user_id = ? AND date >= ?
            ORDER BY date DESC
        ''', (session['user_id'], thirty_days_ago))
        
        recent_data = [dict(row) for row in cursor.fetchall()]
        db.close()
        
        # Generate AI suggestions (similar logic to get_ai_suggestions)
        suggestions = []
        if recent_data:
            appliance_usage = {}
            total_daily_avg = sum(day['total_cost'] for day in recent_data) / len(recent_data)
            
            for day in recent_data:
                appliances_list = json.loads(day['appliance_data'])
                for app in appliances_list:
                    name = app['name']
                    if name in appliance_usage:
                        appliance_usage[name]['count'] += 1
                        appliance_usage[name]['total_cost'] += app['cost']
                        appliance_usage[name]['total_hours'] += app['hours']
                    else:
                        appliance_usage[name] = {
                            'count': 1,
                            'total_cost': app['cost'],
                            'total_hours': app['hours'],
                            'power': app['power']
                        }
            
            # High power device warnings
            for name, data in appliance_usage.items():
                avg_daily_cost = data['total_cost'] / len(recent_data)
                avg_hours = data['total_hours'] / data['count']
                
                if data['power'] > 1500 and avg_hours > 4:
                    suggestions.append({
                        'type': 'warning',
                        'title': f'High Power: {name}',
                        'message': f'{name} ({data["power"]}W) runs {avg_hours:.1f}h/day avg. Reduce 1-2h to save.',
                        'potential_saving': avg_daily_cost * 0.25 * 30
                    })
                
                if 'AC' in name.upper():
                    suggestions.append({
                        'type': 'info',
                        'title': 'AC Optimization',
                        'message': f'Set to 24-25°C, use timer. Save up to 20%.',
                        'potential_saving': avg_daily_cost * 0.20 * 30
                    })
            
            # Budget alerts
            projected_monthly = total_daily_avg * 30
            if projected_monthly > user['monthly_budget'] * 0.9:
                suggestions.append({
                    'type': 'alert',
                    'title': 'Budget Alert',
                    'message': f'Projected ₹{projected_monthly:.2f}/month exceeds budget. Reduce usage by {((projected_monthly - user["monthly_budget"]) / projected_monthly * 100):.1f}%.',
                    'potential_saving': projected_monthly - user['monthly_budget']
                })
            
            # General tips
            suggestions.append({
                'type': 'success',
                'title': 'Peak Hour Savings',
                'message': 'Shift heavy appliances to off-peak hours (10 PM - 6 AM).',
                'potential_saving': total_daily_avg * 0.15 * 30
            })
            
            suggestions.sort(key=lambda x: x.get('potential_saving', 0), reverse=True)
        
        # Generate PDF with suggestions
        pdf_path = generate_pdf_report(
            user_name=user['full_name'],
            date=date,
            appliances=json.loads(usage['appliance_data']),
            total_units=usage['total_units'],
            total_cost=usage['total_cost'],
            electricity_rate=usage['electricity_rate'],
            suggestions=suggestions[:5]  # Top 5 suggestions
        )
        
        return send_file(pdf_path, as_attachment=True, download_name=f'electricity_report_{date}.pdf')
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/update-budget', methods=['POST'])
@login_required
def update_budget():
    """Update monthly budget"""
    try:
        data = request.json
        new_budget = float(data['budget'])
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('UPDATE users SET monthly_budget = ? WHERE id = ?', 
                      (new_budget, session['user_id']))
        
        db.commit()
        db.close()
        
        return jsonify({'success': True, 'message': 'Budget updated successfully!'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/electricity-rate')
@login_required
def get_electricity_rate():
    """Get electricity rate for user's state"""
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT state FROM users WHERE id = ?', (session['user_id'],))
    user = cursor.fetchone()
    db.close()
    
    state = user['state'] or 'Default'
    
    # Calculate effective rate for 100 units (for display)
    effective_rate = get_effective_rate(100, state)
    
    return jsonify({
        'state': state,
        'effective_rate': effective_rate,
        'uses_slabs': True
    })

@app.route('/api/calculate-cost', methods=['POST'])
@login_required
def calculate_cost_api():
    """Calculate cost using slab-based tariff"""
    try:
        data = request.json
        units = float(data.get('units', 0))
        
        # Get user's state
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT state FROM users WHERE id = ?', (session['user_id'],))
        user = cursor.fetchone()
        db.close()
        
        state = user['state'] or 'Default'
        
        # Calculate using slab system
        total_cost = calculate_bill(units, state)
        breakdown = get_slab_breakdown(units, state)
        effective_rate = get_effective_rate(units, state)
        
        return jsonify({
            'success': True,
            'cost': total_cost,
            'breakdown': breakdown,
            'effective_rate': effective_rate,
            'state': state
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/appliance-power/<appliance_name>')
def get_appliance_power_api(appliance_name):
    """Get power consumption for an appliance"""
    from models.appliance_power import get_appliance_power
    
    power = get_appliance_power(appliance_name)
    
    if power:
        return jsonify({'success': True, 'power': power, 'appliance': appliance_name})
    else:
        return jsonify({'success': False, 'message': 'Appliance not found'})

@app.route('/api/appliances-list')
def get_appliances_list():
    """Get list of all appliances"""
    from models.appliance_power import get_all_appliances
    
    appliances = get_all_appliances()
    return jsonify({'appliances': appliances})

@app.route('/api/update-profile', methods=['POST'])
@login_required
def update_profile():
    """Update user profile"""
    try:
        data = request.json
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
            UPDATE users SET
                full_name = ?,
                phone = ?,
                house_type = ?,
                city = ?,
                state = ?,
                electricity_board = ?,
                meter_number = ?,
                connection_type = ?,
                monthly_budget = ?
            WHERE id = ?
        ''', (
            data['full_name'],
            data.get('phone', ''),
            data.get('house_type', ''),
            data.get('city', ''),
            data.get('state', ''),
            data.get('electricity_board', ''),
            data.get('meter_number', ''),
            data.get('connection_type', ''),
            data.get('monthly_budget', 1000),
            session['user_id']
        ))
        
        db.commit()
        db.close()
        
        return jsonify({'success': True, 'message': 'Profile updated successfully!'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/upload-profile-picture', methods=['POST'])
@login_required
def upload_profile_picture():
    """Upload profile picture"""
    try:
        if 'profile_picture' not in request.files:
            return jsonify({'success': False, 'message': 'No file provided'})
        
        file = request.files['profile_picture']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'})
        
        # Get user email for filename
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT email FROM users WHERE id = ?', (session['user_id'],))
        user = cursor.fetchone()
        
        # Create filename
        filename = f"{user['email'].replace('@', '_').replace('.', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save file
        file.save(filepath)
        
        # Update database
        cursor.execute('UPDATE users SET profile_picture = ? WHERE id = ?', 
                      (filename, session['user_id']))
        db.commit()
        db.close()
        
        return jsonify({'success': True, 'filename': filename})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/delete-usage/<date>', methods=['DELETE'])
@login_required
def delete_usage(date):
    """Delete usage entry for a specific date"""
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Check if entry exists
        cursor.execute('''
            SELECT id FROM daily_usage 
            WHERE user_id = ? AND date = ?
        ''', (session['user_id'], date))
        
        if not cursor.fetchone():
            db.close()
            return jsonify({'success': False, 'message': 'No data found for this date'})
        
        # Delete the entry
        cursor.execute('''
            DELETE FROM daily_usage 
            WHERE user_id = ? AND date = ?
        ''', (session['user_id'], date))
        
        db.commit()
        db.close()
        
        return jsonify({'success': True, 'message': 'Usage data deleted successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
# Add these routes to your app.py file

@app.route('/api/analytics-daily/<date>')
@login_required
def get_daily_analytics(date):
    """Get analytics for a specific date"""
    try:
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
            SELECT appliance_data, total_units, total_cost
            FROM daily_usage
            WHERE user_id = ? AND date = ?
        ''', (session['user_id'], date))
        
        data = cursor.fetchone()
        db.close()
        
        if not data:
            return jsonify({'error': True, 'message': 'No data for selected date'})
        
        appliances = json.loads(data['appliance_data'])
        
        return jsonify({
            'date': date,
            'appliances': appliances,
            'total_units': data['total_units'],
            'total_cost': data['total_cost']
        })
        
    except Exception as e:
        return jsonify({'error': True, 'message': str(e)})


@app.route('/api/analytics-weekly/<start_date>')
@login_required
def get_weekly_analytics(start_date):
    """Get analytics for a 7-day period"""
    try:
        from datetime import datetime, timedelta
        
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = start + timedelta(days=6)
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
            SELECT date, appliance_data, total_units, total_cost
            FROM daily_usage
            WHERE user_id = ? AND date BETWEEN ? AND ?
            ORDER BY date ASC
        ''', (session['user_id'], start_date, end.strftime('%Y-%m-%d')))
        
        results = cursor.fetchall()
        db.close()
        
        if len(results) < 7:
            return jsonify({
                'error': True,
                'message': f'Only {len(results)} days of data available. Need 7 days for weekly view.'
            })
        
        # Aggregate data
        daily_data = []
        appliance_totals = {}
        
        for row in results:
            daily_data.append({
                'date': row['date'],
                'total_units': row['total_units'],
                'total_cost': row['total_cost']
            })
            
            appliances = json.loads(row['appliance_data'])
            for app in appliances:
                name = app['name']
                if name in appliance_totals:
                    appliance_totals[name]['units'] += app['units']
                    appliance_totals[name]['cost'] += app['cost']
                else:
                    appliance_totals[name] = {
                        'units': app['units'],
                        'cost': app['cost']
                    }
        
        return jsonify({
            'daily': daily_data,
            'appliances': appliance_totals,
            'week_start': start_date,
            'week_end': end.strftime('%Y-%m-%d')
        })
        
    except Exception as e:
        return jsonify({'error': True, 'message': str(e)})


@app.route('/api/analytics-monthly/<month>')
@login_required
def get_monthly_analytics(month):
    """Get analytics for a full month (YYYY-MM format)"""
    try:
        from datetime import datetime
        import calendar
        
        year, month_num = map(int, month.split('-'))
        days_in_month = calendar.monthrange(year, month_num)[1]
        
        start_date = f"{month}-01"
        end_date = f"{month}-{days_in_month:02d}"
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
            SELECT date, appliance_data, total_units, total_cost
            FROM daily_usage
            WHERE user_id = ? AND date BETWEEN ? AND ?
            ORDER BY date ASC
        ''', (session['user_id'], start_date, end_date))
        
        results = cursor.fetchall()
        db.close()
        
        if len(results) < 30:
            return jsonify({
                'error': True,
                'message': f'Only {len(results)} days of data available. Need 30+ days for monthly view.'
            })
        
        # Aggregate data
        daily_data = []
        appliance_totals = {}
        weekly_data = {}
        
        for row in results:
            daily_data.append({
                'date': row['date'],
                'total_units': row['total_units'],
                'total_cost': row['total_cost']
            })
            
            # Get week number
            date_obj = datetime.strptime(row['date'], '%Y-%m-%d')
            week_num = (date_obj.day - 1) // 7 + 1
            week_key = f"Week {week_num}"
            
            if week_key not in weekly_data:
                weekly_data[week_key] = {'units': 0, 'cost': 0}
            
            weekly_data[week_key]['units'] += row['total_units']
            weekly_data[week_key]['cost'] += row['total_cost']
            
            appliances = json.loads(row['appliance_data'])
            for app in appliances:
                name = app['name']
                if name in appliance_totals:
                    appliance_totals[name]['units'] += app['units']
                    appliance_totals[name]['cost'] += app['cost']
                else:
                    appliance_totals[name] = {
                        'units': app['units'],
                        'cost': app['cost']
                    }
        
        return jsonify({
            'daily': daily_data,
            'weekly': weekly_data,
            'appliances': appliance_totals,
            'month': month,
            'total_days': len(results)
        })
        
    except Exception as e:
        return jsonify({'error': True, 'message': str(e)})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)



