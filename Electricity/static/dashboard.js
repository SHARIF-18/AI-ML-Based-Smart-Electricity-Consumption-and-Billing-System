// Global state
let currentSection = 'dashboard';
let electricityRate = 6.0;
let appliances = [];

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    loadUserProfile();
    loadDashboardStats();
    loadElectricityRate();
    
    // Set today's date
    document.getElementById('usageDate').valueAsDate = new Date();
    
    // Add first appliance row
    addApplianceRow();
    
    // Event listeners
    setupEventListeners();
    
    // Load initial data
    loadHistory();
    loadPredictions();
    loadSuggestions();
});

function setupEventListeners() {
    // Navigation
    document.querySelectorAll('.nav-item, .action-btn[data-section]').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const section = this.dataset.section;
            if (section) switchSection(section);
        });
    });
    
    // Menu toggle for mobile
    document.getElementById('menuToggle')?.addEventListener('click', function() {
        document.querySelector('.sidebar').classList.toggle('active');
    });
    
    // Add usage form
    document.getElementById('addApplianceBtn').addEventListener('click', addApplianceRow);
    document.getElementById('clearAllBtn').addEventListener('click', clearAllAppliances);
    document.getElementById('saveUsageBtn').addEventListener('click', saveUsage);
    
    // History refresh
    document.getElementById('refreshHistoryBtn')?.addEventListener('click', loadHistory);
    
    // Predictions refresh
    document.getElementById('refreshPredictionsBtn')?.addEventListener('click', loadPredictions);
    
    // Suggestions refresh
    document.getElementById('refreshSuggestionsBtn')?.addEventListener('click', loadSuggestions);
    
    // Budget edit
    document.getElementById('editBudgetBtn')?.addEventListener('click', editBudget);
    
    // Usage date change
    document.getElementById('usageDate').addEventListener('change', function() {
        loadUsageForDate(this.value);
    });
    
    // Profile section
    document.getElementById('editProfileBtn')?.addEventListener('click', showProfileEdit);
    document.getElementById('cancelEditBtn')?.addEventListener('click', hideProfileEdit);
    document.getElementById('profileEditForm')?.addEventListener('submit', saveProfileChanges);
    document.getElementById('changePictureBtn')?.addEventListener('click', function() {
        document.getElementById('profilePictureInput').click();
    });
    document.getElementById('profilePictureInput')?.addEventListener('change', handleProfilePictureChange);
}
// Add analytics controls
setupAnalyticsControls();
function switchSection(section) {
    currentSection = section;
    
    // Update navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
        if (item.dataset.section === section) {
            item.classList.add('active');
        }
    });
    
    // Update content
    document.querySelectorAll('.content-section').forEach(sec => {
        sec.classList.remove('active');
    });
    document.getElementById(`section-${section}`).classList.add('active');
    
    // Update page title
    const titles = {
        'dashboard': 'Dashboard',
        'add-usage': 'Add Daily Usage',
        'history': 'Usage History',
        'analytics': 'Analytics',
        'predictions': 'AI Predictions',
        'suggestions': 'Energy Saving Tips'
    };
    document.getElementById('pageTitle').textContent = titles[section] || 'Dashboard';
    
    // Load section-specific data
    if (section === 'analytics') {
        loadAnalytics();
    } else if (section === 'predictions') {
        loadPredictions();
    } else if (section === 'suggestions') {
        loadSuggestions();
    } else if (section === 'profile') {
        loadProfileView();
    }
}

async function loadUserProfile() {
    try {
        const response = await fetch('/api/user-profile');
        const user = await response.json();
        
        document.getElementById('userName').textContent = user.full_name;
        
        if (user.profile_picture) {
            document.getElementById('userAvatar').src = `/static/images/profiles/${user.profile_picture}`;
        } else {
            document.getElementById('userAvatar').src = '/static/images/profiles/default.svg';
        }
    } catch (error) {
        console.error('Error loading profile:', error);
        document.getElementById('userName').textContent = 'User';
    }
}

async function loadDashboardStats() {
    try {
        const response = await fetch('/api/dashboard-stats');
        const stats = await response.json();
        
        document.getElementById('todayCost').textContent = stats.today_cost.toFixed(2);
        document.getElementById('todayUnits').textContent = stats.today_units.toFixed(2);
        document.getElementById('monthTotal').textContent = stats.month_total.toFixed(2);
        document.getElementById('monthlyBudget').textContent = stats.monthly_budget.toFixed(2);
        document.getElementById('remainingBalance').textContent = Math.abs(stats.remaining_balance).toFixed(2);
        
        // Update budget progress
        const percentage = Math.min(stats.budget_percentage, 100);
        document.getElementById('budgetProgress').style.width = `${percentage}%`;
        document.getElementById('budgetPercentage').textContent = `${percentage.toFixed(0)}%`;
        
        // Update remaining balance icon and status
        const remainingIcon = document.getElementById('remainingIcon');
        const budgetStatus = document.getElementById('budgetStatus');
        
        if (stats.budget_exceeded) {
            remainingIcon.classList.remove('green', 'orange');
            remainingIcon.classList.add('red');
            budgetStatus.textContent = 'Budget exceeded!';
            budgetStatus.style.color = 'var(--red)';
            
            // Show alert
            const alertBanner = document.getElementById('budgetAlert');
            const alertMessage = document.getElementById('alertMessage');
            alertMessage.textContent = `Warning! You've exceeded your monthly budget by ₹${Math.abs(stats.remaining_balance).toFixed(2)}`;
            alertBanner.style.display = 'flex';
        } else if (stats.budget_percentage > 80) {
            remainingIcon.classList.remove('green', 'red');
            remainingIcon.classList.add('orange');
            budgetStatus.textContent = 'Nearing budget limit';
            budgetStatus.style.color = 'var(--orange)';
            
            const alertBanner = document.getElementById('budgetAlert');
            const alertMessage = document.getElementById('alertMessage');
            alertMessage.textContent = `Caution! You've used ${percentage.toFixed(0)}% of your monthly budget`;
            alertBanner.style.display = 'flex';
            alertBanner.style.background = 'linear-gradient(135deg, var(--orange), var(--orange-light))';
        } else {
            remainingIcon.classList.remove('orange', 'red');
            remainingIcon.classList.add('green');
            budgetStatus.textContent = 'Within budget';
            budgetStatus.style.color = 'var(--green)';
        }
    } catch (error) {
        console.error('Error loading dashboard stats:', error);
    }
}

async function loadElectricityRate() {
    try {
        const response = await fetch('/api/electricity-rate');
        const data = await response.json();
        electricityRate = data.effective_rate || data.rate || 6.0;
        document.getElementById('electricityRate').textContent = `₹${electricityRate.toFixed(2)}/unit`;
    } catch (error) {
        console.error('Error loading electricity rate:', error);
    }
}

// Add Usage Functions
function addApplianceRow() {
    const container = document.getElementById('applianceRows');
    const rowCount = container.children.length + 1;
    const row = document.createElement('div');
    row.className = 'appliance-row';
    row.setAttribute('data-index', rowCount);
    
    row.innerHTML = `
        <div class="input-group appliance-name-group">
            <label><i class="fas fa-plug"></i> Appliance Name *</label>
            <input type="text" class="appliance-name" placeholder="Type to search appliances..." required autocomplete="off">
            <div class="appliance-suggestions" style="display: none;"></div>
        </div>
        <div class="input-group">
            <label><i class="fas fa-bolt"></i> Power (W) <span class="optional-label">(Optional)</span></label>
            <input type="number" class="appliance-power" min="1" placeholder="Auto-filled">
        </div>
        <div class="input-group">
            <label><i class="fas fa-clock"></i> Hours *</label>
            <input type="number" class="appliance-hours" min="0" max="24" value="0" required>
        </div>
        <div class="input-group">
            <label><i class="fas fa-stopwatch"></i> Minutes</label>
            <input type="number" class="appliance-minutes" min="0" max="59" value="0">
        </div>
        <div class="input-group">
            <label><i class="fas fa-tachometer-alt"></i> Units (kWh)</label>
            <input type="text" class="appliance-units" readonly placeholder="Auto">
        </div>
        <div class="input-group">
            <label><i class="fas fa-rupee-sign"></i> Cost (₹)</label>
            <input type="text" class="appliance-cost" readonly placeholder="Auto">
        </div>
        <button type="button" class="remove-row-btn" onclick="removeApplianceRow(this)" title="Remove">
            <i class="fas fa-trash"></i>
        </button>
    `;
    
    container.appendChild(row);
    
    // Add event listeners for calculation
    row.querySelectorAll('input[type="number"]').forEach(input => {
        input.addEventListener('input', calculateRow);
    });
    
    // Add autocomplete functionality
    const nameInput = row.querySelector('.appliance-name');
    const powerInput = row.querySelector('.appliance-power');
    const suggestionsDiv = row.querySelector('.appliance-suggestions');
    
    nameInput.addEventListener('input', async function() {
        const query = this.value.trim();
        
        if (query.length < 2) {
            suggestionsDiv.style.display = 'none';
            return;
        }
        
        try {
            const response = await fetch(`/api/appliance-suggestions?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            
            if (data.suggestions && data.suggestions.length > 0) {
                suggestionsDiv.innerHTML = data.suggestions.map(item => `
                    <div class="suggestion-item-appliance" data-name="${item.name}" data-power="${item.power}">
                        <span class="suggestion-name">${item.name}</span>
                        <span class="suggestion-power">${item.power}W</span>
                    </div>
                `).join('');
                suggestionsDiv.style.display = 'block';
                
                // Add click handlers
                suggestionsDiv.querySelectorAll('.suggestion-item-appliance').forEach(item => {
                    item.addEventListener('click', function() {
                        nameInput.value = this.dataset.name;
                        powerInput.value = this.dataset.power;
                        suggestionsDiv.style.display = 'none';
                        calculateRow({target: powerInput});
                    });
                });
            } else {
                suggestionsDiv.style.display = 'none';
            }
        } catch (error) {
            console.error('Error fetching suggestions:', error);
        }
    });
    
    // Hide suggestions when clicking outside
    nameInput.addEventListener('blur', function() {
        setTimeout(() => {
            suggestionsDiv.style.display = 'none';
        }, 200);
    });
    
    // Try to auto-fill power when name is entered
    nameInput.addEventListener('blur', async function() {
        const name = this.value.trim();
        if (name && !powerInput.value) {
            try {
                const response = await fetch(`/api/appliance-power/${encodeURIComponent(name)}`);
                const data = await response.json();
                if (data.success && data.power) {
                    powerInput.value = data.power;
                    calculateRow({target: powerInput});
                }
            } catch (error) {
                console.error('Error fetching power:', error);
            }
        }
    });
    
    // Update all row numbers
    updateRowNumbers();
}

function updateRowNumbers() {
    const rows = document.querySelectorAll('.appliance-row');
    rows.forEach((row, index) => {
        row.setAttribute('data-index', index + 1);
    });
}

function removeApplianceRow(btn) {
    btn.closest('.appliance-row').remove();
    updateRowNumbers();
    calculateTotals();
}

function clearAllAppliances() {
    if (confirm('Are you sure you want to clear all appliances?')) {
        document.getElementById('applianceRows').innerHTML = '';
        addApplianceRow();
        calculateTotals();
    }
}

function calculateRow(e) {
    const row = e.target.closest('.appliance-row');
    const powerInput = row.querySelector('.appliance-power');
    const power = parseFloat(powerInput.value) || 0;
    const hours = parseFloat(row.querySelector('.appliance-hours').value) || 0;
    const minutes = parseFloat(row.querySelector('.appliance-minutes').value) || 0;
    
    // Show warning if power is missing
    if (!power || power === 0) {
        row.querySelector('.appliance-units').value = '';
        row.querySelector('.appliance-cost').value = '';
        powerInput.style.borderColor = 'var(--orange)';
        powerInput.placeholder = 'Enter power in Watts';
        calculateTotals();
        return;
    } else {
        powerInput.style.borderColor = '';
        powerInput.placeholder = 'Watts';
    }
    
    // Calculate total hours
    const totalHours = hours + (minutes / 60);
    
    // Calculate units: (Power in Watts × Hours) / 1000
    const units = (power * totalHours) / 1000;
    
    row.querySelector('.appliance-units').value = units.toFixed(3);
    row.querySelector('.appliance-cost').value = (units * electricityRate).toFixed(2); // Will be calculated by slab system
    
    calculateTotals();
}

function calculateTotals() {
    let totalUnits = 0;
    
    document.querySelectorAll('.appliance-row').forEach(row => {
        const units = parseFloat(row.querySelector('.appliance-units').value) || 0;
        totalUnits += units;
    });
    
    // Update totals display
    const totalsElement = document.getElementById('totalUnits');
    if (totalsElement) {
        totalsElement.textContent = totalUnits.toFixed(3);
    }
    
    // Calculate cost using slab system via API
    if (totalUnits > 0) {
        fetch('/api/calculate-cost', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({units: totalUnits})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const costElement = document.getElementById('totalCost');
                const rateElement = document.getElementById('electricityRate');
                
                if (costElement) costElement.textContent = data.cost.toFixed(2);
                if (rateElement) rateElement.textContent = data.effective_rate.toFixed(2);
                
                // Store for saving
                window.currentTotalCost = data.cost;
                window.currentEffectiveRate = data.effective_rate;
            }
        })
        .catch(error => console.error('Error calculating cost:', error));
    } else {
        const costElement = document.getElementById('totalCost');
        const rateElement = document.getElementById('electricityRate');
        
        if (costElement) costElement.textContent = '0.00';
        if (rateElement) rateElement.textContent = '0.00';
        
        window.currentTotalCost = 0;
        window.currentEffectiveRate = 0;
    }
}

async function saveUsage() {
    const date = document.getElementById('usageDate').value;
    const rows = document.querySelectorAll('.appliance-row');
    
    if (!date) {
        alert('Please select a date');
        return;
    }
    
    appliances = [];
    let isValid = true;
    let missingPowerAppliances = [];
    
    rows.forEach(row => {
        const name = row.querySelector('.appliance-name').value.trim();
        const powerValue = row.querySelector('.appliance-power').value;
        const power = parseFloat(powerValue);
        const hours = parseFloat(row.querySelector('.appliance-hours').value) || 0;
        const minutes = parseFloat(row.querySelector('.appliance-minutes').value) || 0;
        
        if (!name) {
            isValid = false;
            return;
        }
        
        // Check if power is missing
        if (!power || power === 0) {
            missingPowerAppliances.push(name);
            isValid = false;
            return;
        }
        
        const totalHours = hours + (minutes / 60);
        const units = (power * totalHours) / 1000;
        // Cost will be calculated on backend using slab system
        
        appliances.push({
            name,
            power,
            hours: totalHours,
            units,
            cost: 0  // Placeholder - backend will calculate using slabs
        });
    });
    
    if (!isValid) {
        if (missingPowerAppliances.length > 0) {
            alert(`Please enter power consumption for: ${missingPowerAppliances.join(', ')}\n\nTip: Start typing the appliance name to get suggestions with power values!`);
        } else {
            alert('Please fill in all required fields (Name and Hours are required)');
        }
        return;
    }
    
    if (appliances.length === 0) {
        alert('Please add at least one appliance');
        return;
    }
    
    const totalUnits = appliances.reduce((sum, app) => sum + app.units, 0);
    
    const btn = document.getElementById('saveUsageBtn');
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
    
    try {
        const response = await fetch('/api/save-daily-usage', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                date,
                appliances,
                total_units: totalUnits,
                total_cost: 0  // Backend will calculate using slab system
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert(`Usage saved successfully!\n\nTotal Cost: ₹${data.total_cost.toFixed(2)}\nEffective Rate: ₹${data.effective_rate.toFixed(2)}/unit`);
            loadDashboardStats();
            loadHistory();
        } else {
            alert(data.message || 'Failed to save usage');
        }
    } catch (error) {
        alert('An error occurred while saving');
        console.error(error);
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-save"></i> Save Usage';
    }
}

async function loadUsageForDate(date) {
    try {
        const response = await fetch(`/api/usage-details/${date}`);
        const data = await response.json();
        
        if (data.appliances && data.appliances.length > 0) {
            // Clear existing rows
            document.getElementById('applianceRows').innerHTML = '';
            
            // Add rows for each appliance
            data.appliances.forEach(app => {
                addApplianceRow();
                const rows = document.querySelectorAll('.appliance-row');
                const lastRow = rows[rows.length - 1];
                
                lastRow.querySelector('.appliance-name').value = app.name;
                lastRow.querySelector('.appliance-power').value = app.power;
                const hours = Math.floor(app.hours);
                const minutes = Math.round((app.hours - hours) * 60);
                lastRow.querySelector('.appliance-hours').value = hours;
                lastRow.querySelector('.appliance-minutes').value = minutes;
                lastRow.querySelector('.appliance-units').value = app.units.toFixed(3);
                lastRow.querySelector('.appliance-cost').value = app.cost.toFixed(2);
            });
            
            calculateTotals();
        }
    } catch (error) {
        console.error('Error loading usage for date:', error);
    }
}

// History Functions
async function loadHistory() {
    try {
        const response = await fetch('/api/usage-history');
        const history = await response.json();
        
        const container = document.getElementById('historyList');
        
        if (history.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-inbox"></i>
                    <p>No usage data yet. Start by adding your daily usage!</p>
                </div>
            `;
            return;
        }
        
        container.innerHTML = history.map(item => `
            <div class="history-item">
                <div class="history-date">${formatDate(item.date)}</div>
                <div class="history-stats">
                    <div class="history-stat">
                        <div class="history-stat-label">Units</div>
                        <div class="history-stat-value">${item.total_units.toFixed(2)}</div>
                    </div>
                    <div class="history-stat">
                        <div class="history-stat-label">Cost</div>
                        <div class="history-stat-value">₹${item.total_cost.toFixed(2)}</div>
                    </div>
                </div>
                <div class="history-actions">
                    <button class="icon-btn view" onclick="viewDetails('${item.date}')" title="View Details">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="icon-btn download" onclick="downloadReport('${item.date}')" title="Download PDF">
                        <i class="fas fa-download"></i>
                    </button>
                    <button class="icon-btn delete" onclick="deleteUsage('${item.date}')" title="Delete Entry">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

async function deleteUsage(date) {
    if (!confirm(`Are you sure you want to delete usage data for ${formatDate(date)}?`)) {
        return;
    }
    
    try {
        const response = await fetch(`/api/delete-usage/${date}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('Usage data deleted successfully!');
            loadHistory();
            loadDashboardStats(); // Refresh dashboard
        } else {
            alert(data.message || 'Failed to delete usage data');
        }
    } catch (error) {
        alert('An error occurred while deleting');
        console.error(error);
    }
}

function formatDate(dateStr) {
    const date = new Date(dateStr);
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

function viewDetails(date) {
    document.getElementById('usageDate').value = date;
    loadUsageForDate(date);
    switchSection('add-usage');
}

async function downloadReport(date) {
    try {
        window.location.href = `/api/download-report/${date}`;
    } catch (error) {
        console.error('Error downloading report:', error);
        alert('Failed to download report');
    }
}

// Analytics Functions
// Enhanced Analytics JavaScript
// Add this to your dashboard.js file, replacing the existing analytics functions

// Analytics state
let currentAnalyticsView = 'overview';
let analyticsCharts = {
    chart1: null,
    chart2: null,
    chart3: null,
    chart4: null
};

// Setup analytics controls (add to setupEventListeners function)
function setupAnalyticsControls() {
    const viewType = document.getElementById('analyticsViewType');
    const loadBtn = document.getElementById('loadAnalyticsBtn');
    
    viewType?.addEventListener('change', function() {
        currentAnalyticsView = this.value;
        toggleDateControls(this.value);
    });
    
    loadBtn?.addEventListener('click', loadEnhancedAnalytics);
    
    // Set default dates
    const today = new Date().toISOString().split('T')[0];
    const currentMonth = new Date().toISOString().slice(0, 7);
    
    document.getElementById('analyticsDailyDate').value = today;
    document.getElementById('analyticsWeeklyDate').value = today;
    document.getElementById('analyticsMonthlyDate').value = currentMonth;
}

function toggleDateControls(viewType) {
    document.getElementById('dailyDateControl').style.display = viewType === 'daily' ? 'flex' : 'none';
    document.getElementById('weeklyDateControl').style.display = viewType === 'weekly' ? 'flex' : 'none';
    document.getElementById('monthlyDateControl').style.display = viewType === 'monthly' ? 'flex' : 'none';
}

async function loadEnhancedAnalytics() {
    const viewType = currentAnalyticsView;
    
    // Clear existing charts
    destroyAllCharts();
    
    try {
        let data;
        
        switch(viewType) {
            case 'daily':
                const dailyDate = document.getElementById('analyticsDailyDate').value;
                if (!dailyDate) {
                    alert('Please select a date');
                    return;
                }
                data = await fetchDailyAnalytics(dailyDate);
                renderDailyAnalytics(data);
                break;
                
            case 'weekly':
                const weekStart = document.getElementById('analyticsWeeklyDate').value;
                if (!weekStart) {
                    alert('Please select a week start date');
                    return;
                }
                data = await fetchWeeklyAnalytics(weekStart);
                if (data.error) {
                    alert(data.message);
                    return;
                }
                renderWeeklyAnalytics(data);
                break;
                
            case 'monthly':
                const month = document.getElementById('analyticsMonthlyDate').value;
                if (!month) {
                    alert('Please select a month');
                    return;
                }
                data = await fetchMonthlyAnalytics(month);
                if (data.error) {
                    alert(data.message);
                    return;
                }
                renderMonthlyAnalytics(data);
                break;
                
            case 'overview':
            default:
                data = await fetchOverviewAnalytics();
                renderOverviewAnalytics(data);
                break;
        }
    } catch (error) {
        console.error('Error loading analytics:', error);
        //alert('Failed to load analytics. Please try again.');
    }
}

// Fetch functions
async function fetchDailyAnalytics(date) {
    const response = await fetch(`/api/analytics-daily/${date}`);
    return await response.json();
}

async function fetchWeeklyAnalytics(startDate) {
    const response = await fetch(`/api/analytics-weekly/${startDate}`);
    return await response.json();
}

async function fetchMonthlyAnalytics(month) {
    const response = await fetch(`/api/analytics-monthly/${month}`);
    return await response.json();
}

async function fetchOverviewAnalytics() {
    const response = await fetch('/api/analytics-data');
    return await response.json();
}

// Render functions
f// FIXED ANALYTICS RENDERING FUNCTIONS
// Replace the render functions in analytics_enhanced.js with these:

function renderDailyAnalytics(data) {
    if (!data.appliances || data.appliances.length === 0) {
        showNoDataMessage('No data for selected date');
        return;
    }
    
    document.getElementById('chartTitle1').textContent = `Usage on ${formatDate(data.date)}`;
    document.getElementById('chartTitle2').textContent = 'Hours Used per Appliance';
    document.getElementById('chartTitle3').textContent = 'Appliance Breakdown';
    document.getElementById('chartTitle4').textContent = 'Cost per Appliance';
    
    // Chart 1: Appliance-wise units (BAR CHART)
    const ctx1 = document.getElementById('analyticsChart1');
    if (ctx1) {
        analyticsCharts.chart1 = new Chart(ctx1, {
            type: 'bar',
            data: {
                labels: data.appliances.map(a => a.name),
                datasets: [{
                    label: 'Units (kWh)',
                    data: data.appliances.map(a => a.units),
                    backgroundColor: '#3b82f6',
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: { 
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Units (kWh)'
                        }
                    }
                }
            }
        });
    }
    
    // Chart 2: Hours used (HORIZONTAL BAR)
    const ctx2 = document.getElementById('analyticsChart2');
    if (ctx2) {
        analyticsCharts.chart2 = new Chart(ctx2, {
            type: 'bar',
            data: {
                labels: data.appliances.map(a => a.name),
                datasets: [{
                    label: 'Hours Used',
                    data: data.appliances.map(a => a.hours),
                    backgroundColor: '#10b981',
                    borderRadius: 8
                }]
            },
            options: {
                indexAxis: 'y', // This makes it horizontal
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: { 
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Hours'
                        }
                    }
                }
            }
        });
    }
    
    // Chart 3: Pie chart
    const ctx3 = document.getElementById('analyticsChart3');
    if (ctx3) {
        analyticsCharts.chart3 = new Chart(ctx3, {
            type: 'doughnut',
            data: {
                labels: data.appliances.map(a => a.name),
                datasets: [{
                    data: data.appliances.map(a => a.units),
                    backgroundColor: [
                        '#3b82f6', '#10b981', '#f59e0b', '#ef4444', 
                        '#8b5cf6', '#ec4899', '#06b6d4', '#84cc16'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { 
                        position: 'bottom',
                        labels: {
                            padding: 15,
                            font: { size: 11 }
                        }
                    }
                }
            }
        });
    }
    
    // Chart 4: Cost breakdown (BAR CHART)
    const ctx4 = document.getElementById('analyticsChart4');
    if (ctx4) {
        analyticsCharts.chart4 = new Chart(ctx4, {
            type: 'bar',
            data: {
                labels: data.appliances.map(a => a.name),
                datasets: [{
                    label: 'Cost (₹)',
                    data: data.appliances.map(a => a.cost),
                    backgroundColor: '#f59e0b',
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '₹' + value.toFixed(2);
                            }
                        },
                        title: {
                            display: true,
                            text: 'Cost (₹)'
                        }
                    }
                }
            }
        });
    }
}

function renderWeeklyAnalytics(data) {
    document.getElementById('chartTitle1').textContent = 'Daily Cost Trend (7 Days)';
    document.getElementById('chartTitle2').textContent = 'Daily Units Consumption';
    document.getElementById('chartTitle3').textContent = 'Top Appliances (Week Total)';
    document.getElementById('chartTitle4').textContent = 'Units vs Cost Comparison';
    
    // Chart 1: Daily cost line chart
    const ctx1 = document.getElementById('analyticsChart1');
    if (ctx1) {
        analyticsCharts.chart1 = new Chart(ctx1, {
            type: 'line',
            data: {
                labels: data.daily.map(d => formatDateShort(d.date)),
                datasets: [{
                    label: 'Daily Cost (₹)',
                    data: data.daily.map(d => d.total_cost),
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { display: true }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '₹' + value;
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Chart 2: Daily units bar chart
    const ctx2 = document.getElementById('analyticsChart2');
    if (ctx2) {
        analyticsCharts.chart2 = new Chart(ctx2, {
            type: 'bar',
            data: {
                labels: data.daily.map(d => formatDateShort(d.date)),
                datasets: [{
                    label: 'Units (kWh)',
                    data: data.daily.map(d => d.total_units),
                    backgroundColor: '#10b981',
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { display: true }
                },
                scales: {
                    y: { 
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Units (kWh)'
                        }
                    }
                }
            }
        });
    }
    
    // Chart 3: Top appliances pie chart
    const topAppliances = Object.entries(data.appliances)
        .sort((a, b) => b[1].cost - a[1].cost)
        .slice(0, 6);
    
    const ctx3 = document.getElementById('analyticsChart3');
    if (ctx3) {
        analyticsCharts.chart3 = new Chart(ctx3, {
            type: 'doughnut',
            data: {
                labels: topAppliances.map(a => a[0]),
                datasets: [{
                    data: topAppliances.map(a => a[1].cost),
                    backgroundColor: [
                        '#3b82f6', '#10b981', '#f59e0b', 
                        '#ef4444', '#8b5cf6', '#ec4899'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { 
                        position: 'bottom',
                        labels: {
                            padding: 10,
                            font: { size: 11 }
                        }
                    }
                }
            }
        });
    }
    
    // Chart 4: Dual axis - units and cost
    const ctx4 = document.getElementById('analyticsChart4');
    if (ctx4) {
        analyticsCharts.chart4 = new Chart(ctx4, {
            type: 'bar',
            data: {
                labels: data.daily.map(d => formatDateShort(d.date)),
                datasets: [
                    {
                        label: 'Units (kWh)',
                        data: data.daily.map(d => d.total_units),
                        backgroundColor: '#3b82f6',
                        yAxisID: 'y',
                        order: 2
                    },
                    {
                        label: 'Cost (₹)',
                        data: data.daily.map(d => d.total_cost),
                        type: 'line',
                        borderColor: '#f59e0b',
                        backgroundColor: 'rgba(245, 158, 11, 0.1)',
                        yAxisID: 'y1',
                        order: 1,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                scales: {
                    y: {
                        type: 'linear',
                        position: 'left',
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Units (kWh)'
                        }
                    },
                    y1: {
                        type: 'linear',
                        position: 'right',
                        beginAtZero: true,
                        grid: {
                            drawOnChartArea: false
                        },
                        title: {
                            display: true,
                            text: 'Cost (₹)'
                        }
                    }
                }
            }
        });
    }
}

function renderOverviewAnalytics(data) {
    if (!data.daily || data.daily.length === 0) {
        showNoDataMessage('No usage data available. Add some usage data to see analytics.');
        return;
    }
    
    document.getElementById('chartTitle1').textContent = 'Last 30 Days Cost Trend';
    document.getElementById('chartTitle2').textContent = 'Monthly Summary';
    document.getElementById('chartTitle3').textContent = 'Appliance Breakdown';
    document.getElementById('chartTitle4').textContent = 'Units vs Cost Analysis';
    
    // Chart 1: Daily cost trend
    const ctx1 = document.getElementById('analyticsChart1');
    if (ctx1) {
        analyticsCharts.chart1 = new Chart(ctx1, {
            type: 'line',
            data: {
                labels: data.daily.map(d => formatDateShort(d.date)),
                datasets: [{
                    label: 'Daily Cost (₹)',
                    data: data.daily.map(d => d.total_cost),
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: { 
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: value => '₹' + value
                        }
                    }
                }
            }
        });
    }
    
    // Chart 2: Monthly trend
    const ctx2 = document.getElementById('analyticsChart2');
    if (ctx2 && data.monthly) {
        analyticsCharts.chart2 = new Chart(ctx2, {
            type: 'bar',
            data: {
                labels: data.monthly.map(d => formatMonth(d.month)),
                datasets: [{
                    label: 'Monthly Total (₹)',
                    data: data.monthly.map(d => d.total),
                    backgroundColor: '#3b82f6',
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: value => '₹' + value
                        }
                    }
                }
            }
        });
    }
    
    // Chart 3: Appliance breakdown
    const ctx3 = document.getElementById('analyticsChart3');
    if (ctx3 && data.appliances) {
        const labels = Object.keys(data.appliances);
        const costs = labels.map(name => data.appliances[name].cost);
        
        analyticsCharts.chart3 = new Chart(ctx3, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: costs,
                    backgroundColor: [
                        '#3b82f6', '#10b981', '#8b5cf6', '#f59e0b', 
                        '#ef4444', '#06b6d4', '#ec4899', '#84cc16'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 10,
                            font: { size: 11 }
                        }
                    }
                }
            }
        });
    }
    
    // Chart 4: Scatter plot
    const ctx4 = document.getElementById('analyticsChart4');
    if (ctx4) {
        analyticsCharts.chart4 = new Chart(ctx4, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Units vs Cost',
                    data: data.daily.map(d => ({
                        x: d.total_units,
                        y: d.total_cost
                    })),
                    backgroundColor: '#3b82f6',
                    pointRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Units (kWh)'
                        },
                        beginAtZero: true
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Cost (₹)'
                        },
                        beginAtZero: true
                    }
                }
            }
        });
    }
}

function formatMonth(monthStr) {
    const [year, month] = monthStr.split('-');
    const date = new Date(year, month - 1);
    return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
}


// Helper functions
function destroyAllCharts() {
    Object.values(analyticsCharts).forEach(chart => {
        if (chart) chart.destroy();
    });
    analyticsCharts = { chart1: null, chart2: null, chart3: null, chart4: null };
}

function showNoDataMessage(message) {
    document.getElementById('analyticsChartsContainer').innerHTML = `
        <div class="card" style="grid-column: 1 / -1;">
            <div class="empty-state">
                <i class="fas fa-chart-bar" style="font-size: 4rem; color: var(--primary-blue); opacity: 0.3;"></i>
                <h3>No Data Available</h3>
                <p>${message}</p>
            </div>
        </div>
    `;
}

function formatDateShort(dateStr) {
    const date = new Date(dateStr);
    return `${date.getMonth() + 1}/${date.getDate()}`;
}

function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
}

// Update the existing createDailyCostChart, createMonthlyTrendChart, etc. to accept canvas ID
function createDailyCostChart(dailyData, canvasId) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    analyticsCharts.chart1 = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dailyData.map(d => formatDateShort(d.date)),
            datasets: [{
                label: 'Daily Cost (₹)',
                data: dailyData.map(d => d.total_cost),
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: { legend: { display: false } },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { callback: value => '₹' + value }
                }
            }
        }
    });
}

// Similar updates for other chart functions...

// Predictions Functions
async function loadPredictions() {
    try {
        const response = await fetch('/api/predict-costs');
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('tomorrowPrediction').textContent = data.tomorrow_cost.toFixed(2);
            document.getElementById('monthlyPrediction').textContent = data.monthly_estimate.toFixed(2);
            
            const confidence = data.confidence;
            document.getElementById('confidenceFill').style.width = `${confidence}%`;
            document.getElementById('confidenceLabel').textContent = `${confidence.toFixed(0)}% Confident`;
            
            document.getElementById('tomorrowInfo').textContent = 
                `Based on your recent usage patterns`;
            document.getElementById('monthlyInfo').textContent = 
                `Estimated total for this month`;
        } else {
            document.getElementById('tomorrowInfo').textContent = data.message;
            document.getElementById('monthlyInfo').textContent = 
                'Keep adding daily usage data to improve predictions';
        }
    } catch (error) {
        console.error('Error loading predictions:', error);
    }
}

// Suggestions Functions
async function loadSuggestions() {
    console.log('Loading suggestions...');
    
    const container = document.getElementById('suggestionsList');
    
    // Show loading state
    container.innerHTML = `
        <div class="empty-state">
            <i class="fas fa-spinner fa-spin" style="font-size: 3rem; color: var(--primary-blue);"></i>
            <p>Generating personalized suggestions...</p>
        </div>
    `;
    
    try {
        const response = await fetch('/api/ai-suggestions');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const suggestions = await response.json();
        console.log('Suggestions received:', suggestions);
        
        if (suggestions.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-lightbulb" style="font-size: 4rem; color: var(--orange); opacity: 0.3;"></i>
                    <h3>No Suggestions Yet</h3>
                    <p>Add more usage data to get personalized recommendations!</p>
                    <button class="btn-primary" data-section="add-usage" onclick="switchSection('add-usage')">
                        <i class="fas fa-plus-circle"></i> Add Usage Now
                    </button>
                </div>
            `;
            return;
        }
        
        container.innerHTML = suggestions.map(item => `
            <div class="suggestion-item ${item.type}">
                <div class="suggestion-icon">
                    <i class="fas fa-${getIconForType(item.type)}"></i>
                </div>
                <div class="suggestion-content">
                    <div class="suggestion-title">${item.title}</div>
                    <div class="suggestion-message">${item.message}</div>
                    ${item.potential_saving ? `
                        <div class="suggestion-saving">
                            💰 Potential Monthly Savings: ₹${item.potential_saving.toFixed(2)}
                        </div>
                    ` : ''}
                </div>
            </div>
        `).join('');
        
        console.log('Suggestions loaded successfully');
        
    } catch (error) {
        console.error('Error loading suggestions:', error);
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-exclamation-triangle" style="font-size: 4rem; color: var(--red); opacity: 0.5;"></i>
                <h3>Error Loading Suggestions</h3>
                <p>${error.message}</p>
                <button class="btn-primary" onclick="loadSuggestions()">
                    <i class="fas fa-sync"></i> Try Again
                </button>
            </div>
        `;
    }
}

function getIconForType(type) {
    const icons = {
        'warning': 'exclamation-triangle',
        'info': 'info-circle',
        'tip': 'lightbulb',
        'alert': 'bell',
        'success': 'check-circle'
    };
    return icons[type] || 'info-circle';
}

async function editBudget() {
    const currentBudget = parseFloat(document.getElementById('monthlyBudget').textContent);
    const newBudget = prompt('Enter new monthly budget (₹):', currentBudget);
    
    if (newBudget && !isNaN(newBudget) && newBudget > 0) {
        try {
            const response = await fetch('/api/update-budget', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ budget: parseFloat(newBudget) })
            });
            
            const data = await response.json();
            
            if (data.success) {
                alert('Budget updated successfully!');
                loadDashboardStats();
            } else {
                alert(data.message || 'Failed to update budget');
            }
        } catch (error) {
            alert('An error occurred');
            console.error(error);
        }
    }
}

// Profile Functions
async function loadProfileView() {
    try {
        const response = await fetch('/api/user-profile');
        const user = await response.json();
        
        // Update profile view
        document.getElementById('profileFullName').textContent = user.full_name;
        document.getElementById('profileEmail').textContent = user.email;
        document.getElementById('profilePhone').textContent = user.phone || '-';
        document.getElementById('profileHouseType').textContent = user.house_type || '-';
        document.getElementById('profileCity').textContent = user.city || '-';
        document.getElementById('profileState').textContent = user.state || '-';
        document.getElementById('profileBoard').textContent = user.electricity_board || '-';
        document.getElementById('profileMeter').textContent = user.meter_number || '-';
        document.getElementById('profileConnection').textContent = user.connection_type || '-';
        document.getElementById('profileBudget').textContent = user.monthly_budget ? `₹${user.monthly_budget.toFixed(2)}` : '-';
        
        // Update profile picture
        if (user.profile_picture) {
            document.getElementById('profilePictureLarge').src = `/static/images/profiles/${user.profile_picture}`;
        }
        
        // Store user data for editing
        window.currentUserData = user;
    } catch (error) {
        console.error('Error loading profile:', error);
    }
}

function showProfileEdit() {
    const user = window.currentUserData;
    if (!user) return;
    
    // Populate edit form
    document.getElementById('editFullName').value = user.full_name;
    document.getElementById('editEmail').value = user.email;
    document.getElementById('editPhone').value = user.phone || '';
    document.getElementById('editHouseType').value = user.house_type || '';
    document.getElementById('editCity').value = user.city || '';
    document.getElementById('editState').value = user.state || '';
    document.getElementById('editBoard').value = user.electricity_board || '';
    document.getElementById('editMeter').value = user.meter_number || '';
    document.getElementById('editConnection').value = user.connection_type || '';
    document.getElementById('editMonthlyBudget').value = user.monthly_budget || 1000;
    
    // Toggle views
    document.getElementById('profileView').style.display = 'none';
    document.getElementById('profileEditForm').style.display = 'block';
    document.getElementById('editProfileBtn').style.display = 'none';
}

function hideProfileEdit() {
    document.getElementById('profileView').style.display = 'block';
    document.getElementById('profileEditForm').style.display = 'none';
    document.getElementById('editProfileBtn').style.display = 'block';
}

async function saveProfileChanges(e) {
    e.preventDefault();
    
    const updatedData = {
        full_name: document.getElementById('editFullName').value,
        email: document.getElementById('editEmail').value,
        phone: document.getElementById('editPhone').value,
        house_type: document.getElementById('editHouseType').value,
        city: document.getElementById('editCity').value,
        state: document.getElementById('editState').value,
        electricity_board: document.getElementById('editBoard').value,
        meter_number: document.getElementById('editMeter').value,
        connection_type: document.getElementById('editConnection').value,
        monthly_budget: parseFloat(document.getElementById('editMonthlyBudget').value)
    };
    
    try {
        const response = await fetch('/api/update-profile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updatedData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('Profile updated successfully!');
            hideProfileEdit();
            loadProfileView();
            loadUserProfile(); // Update top bar
            loadDashboardStats(); // Update stats if budget changed
        } else {
            alert(data.message || 'Failed to update profile');
        }
    } catch (error) {
        alert('An error occurred while updating profile');
        console.error(error);
    }
}

async function handleProfilePictureChange(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    // Preview
    const reader = new FileReader();
    reader.onload = function(e) {
        document.getElementById('profilePictureLarge').src = e.target.result;
    };
    reader.readAsDataURL(file);
    
    // Upload
    const formData = new FormData();
    formData.append('profile_picture', file);
    
    try {
        const response = await fetch('/api/upload-profile-picture', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('Profile picture updated!');
            loadUserProfile(); // Update top bar
            loadProfileView(); // Refresh profile
        } else {
            alert(data.message || 'Failed to upload picture');
        }
    } catch (error) {
        alert('An error occurred while uploading');
        console.error(error);
    }
}