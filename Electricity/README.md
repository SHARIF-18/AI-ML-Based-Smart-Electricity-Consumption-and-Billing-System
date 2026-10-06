# Smart Electricity Consumption and Billing System

A comprehensive web-based AI/ML-powered system for tracking, analyzing, predicting, and optimizing daily electricity usage and costs.

## 🌟 Features

### Core Functionality
- **Daily Usage Tracking**: Log appliance usage with automatic unit and cost calculation
- **Budget Monitoring**: Set monthly budgets with real-time progress tracking and alerts
- **Historical Data**: View and download usage history with detailed reports
- **PDF Reports**: Generate professional PDF reports for any date
- **State-wise Pricing**: Accurate calculations based on Indian state electricity rates

### AI/ML Capabilities
- **Cost Prediction**: Machine learning predicts tomorrow's costs and monthly bills
- **Smart Suggestions**: AI-powered energy-saving recommendations based on usage patterns
- **Pattern Analysis**: Identify high-consumption appliances and usage trends

### Analytics Dashboard
- **Daily Cost Trends**: Line charts showing 30-day consumption patterns
- **Monthly Overview**: Bar charts for 6-month spending trends
- **Appliance Analysis**: Pie charts showing consumption by appliance
- **Units vs Cost**: Scatter plots for correlation analysis

### User Experience
- **Modern UI**: Beautiful blue-themed interface with gradient designs
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Smooth Animations**: Engaging animations and transitions
- **Secure Authentication**: Session-based login with encrypted passwords

## 🚀 Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js
- **PDF Generation**: ReportLab
- **Machine Learning**: scikit-learn, numpy, pandas

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Clone or extract the project**
```bash
cd smart_electricity_system
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python app.py
```

4. **Access the application**
Open your browser and navigate to:
```
http://localhost:5000
```

## 📖 Usage Guide

### Getting Started

1. **Sign Up**
   - Navigate to the landing page
   - Click "Get Started" or "Sign Up"
   - Fill in your details:
     - Full Name, Email, Password
     - State (for accurate electricity rates)
     - Optional: Profile picture, phone, house type, etc.
   - Set your monthly budget

2. **Login**
   - Use your email and password to login
   - You'll be redirected to your personalized dashboard

### Dashboard Overview

The dashboard shows:
- Today's electricity cost and units consumed
- Current month's total spending
- Monthly budget and remaining balance
- Budget progress bar with visual indicators
- Alerts when budget limits are approached or exceeded

### Adding Daily Usage

1. Click "Add Today's Usage" or navigate to "Add Usage"
2. Select the date (defaults to today)
3. Add appliances:
   - Enter appliance name (e.g., "LED TV", "Air Conditioner")
   - Enter power consumption in Watts
   - Enter hours and minutes of usage
   - System automatically calculates units and cost
4. Add multiple appliances using the "Add Appliance" button
5. Review totals and click "Save Usage"

**Formula Used:**
- Units (kWh) = (Power in Watts × Hours) ÷ 1000
- Cost (₹) = Units × Electricity Rate

### Viewing History

1. Navigate to "History"
2. View all past usage entries
3. Click the eye icon to view details
4. Click the download icon to get a PDF report

### Analytics

The analytics section provides:
- **Daily Cost Trend**: See how your daily costs vary over the last 30 days
- **Monthly Trends**: Compare spending across the last 6 months
- **Appliance Breakdown**: Identify which appliances consume the most
- **Correlation Analysis**: Understand the relationship between units and cost

### AI Predictions

1. Navigate to "AI Predictions"
2. View predicted costs for tomorrow
3. See estimated monthly bill based on current usage
4. Check prediction confidence score
5. More data = better predictions!

**Note**: Requires at least 7 days of usage data for accurate predictions

### Energy Saving Suggestions

1. Navigate to "Suggestions"
2. View personalized AI-powered recommendations:
   - High power device warnings
   - AC/Heater optimization tips
   - Appliance efficiency suggestions
   - Budget management alerts
   - Time-shifting recommendations
3. Each suggestion shows potential monthly savings

## 🎨 Features in Detail

### State-wise Electricity Rates

The system includes average electricity rates for all Indian states and union territories:
- Rates range from ₹4.50 to ₹8.50 per unit
- Automatically applied based on user's state
- Updated during signup and calculations

### Budget Monitoring

- Set custom monthly budgets
- Real-time progress tracking
- Visual progress bar with color coding:
  - Green: < 80% of budget
  - Orange: 80-100% of budget
  - Red: > 100% (exceeded)
- Automatic alerts when approaching or exceeding limits

### PDF Reports

Professional PDF reports include:
- User information and date
- Detailed appliance breakdown
- Units and cost calculations
- Daily summary totals
- Energy-saving tips
- Professional formatting with tables and styling

### Machine Learning Model

The system uses Random Forest Regression for predictions:
- Features: day number, day of week, day of month, moving averages
- Predicts tomorrow's cost based on historical patterns
- Estimates monthly bill using trend analysis
- Provides confidence score based on R² metric

## 🔒 Security

- Passwords hashed using SHA-256
- Session-based authentication
- Protected routes requiring login
- File uploads validated and stored securely

## 📱 Responsive Design

The application is fully responsive:
- **Desktop**: Full-featured experience with sidebar navigation
- **Tablet**: Optimized layout with collapsible sidebar
- **Mobile**: Touch-friendly interface with hamburger menu

## 🎯 Key Benefits

1. **No More Surprise Bills**: Track daily instead of waiting for monthly bills
2. **Save Money**: AI suggestions help reduce consumption by 20-30%
3. **Budget Control**: Stay within limits with real-time monitoring
4. **Data-Driven Decisions**: Visual analytics reveal usage patterns
5. **Predict Future Costs**: Plan ahead with ML-based predictions
6. **Identify Culprits**: Find out which appliances cost the most

## 🛠️ Project Structure

```
smart_electricity_system/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── models/
│   ├── ml_predictor.py        # Machine learning prediction model
│   ├── pdf_generator.py       # PDF report generation
│   └── state_pricing.py       # State-wise electricity rates
├── templates/
│   ├── index.html             # Landing page
│   ├── login.html             # Login page
│   ├── signup.html            # Signup page
│   └── dashboard.html         # Main dashboard
├── static/
│   ├── css/
│   │   └── style.css          # Comprehensive styling
│   ├── js/
│   │   ├── dashboard.js       # Dashboard functionality
│   │   └── landing.js         # Landing page animations
│   └── images/
│       └── profiles/          # User profile pictures
└── data/
    ├── electricity.db         # SQLite database (auto-created)
    └── reports/               # Generated PDF reports
```

## 🔧 Configuration

### Changing the Secret Key
Edit `app.py` and change:
```python
app.secret_key = 'your-secret-key-change-in-production'
```

### Updating Electricity Rates
Edit `models/state_pricing.py` to update rates:
```python
STATE_ELECTRICITY_RATES = {
    'State Name': rate_per_unit,
    ...
}
```

## 📊 Database Schema

### Users Table
- id, email, password, full_name, phone
- profile_picture, house_type, city, state
- electricity_board, meter_number, connection_type
- monthly_budget, created_at

### Daily Usage Table
- id, user_id, date
- appliance_data (JSON), total_units, total_cost
- electricity_rate, created_at

## 🐛 Troubleshooting

**Issue**: Charts not displaying
- **Solution**: Ensure Chart.js CDN is accessible. Check browser console for errors.

**Issue**: PDF download not working
- **Solution**: Check `data/reports` folder exists and has write permissions.

**Issue**: Predictions show "Need more data"
- **Solution**: Add at least 7 days of usage data.

**Issue**: Cannot upload profile picture
- **Solution**: Ensure `static/images/profiles` folder exists.

## 🚀 Future Enhancements

- Real-time smart meter integration
- Mobile app (iOS/Android)
- Social comparison features
- Gamification and achievements
- Weather-based predictions
- Appliance-specific recommendations
- Multi-user household support
- Export data to Excel/CSV
- Email/SMS notifications
- Integration with electricity boards

## 📄 License

This project is developed for educational and personal use.

## 👨‍💻 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the usage guide
3. Examine browser console for errors

## 🎉 Acknowledgments

- Chart.js for beautiful visualizations
- ReportLab for PDF generation
- scikit-learn for ML capabilities
- Font Awesome for icons

---

**Start tracking your electricity consumption today and save money with AI-powered insights!** 💡⚡💰
