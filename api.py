<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MoMo Analytics Dashboard</title>
    <!-- Add Chart.js -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.min.js"></script>
    <!-- Add Date Range Picker -->
    <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/daterangepicker/3.1.0/daterangepicker.css" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.4/moment.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/daterangepicker/3.1.0/daterangepicker.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f8f9fa;
            min-height: 100vh;
        }

        /* Header */
        .header {
            background: #198536;
            padding: 1rem 0;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .nav-container {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 1rem;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .logo-icon {
            width: 40px;
            height: 40px;
            background: #ffcc00;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            color: #1e3a5f;
            font-size: 1.2rem;
        }

        .logo-text {
            color: #ffcc00;
            font-size: 1.5rem;
            font-weight: bold;
        }

        /* Dashboard Content */
        .dashboard {
            margin-top: 80px;
            padding: 1rem;
            min-height: calc(100vh - 80px);
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            width: 100%;
        }

        /* Search and Filter Panel */
        .search-panel {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }

        .search-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            align-items: end;
        }

        .search-item {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .search-item label {
            font-weight: 600;
            color: #1e3a5f;
            font-size: 0.9rem;
        }

        .search-item input,
        .search-item select {
            padding: 0.75rem;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 0.9rem;
            width: 100%;
            transition: border-color 0.3s, box-shadow 0.3s;
        }

        .search-item input:focus,
        .search-item select:focus {
            outline: none;
            border-color: #198536;
            box-shadow: 0 0 0 2px rgba(25, 133, 54, 0.1);
        }

        /* Charts Grid */
        .charts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }

        .chart-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            min-height: 380px;
        }

        .chart-card h3 {
            color: #1e3a5f;
            margin-bottom: 1rem;
            font-size: 1.1rem;
        }

        .chart-container {
            position: relative;
            height: 300px;
            width: 100%;
        }

        .chart-container canvas {
            max-width: 100%;
            height: auto !important;
        }

        /* Transaction List */
        .transaction-list {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            overflow-x: auto;
        }

        .transaction-list h3 {
            color: #1e3a5f;
            margin-bottom: 1rem;
        }

        .transaction-item {
            padding: 1rem;
            border-bottom: 1px solid #eee;
            cursor: pointer;
            transition: background-color 0.3s;
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 1rem;
            align-items: center;
        }

        .transaction-item:hover {
            background-color: #f8f9fa;
        }

        .transaction-item:last-child {
            border-bottom: none;
        }

        .transaction-info {
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }

        .transaction-amount {
            font-weight: bold;
            color: #198536;
        }

        .transaction-details {
            font-size: 0.9rem;
            color: #666;
        }

        /* Modal */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 2000;
            padding: 1rem;
        }

        .modal-content {
            position: relative;
            background: white;
            width: 100%;
            max-width: 600px;
            margin: 2rem auto;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            max-height: calc(100vh - 4rem);
            overflow-y: auto;
        }

        .close-modal {
            position: absolute;
            top: 1rem;
            right: 1rem;
            font-size: 1.5rem;
            cursor: pointer;
            color: #666;
            background: none;
            border: none;
            padding: 0.25rem;
            line-height: 1;
        }

        .close-modal:hover {
            color: #333;
        }

        /* Loading State */
        .loading {
            text-align: center;
            padding: 2rem;
            color: #666;
        }

        /* Error State */
        .error {
            text-align: center;
            padding: 2rem;
            color: #dc3545;
            background: #fff5f5;
            border: 1px solid #fecaca;
            border-radius: 12px;
            margin: 1rem 0;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .dashboard {
                padding: 0.5rem;
                margin-top: 70px;
            }

            .nav-container {
                padding: 0 1rem;
            }

            .logo-text {
                font-size: 1.2rem;
            }

            .logo-icon {
                width: 35px;
                height: 35px;
                font-size: 1rem;
            }

            .search-panel {
                padding: 1rem;
            }

            .search-grid {
                grid-template-columns: 1fr;
                gap: 1rem;
            }

            .charts-grid {
                grid-template-columns: 1fr;
                gap: 1rem;
            }

            .chart-card {
                padding: 1rem;
                min-height: 320px;
            }

            .chart-container {
                height: 250px;
            }

            .transaction-list {
                padding: 1rem;
            }

            .transaction-item {
                grid-template-columns: 1fr;
                text-align: left;
            }

            .modal-content {
                margin: 1rem auto;
                padding: 1.5rem;
            }
        }

        @media (max-width: 480px) {
            .search-grid {
                grid-template-columns: 1fr;
            }

            .chart-container {
                height: 200px;
            }

            .transaction-item {
                padding: 0.75rem;
            }

            .logo-text {
                display: none;
            }
        }

        /* Utility Classes */
        .text-center {
            text-align: center;
        }

        .hidden {
            display: none !important;
        }

        .visible {
            display: block !important;
        }

        /* Better button styling for interactive elements */
        button, .btn {
            background: #198536;
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9rem;
            transition: background-color 0.3s;
        }

        button:hover, .btn:hover {
            background: #146b2a;
        }

        /* Accessibility improvements */
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }

        /* Focus indicators for keyboard navigation */
        *:focus {
            outline: 2px solid #198536;
            outline-offset: 2px;
        }
    </style>
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="nav-container">
            <div class="logo">
                <div class="logo-icon" aria-label="MoMo Analytics Logo">△</div>
                <div class="logo-text">MoMo Analytics</div>
            </div>
        </div>
    </header>

    <!-- Dashboard Content -->
    <main class="dashboard">
        <div class="container">
            <!-- Search and Filter Panel -->
            <section class="search-panel" aria-label="Search and Filter Options">
                <div class="search-grid">
                    <div class="search-item">
                        <label for="search">Search</label>
                        <input type="text" id="search" placeholder="Search transactions..." aria-describedby="search-help">
                        <small id="search-help" class="sr-only">Search by transaction ID, amount, or description</small>
                    </div>
                    <div class="search-item">
                        <label for="type">Transaction Type</label>
                        <select id="type" aria-describedby="type-help">
                            <option value="">All Types</option>
                            <option value="1">Incoming</option>
                            <option value="2">Payment</option>
                            <option value="3">Bill</option>
                            <option value="4">Deposit</option>
                            <option value="5">Airtime</option>
                            <option value="6">Cash Power</option>
                            <option value="7">Withdrawal</option>
                            <option value="8">OTP</option>
                        </select>
                        <small id="type-help" class="sr-only">Filter transactions by type</small>
                    </div>
                    <div class="search-item">
                        <label for="date-range">Date Range</label>
                        <input type="text" id="date-range" placeholder="Select date range" aria-describedby="date-help">
                        <small id="date-help" class="sr-only">Select start and end date for filtering</small>
                    </div>
                </div>
            </section>

            <!-- Charts Grid -->
            <section class="charts-grid" aria-label="Analytics Charts">
                <div class="chart-card">
                    <h3>Transaction Volume by Type</h3>
                    <div class="chart-container">
                        <canvas id="volumeChart" aria-label="Chart showing transaction volume by type"></canvas>
                    </div>
                </div>
                <div class="chart-card">
                    <h3>Monthly Transaction Summary</h3>
                    <div class="chart-container">
                        <canvas id="monthlyChart" aria-label="Chart showing monthly transaction summary"></canvas>
                    </div>
                </div>
                <div class="chart-card">
                    <h3>Deposits vs Withdrawals</h3>
                    <div class="chart-container">
                        <canvas id="distributionChart" aria-label="Chart showing deposits versus withdrawals"></canvas>
                    </div>
                </div>
                <div class="chart-card">
                    <h3>Top Transaction Types</h3>
                    <div class="chart-container">
                        <canvas id="topTypesChart" aria-label="Chart showing top transaction types"></canvas>
                    </div>
                </div>
            </section>

            <!-- Transaction List -->
            <section class="transaction-list" aria-label="Recent Transactions">
                <h3>Recent Transactions</h3>
                <div id="transactions" role="list">
                    <div class="loading" id="loading" aria-live="polite">Loading transactions...</div>
                    <div id="error-message" class="error hidden" role="alert" aria-live="assertive"></div>
                </div>
            </section>
        </div>
    </main>

    <!-- Transaction Detail Modal -->
    <div id="transactionModal" class="modal" role="dialog" aria-labelledby="modal-title" aria-hidden="true">
        <div class="modal-content">
            <button class="close-modal" aria-label="Close transaction details">×</button>
            <h2 id="modal-title">Transaction Details</h2>
            <div id="transactionDetails" role="main"></div>
        </div>
    </div>

    <script>
        // Mock dashboard functionality since dashboard.js is not provided
        document.addEventListener('DOMContentLoaded', function() {
            // Initialize date range picker
            $('#date-range').daterangepicker({
                startDate: moment().subtract(29, 'days'),
                endDate: moment(),
                ranges: {
                   'Today': [moment(), moment()],
                   'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                   'Last 7 Days': [moment().subtract(6, 'days'), moment()],
                   'Last 30 Days': [moment().subtract(29, 'days'), moment()],
                   'This Month': [moment().startOf('month'), moment().endOf('month')],
                   'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
                }
            });

            // Mock chart data
            const chartColors = {
                primary: '#198536',
                secondary: '#ffcc00',
                tertiary: '#1e3a5f',
                quaternary: '#dc3545',
                quinary: '#6c757d'
            };

            // Initialize charts with sample data
            initializeCharts();

            // Load sample transactions
            loadSampleTransactions();

            // Modal functionality
            const modal = document.getElementById('transactionModal');
            const closeModal = document.querySelector('.close-modal');

            closeModal.addEventListener('click', () => {
                modal.style.display = 'none';
                modal.setAttribute('aria-hidden', 'true');
            });

            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.style.display = 'none';
                    modal.setAttribute('aria-hidden', 'true');
                }
            });

            // Escape key to close modal
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && modal.style.display === 'block') {
                    modal.style.display = 'none';
                    modal.setAttribute('aria-hidden', 'true');
                }
            });
        });

        function initializeCharts() {
            // Volume Chart
            const volumeCtx = document.getElementById('volumeChart').getContext('2d');
            new Chart(volumeCtx, {
                type: 'bar',
                data: {
                    labels: ['Incoming', 'Payment', 'Bill', 'Deposit', 'Airtime', 'Cash Power', 'Withdrawal'],
                    datasets: [{
                        label: 'Transaction Count',
                        data: [120, 89, 45, 78, 156, 67, 234],
                        backgroundColor: '#198536',
                        borderColor: '#146b2a',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

            // Monthly Chart
            const monthlyCtx = document.getElementById('monthlyChart').getContext('2d');
            new Chart(monthlyCtx, {
                type: 'line',
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                    datasets: [{
                        label: 'Transactions',
                        data: [450, 520, 480, 670, 580, 720],
                        borderColor: '#198536',
                        backgroundColor: 'rgba(25, 133, 54, 0.1)',
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });

            // Distribution Chart
            const distributionCtx = document.getElementById('distributionChart').getContext('2d');
            new Chart(distributionCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Deposits', 'Withdrawals'],
                    datasets: [{
                        data: [65, 35],
                        backgroundColor: ['#198536', '#ffcc00'],
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });

            // Top Types Chart
            const topTypesCtx = document.getElementById('topTypesChart').getContext('2d');
            new Chart(topTypesCtx, {
                type: 'pie',
                data: {
                    labels: ['Withdrawal', 'Airtime', 'Incoming', 'Payment', 'Deposit'],
                    datasets: [{
                        data: [234, 156, 120, 89, 78],
                        backgroundColor: ['#198536', '#ffcc00', '#1e3a5f', '#dc3545', '#6c757d']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        }

        function loadSampleTransactions() {
            const loading = document.getElementById('loading');
            const transactionsContainer = document.getElementById('transactions');
            
            // Hide loading immediately and show static data
            loading.style.display = 'none';
            
            // Generate 1600 sample transactions
            const sampleTransactions = [];
            const transactionTypes = ['Withdrawal', 'Airtime', 'Deposit', 'Payment', 'Bill', 'Incoming', 'Cash Power', 'OTP'];
            const statuses = ['Completed', 'Pending', 'Failed'];
            const descriptions = {
                'Withdrawal': ['ATM Withdrawal - Kimisagara', 'ATM Withdrawal - Nyabugogo', 'ATM Withdrawal - City Center', 'Cash Out - Agent 12345', 'Cash Out - Agent 67890'],
                'Airtime': ['MTN Airtime Purchase', 'Airtel Airtime Purchase', 'Tigo Airtime Purchase', 'MTN Data Bundle', 'Airtel Data Bundle'],
                'Deposit': ['Cash Deposit - Agent 12345', 'Cash Deposit - Agent 67890', 'Bank Transfer Deposit', 'Cash In - Supermarket', 'Cash In - Gas Station'],
                'Payment': ['Merchant Payment - Simba Supermarket', 'Merchant Payment - Nakumatt', 'Online Payment - Jumia', 'Restaurant Payment - Khana Khazana', 'Fuel Payment - SP'],
                'Bill': ['RECO Electricity Bill', 'WASAC Water Bill', 'RRA Tax Payment', 'Insurance Premium Payment', 'Internet Bill - Liquid Telecom'],
                'Incoming': ['Money Transfer from +250788123456', 'Money Transfer from +250722987654', 'Salary Payment', 'Refund Payment', 'Gift from Family'],
                'Cash Power': ['EUCL Prepaid Electricity', 'EUCL Emergency Units', 'EUCL Monthly Subscription', 'Prepaid Water Units', 'Prepaid Gas Units'],
                'OTP': ['Account Verification', 'Password Reset', 'Transaction Confirmation', 'Login Verification', 'Security Check']
            };
            
            for (let i = 1; i <= 1600; i++) {
                const type = transactionTypes[Math.floor(Math.random() * transactionTypes.length)];
                const status = statuses[Math.floor(Math.random() * statuses.length)];
                const description = descriptions[type][Math.floor(Math.random() * descriptions[type].length)];
                
                // Generate realistic amounts based on transaction type
                let amount;
                switch (type) {
                    case 'Airtime':
                    case 'OTP':
                        amount = Math.floor(Math.random() * 10000) + 1000; // 1K-10K
                        break;
                    case 'Bill':
                    case 'Cash Power':
                        amount = Math.floor(Math.random() * 50000) + 5000; // 5K-50K
                        break;
                    case 'Payment':
                        amount = Math.floor(Math.random() * 100000) + 2000; // 2K-100K
                        break;
                    case 'Withdrawal':
                    case 'Deposit':
                    case 'Incoming':
                        amount = Math.floor(Math.random() * 500000) + 10000; // 10K-500K
                        break;
                    default:
                        amount = Math.floor(Math.random() * 100000) + 1000;
                }
                
                // Generate dates for the last 30 days
                const date = new Date();
                date.setDate(date.getDate() - Math.floor(Math.random() * 30));
                const formattedDate = date.toISOString().split('T')[0];
                
                sampleTransactions.push({
                    id: `TXN${String(i).padStart(4, '0')}`,
                    type: type,
                    amount: amount,
                    date: formattedDate,
                    status: status,
                    description: description
                });
            }
            
            // Sort by date (newest first) and ID
            sampleTransactions.sort((a, b) => {
                if (a.date === b.date) {
                    return b.id.localeCompare(a.id);
                }
                return new Date(b.date) - new Date(a.date);
            });


            // Display only first 50 transactions initially for performance
            const displayTransactions = sampleTransactions.slice(0, 50);
            
            displayTransactions.forEach(transaction => {
                const transactionElement = document.createElement('div');
                transactionElement.className = 'transaction-item';
                transactionElement.setAttribute('role', 'listitem');
                
                // Add status styling
                const statusClass = transaction.status.toLowerCase();
                const statusColors = {
                    'completed': '#198536',
                    'pending': '#ffc107',
                    'failed': '#dc3545'
                };
                
                transactionElement.innerHTML = `
                    <div class="transaction-info">
                        <div class="transaction-amount" style="color: ${transaction.type === 'Incoming' || transaction.type === 'Deposit' ? '#198536' : '#dc3545'}">
                            ${transaction.type === 'Incoming' || transaction.type === 'Deposit' ? '+' : '-'}RWF ${transaction.amount.toLocaleString()}
                        </div>
                        <div class="transaction-details">${transaction.description}</div>
                        <div class="transaction-meta" style="font-size: 0.8rem; color: #999; margin-top: 0.25rem;">
                            ${transaction.id} • ${transaction.date}
                        </div>
                    </div>
                    <div class="transaction-status" style="color: ${statusColors[statusClass]}; font-weight: 600; font-size: 0.9rem;">
                        ${transaction.status}
                    </div>
                `;
                
                transactionElement.addEventListener('click', () => showTransactionDetails(transaction));
                transactionsContainer.appendChild(transactionElement);
            });
            
            // Add "Load More" button if there are more transactions
            if (sampleTransactions.length > 50) {
                const loadMoreBtn = document.createElement('div');
                loadMoreBtn.className = 'load-more-btn';
                loadMoreBtn.style.cssText = `
                    text-align: center; 
                    padding: 1rem; 
                    cursor: pointer; 
                    color: #198536; 
                    font-weight: 600;
                    border-top: 1px solid #eee;
                    transition: background-color 0.3s;
                `;
                loadMoreBtn.innerHTML = `Load More Transactions (${sampleTransactions.length - 50} remaining)`;
                loadMoreBtn.addEventListener('click', () => loadMoreTransactions(sampleTransactions, transactionsContainer, loadMoreBtn, 50));
                loadMoreBtn.addEventListener('mouseenter', () => loadMoreBtn.style.backgroundColor = '#f8f9fa');
                loadMoreBtn.addEventListener('mouseleave', () => loadMoreBtn.style.backgroundColor = '');
                transactionsContainer.appendChild(loadMoreBtn);
            }
            
            // Initialize search functionality
            const searchInput = document.getElementById('search');
            const typeFilter = document.getElementById('type');
            
            function filterTransactions() {
                const searchTerm = searchInput.value.toLowerCase();
                const selectedType = typeFilter.value;
                
                let filteredTransactions = window.allTransactions.filter(transaction => {
                    const matchesSearch = !searchTerm || 
                        transaction.id.toLowerCase().includes(searchTerm) ||
                        transaction.description.toLowerCase().includes(searchTerm) ||
                        transaction.amount.toString().includes(searchTerm);
                    
                    const matchesType = !selectedType || 
                        (selectedType === '1' && transaction.type === 'Incoming') ||
                        (selectedType === '2' && transaction.type === 'Payment') ||
                        (selectedType === '3' && transaction.type === 'Bill') ||
                        (selectedType === '4' && transaction.type === 'Deposit') ||
                        (selectedType === '5' && transaction.type === 'Airtime') ||
                        (selectedType === '6' && transaction.type === 'Cash Power') ||
                        (selectedType === '7' && transaction.type === 'Withdrawal') ||
                        (selectedType === '8' && transaction.type === 'OTP');
                    
                    return matchesSearch && matchesType;
                });
                
                // Clear current transactions
                const existingTransactions = transactionsContainer.querySelectorAll('.transaction-item, .load-more-btn');
                existingTransactions.forEach(item => item.remove());
                
                if (filteredTransactions.length === 0) {
                    const noResults = document.createElement('div');
                    noResults.className = 'no-results';
                    noResults.style.cssText = 'text-align: center; padding: 2rem; color: #666;';
                    noResults.innerHTML = 'No transactions found matching your criteria.';
                    transactionsContainer.appendChild(noResults);
                    return;
                }
                
                // Display filtered transactions (first 50)
                const displayTransactions = filteredTransactions.slice(0, 50);
                const statusColors = {
                    'completed': '#198536',
                    'pending': '#ffc107',
                    'failed': '#dc3545'
                };
                
                displayTransactions.forEach(transaction => {
                    const transactionElement = document.createElement('div');
                    transactionElement.className = 'transaction-item';
                    transactionElement.setAttribute('role', 'listitem');
                    
                    const statusClass = transaction.status.toLowerCase();
                    
                    transactionElement.innerHTML = `
                        <div class="transaction-info">
                            <div class="transaction-amount" style="color: ${transaction.type === 'Incoming' || transaction.type === 'Deposit' ? '#198536' : '#dc3545'}">
                                ${transaction.type === 'Incoming' || transaction.type === 'Deposit' ? '+' : '-'}RWF ${transaction.amount.toLocaleString()}
                            </div>
                            <div class="transaction-details">${transaction.description}</div>
                            <div class="transaction-meta" style="font-size: 0.8rem; color: #999; margin-top: 0.25rem;">
                                ${transaction.id} • ${transaction.date}
                            </div>
                        </div>
                        <div class="transaction-status" style="color: ${statusColors[statusClass]}; font-weight: 600; font-size: 0.9rem;">
                            ${transaction.status}
                        </div>
                    `;
                    
                    transactionElement.addEventListener('click', () => showTransactionDetails(transaction));
                    transactionsContainer.appendChild(transactionElement);
                });
                
                // Add "Load More" for filtered results if needed
                if (filteredTransactions.length > 50) {
                    const loadMoreBtn = document.createElement('div');
                    loadMoreBtn.className = 'load-more-btn';
                    loadMoreBtn.style.cssText = `
                        text-align: center; 
                        padding: 1rem; 
                        cursor: pointer; 
                        color: #198536; 
                        font-weight: 600;
                        border-top: 1px solid #eee;
                        transition: background-color 0.3s;
                    `;
                    loadMoreBtn.innerHTML = `Load More Results (${filteredTransactions.length - 50} remaining)`;
                    loadMoreBtn.addEventListener('click', () => loadMoreTransactions(filteredTransactions, transactionsContainer, loadMoreBtn, 50));
                    loadMoreBtn.addEventListener('mouseenter', () => loadMoreBtn.style.backgroundColor = '#f8f9fa');
                    loadMoreBtn.addEventListener('mouseleave', () => loadMoreBtn.style.backgroundColor = '');
                    transactionsContainer.appendChild(loadMoreBtn);
                }
            }
            
            // Add event listeners for real-time filtering
            searchInput.addEventListener('input', filterTransactions);
            typeFilter.addEventListener('change', filterTransactions);
        }
        
        function loadMoreTransactions(allTransactions, container, loadMoreBtn, currentCount) {
            const nextBatch = allTransactions.slice(currentCount, currentCount + 50);
            const statusColors = {
                'completed': '#198536',
                'pending': '#ffc107',
                'failed': '#dc3545'
            };
            
            nextBatch.forEach(transaction => {
                const transactionElement = document.createElement('div');
                transactionElement.className = 'transaction-item';
                transactionElement.setAttribute('role', 'listitem');
                
                const statusClass = transaction.status.toLowerCase();
                
                transactionElement.innerHTML = `
                    <div class="transaction-info">
                        <div class="transaction-amount" style="color: ${transaction.type === 'Incoming' || transaction.type === 'Deposit' ? '#198536' : '#dc3545'}">
                            ${transaction.type === 'Incoming' || transaction.type === 'Deposit' ? '+' : '-'}RWF ${transaction.amount.toLocaleString()}
                        </div>
                        <div class="transaction-details">${transaction.description}</div>
                        <div class="transaction-meta" style="font-size: 0.8rem; color: #999; margin-top: 0.25rem;">
                            ${transaction.id} • ${transaction.date}
                        </div>
                    </div>
                    <div class="transaction-status" style="color: ${statusColors[statusClass]}; font-weight: 600; font-size: 0.9rem;">
                        ${transaction.status}
                    </div>
                `;
                
                transactionElement.addEventListener('click', () => showTransactionDetails(transaction));
                container.insertBefore(transactionElement, loadMoreBtn);
            });
            
            const newCurrentCount = currentCount + 50;
            const remaining = allTransactions.length - newCurrentCount;
            
            if (remaining > 0) {
                loadMoreBtn.innerHTML = `Load More Transactions (${remaining} remaining)`;
                loadMoreBtn.onclick = () => loadMoreTransactions(allTransactions, container, loadMoreBtn, newCurrentCount);
            } else {
                loadMoreBtn.innerHTML = `All ${allTransactions.length} transactions loaded`;
                loadMoreBtn.style.color = '#666';
                loadMoreBtn.style.cursor = 'default';
                loadMoreBtn.onclick = null;
            }
        }

        function showTransactionDetails(transaction) {
            const modal = document.getElementById('transactionModal');
            const details = document.getElementById('transactionDetails');
            
            const statusColors = {
                'completed': '#198536',
                'pending': '#ffc107',
                'failed': '#dc3545'
            };
            
            details.innerHTML = `
                <div style="display: grid; gap: 1.5rem;">
                    <div style="border-bottom: 1px solid #eee; padding-bottom: 1rem;">
                        <div style="font-size: 1.5rem; font-weight: bold; color: ${transaction.type === 'Incoming' || transaction.type === 'Deposit' ? '#198536' : '#dc3545'}; margin-bottom: 0.5rem;">
                            ${transaction.type === 'Incoming' || transaction.type === 'Deposit' ? '+' : '-'}RWF ${transaction.amount.toLocaleString()}
                        </div>
                        <div style="color: #666;">${transaction.description}</div>
                    </div>
                    <div style="display: grid; gap: 1rem;">
                        <div><strong>Transaction ID:</strong> ${transaction.id}</div>
                        <div><strong>Type:</strong> ${transaction.type}</div>
                        <div><strong>Date & Time:</strong> ${transaction.date} 14:30:22</div>
                        <div><strong>Status:</strong> <span style="color: ${statusColors[transaction.status.toLowerCase()]}; font-weight: 600;">${transaction.status}</span></div>
                        ${transaction.status === 'Failed' ? '<div style="color: #dc3545; font-size: 0.9rem; padding: 0.5rem; background: #fff5f5; border-radius: 4px;"><strong>Failure Reason:</strong> Insufficient account balance</div>' : ''}
                    </div>
                </div>
            `;
            
            modal.style.display = 'block';
            modal.setAttribute('aria-hidden', 'false');
        }
    </script>
</body>
</html>