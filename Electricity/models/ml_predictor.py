import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import warnings
warnings.filterwarnings('ignore')

class ElectricityPredictor:
    """ML-based electricity cost predictor"""
    
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        
    def predict(self, historical_data):
        """
        Predict tomorrow's cost and monthly estimate
        
        Args:
            historical_data: List of dicts with 'date' and 'total_cost'
            
        Returns:
            dict with 'tomorrow', 'monthly', and 'confidence' predictions
        """
        if len(historical_data) < 7:
            raise ValueError("Need at least 7 days of data")
        
        # Prepare data
        dates = []
        costs = []
        
        for entry in historical_data:
            date_obj = datetime.strptime(entry['date'], '%Y-%m-%d')
            dates.append(date_obj)
            costs.append(entry['total_cost'])
        
        # Sort by date
        sorted_data = sorted(zip(dates, costs), key=lambda x: x[0])
        dates, costs = zip(*sorted_data)
        
        # Create features: day_number, day_of_week, day_of_month
        X = []
        y = []
        
        start_date = dates[0]
        for i, (date, cost) in enumerate(zip(dates, costs)):
            day_number = (date - start_date).days
            day_of_week = date.weekday()  # 0=Monday, 6=Sunday
            day_of_month = date.day
            
            # Add moving average features
            if i >= 3:
                ma_3 = np.mean(costs[i-3:i])
                ma_7 = np.mean(costs[max(0, i-7):i])
            else:
                ma_3 = cost
                ma_7 = cost
            
            X.append([day_number, day_of_week, day_of_month, ma_3, ma_7])
            y.append(cost)
        
        X = np.array(X)
        y = np.array(y)
        
        # Train model
        self.model.fit(X, y)
        
        # Predict tomorrow
        tomorrow_date = dates[-1] + timedelta(days=1)
        tomorrow_features = [
            (tomorrow_date - start_date).days,
            tomorrow_date.weekday(),
            tomorrow_date.day,
            np.mean(costs[-3:]),
            np.mean(costs[-7:])
        ]
        
        tomorrow_cost = self.model.predict([tomorrow_features])[0]
        
        # Calculate monthly estimate
        # Use average of recent predictions
        recent_avg = np.mean(costs[-7:])
        trend_factor = tomorrow_cost / recent_avg if recent_avg > 0 else 1.0
        
        # Estimate remaining days in month
        days_in_month = 30
        current_day = dates[-1].day
        remaining_days = days_in_month - current_day
        
        # Calculate current month spending
        current_month = dates[-1].strftime('%Y-%m')
        current_month_costs = [cost for date, cost in zip(dates, costs) 
                              if date.strftime('%Y-%m') == current_month]
        current_month_total = sum(current_month_costs)
        
        # Estimate total month
        estimated_remaining = remaining_days * recent_avg * trend_factor
        monthly_estimate = current_month_total + estimated_remaining
        
        # Calculate confidence score (R² score)
        from sklearn.metrics import r2_score
        predictions = self.model.predict(X)
        confidence = max(0, min(100, r2_score(y, predictions) * 100))
        
        return {
            'tomorrow': max(0, tomorrow_cost),
            'monthly': max(0, monthly_estimate),
            'confidence': round(confidence, 1)
        }
