# Installation & Testing Guide

## System Requirements

- **Python**: 3.8 or higher
- **RAM**: 512 MB minimum
- **Storage**: 100 MB
- **Browser**: Chrome, Firefox, Safari, or Edge (latest versions)
- **Internet**: Required for CDN resources (Chart.js, Font Awesome)

## Installation Methods

### Method 1: Automatic Installation (Recommended)

**For Linux/Mac:**
```bash
cd smart_electricity_system
chmod +x start.sh
./start.sh
```

The script will:
- Check Python installation
- Install all dependencies
- Create necessary directories
- Start the Flask server

**For Windows:**
```bash
cd smart_electricity_system
pip install -r requirements.txt
python app.py
```

### Method 2: Manual Installation

**Step 1: Install Dependencies**
```bash
pip install Flask==3.0.0
pip install reportlab==4.0.7
pip install scikit-learn==1.3.2
pip install numpy==1.26.2
pip install pandas==2.1.4
```

Or use requirements.txt:
```bash
pip install -r requirements.txt
```

**Step 2: Create Directories**
```bash
mkdir -p data/reports
mkdir -p static/images/profiles
```

**Step 3: Run Application**
```bash
python app.py
```

The server will start on `http://localhost:5000`

## Verification Steps

### 1. Check Dependencies
```bash
python -c "import flask; print('Flask:', flask.__version__)"
python -c "import reportlab; print('ReportLab:', reportlab.Version)"
python -c "import sklearn; print('scikit-learn:', sklearn.__version__)"
```

Expected output:
```
Flask: 3.0.0
ReportLab: 4.0.7
scikit-learn: 1.3.2
```

### 2. Check Directory Structure
```bash
ls -R smart_electricity_system
```

Should show:
- app.py
- requirements.txt
- models/ (with Python files)
- templates/ (with HTML files)
- static/ (with css, js, images folders)
- data/ (empty initially)

### 3. Check Server
After running `python app.py`, you should see:
```
 * Running on http://127.0.0.1:5000
 * Running on http://localhost:5000
```

## Testing the Application

### Test 1: Landing Page
1. Open browser: `http://localhost:5000`
2. Verify:
   - ✅ Page loads with blue gradient background
   - ✅ Navigation bar visible
   - ✅ "Get Started" button works
   - ✅ Feature cards are visible
   - ✅ Smooth scrolling works

### Test 2: User Registration
1. Click "Get Started" or navigate to `/signup`
2. Fill in the form:
   - Full Name: Test User
   - Email: test@example.com
   - Password: test123
   - State: Select any state (e.g., Maharashtra)
   - Monthly Budget: 1000
3. Click "Create Account"
4. Verify:
   - ✅ Success message appears
   - ✅ Redirected to login page

### Test 3: User Login
1. Navigate to `/login`
2. Enter credentials:
   - Email: test@example.com
   - Password: test123
3. Click "Login"
4. Verify:
   - ✅ Redirected to dashboard
   - ✅ Dashboard loads completely
   - ✅ User name appears in top right
   - ✅ All stats show "0.00" initially

### Test 4: Add Daily Usage
1. Click "Add Today's Usage" or navigate to "Add Usage"
2. Date should be pre-filled with today
3. Add appliances:
   
   **Appliance 1:**
   - Name: LED TV
   - Power: 100
   - Hours: 5
   - Minutes: 0
   
   **Appliance 2:**
   - Name: Refrigerator
   - Power: 150
   - Hours: 24
   - Minutes: 0

4. Click "Save Usage"
5. Verify:
   - ✅ Auto-calculation works (Units and Cost populate)
   - ✅ Totals calculate correctly
   - ✅ Success message appears
   - ✅ Data saves (check dashboard stats update)

**Expected Calculations (assuming ₹6/unit rate):**
- TV: 0.500 kWh, ₹3.00
- Refrigerator: 3.600 kWh, ₹21.60
- **Total: 4.100 kWh, ₹24.60**

### Test 5: Dashboard Statistics
1. Navigate to Dashboard
2. Verify:
   - ✅ Today's Cost shows ₹24.60
   - ✅ Today's Units shows 4.10
   - ✅ Monthly Budget shows ₹1000.00
   - ✅ Month Total shows ₹24.60
   - ✅ Remaining Balance shows ₹975.40
   - ✅ Budget Progress bar shows ~2.5%

### Test 6: Usage History
1. Navigate to "History"
2. Verify:
   - ✅ Today's entry appears
   - ✅ Shows correct units and cost
   - ✅ View (eye icon) button works
   - ✅ Clicking view loads data in Add Usage form

### Test 7: PDF Report Generation
1. In History, click download icon for today's entry
2. Verify:
   - ✅ PDF downloads
   - ✅ Opens in PDF viewer
   - ✅ Shows user name, date
   - ✅ Lists all appliances with details
   - ✅ Shows totals correctly
   - ✅ Professional formatting

### Test 8: Analytics (After Adding 7+ Days)

**Quick Data Setup for Testing:**
Run this test after adding usage for multiple days, or use this Python script to add test data:

```python
import requests

# Add usage for last 7 days
for i in range(7):
    date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
    data = {
        'date': date,
        'appliances': [
            {'name': 'TV', 'power': 100, 'hours': 5, 'units': 0.5, 'cost': 3.0},
            {'name': 'Fridge', 'power': 150, 'hours': 24, 'units': 3.6, 'cost': 21.6}
        ],
        'total_units': 4.1,
        'total_cost': 24.6
    }
    # Note: This requires being logged in
```

**Or manually**: Add usage for 7 different dates through the UI

Then verify Analytics:
- ✅ Daily Cost Trend chart displays
- ✅ Monthly Trend chart displays
- ✅ Appliance breakdown chart displays
- ✅ Units vs Cost chart displays
- ✅ Charts are interactive

### Test 9: AI Predictions (Requires 7+ Days Data)
1. Navigate to "AI Predictions"
2. After adding 7+ days of data, verify:
   - ✅ Tomorrow's cost prediction shows
   - ✅ Monthly estimate shows
   - ✅ Confidence score displays
   - ✅ Progress bar animates
   - ✅ Reasonable predictions (not negative or impossibly high)

### Test 10: AI Suggestions
1. Navigate to "Suggestions"
2. Verify:
   - ✅ Suggestions load
   - ✅ Different types (warning, info, tip, alert, success)
   - ✅ Each has icon, title, message
   - ✅ Potential savings shown
   - ✅ Relevant to your usage data

### Test 11: Budget Alerts
1. Add usage that exceeds 80% of budget
2. Verify:
   - ✅ Orange warning appears at 80%
   - ✅ Progress bar turns orange
   - ✅ Alert banner shows
3. Exceed 100% of budget
4. Verify:
   - ✅ Red alert appears
   - ✅ Progress bar turns red
   - ✅ Remaining balance shows negative with red icon
   - ✅ Alert message updates

### Test 12: Budget Editing
1. Click "Edit budget" on dashboard
2. Enter new value (e.g., 2000)
3. Verify:
   - ✅ Prompt appears
   - ✅ New budget saves
   - ✅ Dashboard updates immediately
   - ✅ Progress bar recalculates

### Test 13: Responsive Design
1. Resize browser window to mobile size (< 768px)
2. Verify:
   - ✅ Sidebar collapses
   - ✅ Hamburger menu appears
   - ✅ Content stacks vertically
   - ✅ Touch-friendly buttons
   - ✅ All features accessible

### Test 14: Logout
1. Click logout button
2. Verify:
   - ✅ Redirected to landing page
   - ✅ Session cleared
   - ✅ Cannot access dashboard without login

## Performance Tests

### Load Time Test
1. Clear browser cache
2. Load landing page
3. Expected: < 2 seconds

### Database Query Test
1. Add 30 days of usage data
2. Load Analytics page
3. Expected: Charts render in < 3 seconds

### PDF Generation Test
1. Generate PDF report
2. Expected: < 2 seconds for generation

## Security Tests

### Test 1: Protected Routes
1. Logout
2. Try accessing `/dashboard` directly
3. Verify: Redirected to login

### Test 2: Password Hashing
1. Check database (if you have SQLite browser)
2. Open `data/electricity.db`
3. View users table
4. Verify: Password is hashed (long string, not plain text)

### Test 3: Session Management
1. Login from one browser
2. Copy session cookie
3. Try using in different browser
4. Should work (session-based auth)

## Troubleshooting Common Issues

### Issue: ImportError: No module named 'flask'
**Solution:**
```bash
pip install flask
```

### Issue: Charts not displaying
**Solution:**
- Check internet connection (Chart.js CDN)
- Check browser console for errors
- Ensure JavaScript is enabled

### Issue: PDF generation fails
**Solution:**
```bash
pip install reportlab
mkdir -p data/reports
chmod 755 data/reports
```

### Issue: Database locked error
**Solution:**
- Close any SQLite browser connections
- Restart Flask server

### Issue: Port 5000 already in use
**Solution:**
Edit app.py, change last line:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue: Static files not loading
**Solution:**
- Check static/ directory structure
- Verify CSS/JS file paths
- Check browser console

## Database Inspection

To view the database:
```bash
sqlite3 data/electricity.db
```

Useful commands:
```sql
.tables                          -- List all tables
.schema users                    -- View users table structure
SELECT * FROM users;             -- View all users
SELECT * FROM daily_usage;       -- View all usage data
.exit                           -- Exit SQLite
```

## Production Deployment Notes

⚠️ **Important**: This is a development setup. For production:

1. **Change Secret Key**:
   ```python
   app.secret_key = 'generate-a-strong-random-key-here'
   ```

2. **Use Production Server**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Enable HTTPS**: Use reverse proxy (nginx) with SSL

4. **Use Production Database**: Consider PostgreSQL or MySQL

5. **Set Debug=False**:
   ```python
   app.run(debug=False)
   ```

## Success Criteria

Your installation is successful if:
- ✅ All dependencies install without errors
- ✅ Server starts without crashes
- ✅ Landing page loads with styling
- ✅ User registration works
- ✅ Login authentication works
- ✅ Daily usage saves correctly
- ✅ Dashboard shows accurate statistics
- ✅ PDF reports generate
- ✅ Charts display (after adding data)
- ✅ Predictions work (after 7+ days data)
- ✅ Suggestions appear
- ✅ No console errors in browser

## Quick Test Checklist

```
□ Python 3.8+ installed
□ Dependencies installed
□ Server starts successfully
□ Landing page loads
□ Signup works
□ Login works
□ Dashboard displays
□ Can add usage
□ Calculations are correct
□ History shows entries
□ PDF downloads
□ Analytics charts display
□ Predictions show (with data)
□ Suggestions load
□ Budget alerts work
□ Logout works
□ Mobile responsive
```

## Next Steps After Testing

1. **Add Real Data**: Start tracking your actual electricity usage
2. **Set Realistic Budget**: Based on your typical consumption
3. **Use Daily**: Best results come from consistent tracking
4. **Review Weekly**: Check analytics and suggestions
5. **Adjust Habits**: Act on AI recommendations
6. **Save Money**: Watch your bills decrease! 💰

---

**Congratulations! Your Smart Electricity System is ready to use!** 🎉

If all tests pass, you're ready to start saving money on your electricity bills!
