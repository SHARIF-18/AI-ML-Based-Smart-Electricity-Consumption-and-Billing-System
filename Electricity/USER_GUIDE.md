# Smart Electricity System - User Guide

## Quick Start Guide

### Step 1: Installation (5 minutes)

1. **Extract the project folder** to your desired location
2. **Open terminal/command prompt** and navigate to the folder:
   ```bash
   cd path/to/smart_electricity_system
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Or on Linux/Mac:
   ```bash
   pip install --break-system-packages -r requirements.txt
   ```
4. **Start the server**:
   ```bash
   python app.py
   ```
   Or use the startup script:
   ```bash
   ./start.sh
   ```

5. **Open your browser** and visit: `http://localhost:5000`

### Step 2: Create Your Account (2 minutes)

1. Click **"Get Started"** or **"Sign Up"**
2. Fill in the required information:
   - **Full Name**: Your name
   - **Email**: Your email address (used for login)
   - **Password**: Choose a secure password
   - **State**: Select your state (important for accurate electricity rates!)
   - **Monthly Budget**: Set your target monthly budget (default: ₹1000)
3. Optional fields:
   - Upload a profile picture
   - Add phone number
   - Select house type
   - Enter city, electricity board, meter number
4. Click **"Create Account"**

### Step 3: First Login

1. Use your email and password to login
2. You'll see your personalized dashboard!

## Daily Usage Tutorial

### How to Add Your Daily Electricity Usage

**Example: Adding usage for today**

1. **Navigate to "Add Usage"** from the sidebar or click "Add Today's Usage"

2. **The date is already set to today** - you can change it if needed

3. **Add your first appliance** (the form already has one row):
   
   Let's say you used a **TV** today:
   - **Appliance Name**: LED TV
   - **Power (W)**: 100 (check your TV's power rating)
   - **Hours**: 5
   - **Minutes**: 30
   - The system automatically calculates:
     - Units: 0.550 kWh
     - Cost: ₹3.30 (assuming ₹6/unit)

4. **Add more appliances** by clicking "Add Appliance":

   **Refrigerator** (runs all day):
   - Appliance Name: Refrigerator
   - Power: 150W
   - Hours: 24
   - Minutes: 0
   - Auto-calculated: 3.600 kWh, ₹21.60

   **Air Conditioner**:
   - Appliance Name: AC 1.5 Ton
   - Power: 1500W
   - Hours: 8
   - Minutes: 0
   - Auto-calculated: 12.000 kWh, ₹72.00

   **LED Lights** (5 bulbs × 10W each):
   - Appliance Name: LED Lights
   - Power: 50W
   - Hours: 6
   - Minutes: 0
   - Auto-calculated: 0.300 kWh, ₹1.80

5. **Review totals**:
   - Total Units: 16.450 kWh
   - Total Cost: ₹98.70

6. **Click "Save Usage"**

That's it! Your data is saved and reflected in your dashboard.

## Understanding Your Dashboard

### Dashboard Cards Explained

**Today's Cost Card** (Blue)
- Shows how much you've spent TODAY
- Updates immediately when you save usage

**This Month Card** (Green)
- Running total for the current month
- Helps you track progress toward budget

**Monthly Budget Card** (Purple)
- Your set budget
- Click "Edit budget" to change anytime

**Remaining Balance Card** (Changes color)
- Shows how much budget is left
- Green: You're doing great!
- Orange: Getting close to limit
- Red: Budget exceeded - time to cut back!

### Budget Progress Bar

The progress bar shows your spending as a percentage:
- **0-80%**: Green (Safe zone)
- **80-100%**: Orange (Caution zone)
- **100%+**: Red (Alert! Budget exceeded)

## Using History & Reports

### Viewing Past Usage

1. Go to **"History"** section
2. You'll see a list of all dates with usage data
3. Each entry shows:
   - Date
   - Total units consumed
   - Total cost
4. **View Details**: Click the eye icon to see full breakdown
5. **Download PDF**: Click download icon for a professional report

### PDF Reports Include:
- Your name and date
- Complete appliance breakdown with units and costs
- Daily totals
- Electricity rate used
- Energy-saving tips
- Professional formatting

Perfect for:
- Keeping records
- Sharing with family
- Tracking landlord disputes
- Monthly archives

## Analytics Dashboard

### Four Powerful Charts

**1. Daily Cost Trend (Line Chart)**
- Shows last 30 days of spending
- Spot patterns: Are weekends more expensive?
- Identify unusual spikes

**2. Monthly Spending Trend (Bar Chart)**
- Compare last 6 months
- See seasonal variations
- Track improvement over time

**3. Appliance-wise Consumption (Pie Chart)**
- Which appliances cost the most?
- Visual breakdown of your spending
- Helps prioritize what to optimize

**4. Units vs Cost Analysis (Scatter Plot)**
- Understand the correlation
- Verify rate calculations
- Data visualization for nerds!

## AI Predictions Explained

### Tomorrow's Cost Prediction

The system uses **Random Forest Machine Learning** to predict tomorrow's cost based on:
- Your usage patterns
- Day of the week
- Recent trends
- Moving averages

**Accuracy**: Improves with more data (need minimum 7 days)

### Monthly Bill Estimate

Calculates projected total for the month using:
- Current spending
- Remaining days
- Trend analysis
- Your typical patterns

**Use it to**: Plan ahead, adjust usage, avoid bill shock

### Confidence Score

Shows how reliable the prediction is:
- **70-100%**: High confidence (lots of data)
- **50-70%**: Moderate confidence
- **Below 50%**: Need more data

## Smart Suggestions Guide

### Types of Suggestions You'll Get

**1. High Power Device Warnings** (Orange)
- Identifies appliances using >1500W for >4 hours
- Suggests reducing usage time
- Shows potential savings

**2. AC/Heater Optimization** (Blue)
- Temperature recommendations
- Timer usage tips
- Can save 20% on cooling costs

**3. Budget Alerts** (Red)
- Warns when approaching limit
- Calculates needed reduction
- Helps avoid overspending

**4. Peak Hour Savings** (Green)
- Shift heavy usage to off-peak hours
- Applies if you have time-of-use pricing
- Can reduce costs 15-20%

**5. Equipment Upgrades** (Purple)
- LED bulb recommendations
- Energy-efficient appliance suggestions
- Long-term savings calculations

Each suggestion shows **potential monthly savings** in ₹!

## Pro Tips & Best Practices

### For Accurate Tracking

1. **Be Consistent**: Add usage daily, don't skip days
2. **Be Detailed**: Separate appliances (don't group all lights)
3. **Check Power Ratings**: Look at appliance labels for accurate watts
4. **Update Immediately**: Add usage at end of each day while fresh

### To Save Money

1. **Review Analytics Weekly**: Spot trends and adjust
2. **Act on Suggestions**: They're personalized for YOU
3. **Set Realistic Budgets**: Start high, reduce gradually
4. **Use Predictions**: Plan ahead for high-usage days

### Data Quality

**Good practices**:
- ✅ "Living Room AC" instead of just "AC"
- ✅ Accurate power ratings
- ✅ Precise usage hours
- ✅ Daily entries

**Avoid**:
- ❌ Guessing power consumption
- ❌ Rounding hours too much
- ❌ Skipping days
- ❌ Combining multiple items

## Common Questions

**Q: How accurate is the electricity rate?**
A: We use average state-wise rates. Your actual rate may vary by consumption slab. Check your bill!

**Q: Can I edit past entries?**
A: Yes! Just select the date and add usage - it will overwrite the old data.

**Q: Do I need to add every single bulb?**
A: No, you can group similar items: "LED Lights (5 bulbs × 10W = 50W total)"

**Q: What if I forget to add usage for a day?**
A: No problem! Just select that date and add it anytime.

**Q: Why is my remaining balance negative?**
A: You've exceeded your budget. Time to reduce usage or increase budget!

**Q: Can multiple people use one account?**
A: Yes, but currently no user separation. Perfect for one household!

## Troubleshooting

**Problem**: Can't see charts
**Solution**: Check internet connection (Chart.js needs CDN)

**Problem**: Predictions say "need more data"
**Solution**: Add at least 7 days of usage

**Problem**: PDF won't download
**Solution**: Check folder permissions, ensure data/reports exists

**Problem**: Wrong electricity rate
**Solution**: Update your state in profile, or edit rates in state_pricing.py

## Example Usage Scenario

**Meet Priya, a Smart Electricity User:**

**Day 1**: 
- Signs up, sets ₹2000 monthly budget
- Adds usage: ₹85 for the day
- Dashboard shows 4.25% of budget used

**Day 7**:
- Week total: ₹595
- Analytics show AC costs ₹300 (50% of spending!)
- Gets suggestion: "Reduce AC by 2 hours = Save ₹180/month"

**Day 15**:
- Mid-month: ₹1,275 spent (63% of budget)
- Predictions: "Monthly estimate: ₹2,550" (Exceeds budget!)
- Priya reduces AC usage to 6 hours/day

**Day 30**:
- Month end: ₹1,950 (Under budget!)
- Saved ₹50 vs original trajectory
- Downloaded PDF report for records

**Month 2**:
- Using suggestions, brings budget down to ₹1,800
- Saves ₹200 vs Month 1!

## Advanced Features

### State-wise Pricing
We support all 28 states + 8 union territories with accurate rates

### Export Options
Download professional PDFs with complete usage breakdown

### Historical Trends
Track up to 6 months of data with visual comparisons

### Responsive Design
Use on desktop, tablet, or phone - works everywhere!

## Getting Help

1. **Read the README.md** - Comprehensive technical documentation
2. **Check this guide** - Step-by-step instructions
3. **Review code comments** - Well-documented source code
4. **Browser console** - Check for JavaScript errors

## Final Tips

🎯 **Start simple**: Add just 5 appliances the first week
📊 **Use analytics**: Check weekly to spot patterns  
💡 **Follow suggestions**: They're based on YOUR data
💰 **Track savings**: Compare month-to-month to stay motivated
🔄 **Stay consistent**: Daily tracking = accurate predictions

---

**Ready to take control of your electricity bills? Start tracking today!** ⚡💰

Your journey to lower electricity bills begins with the first entry. Good luck! 🚀
