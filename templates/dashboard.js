let charts = {};

// Initialize date range picker
$(document).ready(function() {
    $('#date-range').daterangepicker({
        opens: window.innerWidth <= 768 ? 'center' : 'left',
        locale: {
            format: 'YYYY-MM-DD'
        },
        autoApply: true,
        maxSpan: {
            days: 30
        }
    });
});

// Initialize charts with responsive options
function initializeCharts() {
    const isMobile = window.innerWidth <= 768;

    charts.volume = new Chart(document.getElementById('volumeChart'), {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Transaction Volume',
                data: [],
                backgroundColor: '#198536'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        font: {
                            size: isMobile ? 12 : 14
                        }
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        maxRotation: isMobile ? 45 : 0,
                        font: {
                            size: isMobile ? 10 : 12
                        }
                    }
                },
                y: {
                    ticks: {
                        font: {
                            size: isMobile ? 10 : 12
                        }
                    }
                }
            }
        }
    });

    charts.monthly = new Chart(document.getElementById('monthlyChart'), {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Monthly Transactions',
                data: [],
                borderColor: '#198536',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        font: {
                            size: isMobile ? 12 : 14
                        }
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        font: {
                            size: isMobile ? 10 : 12
                        }
                    }
                },
                y: {
                    ticks: {
                        font: {
                            size: isMobile ? 10 : 12
                        }
                    }
                }
            }
        }
    });

    charts.distribution = new Chart(document.getElementById('distributionChart'), {
        type: 'pie',
        data: {
            labels: ['Deposits', 'Withdrawals'],
            datasets: [{
                data: [0, 0],
                backgroundColor: ['#198536', '#dc3545']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: isMobile ? 'bottom' : 'top',
                    labels: {
                        font: {
                            size: isMobile ? 12 : 14
                        }
                    }
                }
            }
        }
    });

    charts.topTypes = new Chart(document.getElementById('topTypesChart'), {
        type: 'doughnut',
        data: {
            labels: [],
            datasets: [{
                data: [],
                backgroundColor: ['#198536', '#ffcc00', '#1e3a5f', '#dc3545', '#2196f3']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: isMobile ? 'bottom' : 'top',
                    labels: {
                        font: {
                            size: isMobile ? 12 : 14
                        }
                    }
                }
            }
        }
    });
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Fetch and display transactions
const fetchTransactions = debounce(async function() {
    const searchInput = document.getElementById('search').value;
    const typeSelect = document.getElementById('type').value;
    const dateRange = $('#date-range').data('daterangepicker');
    
    try {
        document.getElementById('loading').style.display = 'block';
        document.getElementById('error-message').style.display = 'none';
        document.getElementById('transactions').innerHTML = '<div class="loading" id="loading">Loading transactions...</div>';

        const response = await fetch('transactions.json', {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}, ${response.statusText}`);
        }
        
        const data = await response.json();
        if (!Array.isArray(data)) {
            throw new Error('Invalid data format: Expected an array of transactions');
        }

        let filteredData = data;
        if (searchInput) {
            filteredData = filteredData.filter(t =>
                (t.message || '').toLowerCase().includes(searchInput.toLowerCase()) ||
                (t.sender || '').toLowerCase().includes(searchInput.toLowerCase()) ||
                (t.recipient || '').toLowerCase().includes(searchInput.toLowerCase())
            );
        }
        if (typeSelect) {
            filteredData = filteredData.filter(t => t.transaction_type === typeSelect);
        }
        if (dateRange) {
            const startDate = dateRange.startDate.format('YYYY-MM-DD');
            const endDate = dateRange.endDate.format('YYYY-MM-DD');
            filteredData = filteredData.filter(t => t.timestamp.slice(0, 10) >= startDate && t.timestamp.slice(0, 10) <= endDate);
        }

        document.getElementById('loading').style.display = 'none';
        displayTransactions(filteredData);
        updateCharts(filteredData);
    } catch (error) {
        console.error('Error fetching transactions:', error);
        document.getElementById('loading').style.display = 'none';
        document.getElementById('error-message').innerText = `Failed to load transactions: ${error.message}. Please ensure transactions.json exists.`;
        document.getElementById('error-message').style.display = 'block';
        document.getElementById('transactions').innerHTML = '';
    }
}, 300);

// Display transactions
function displayTransactions(transactions) {
    const container = document.getElementById('transactions');
    container.innerHTML = '';

    if (!transactions || transactions.length === 0) {
        container.innerHTML = '<div class="error">No transactions found for the selected criteria.</div>';
        return;
    }

    transactions.forEach(txn => {
        if (!txn || !txn.transaction_type || !txn.amount || !txn.timestamp) {
            console.warn('Invalid transaction data:', txn);
            return;
        }
        const transactionItem = document.createElement('div');
        transactionItem.className = 'transaction-item';
        transactionItem.innerHTML = `
            <div class="transaction-info">
                <h4>${txn.message || 'Transaction'}</h4>
                <p>${formatDate(txn.timestamp)}</p>
                <p>Amount: ${formatAmount(txn.amount)}</p>
            </div>
        `;
        
        transactionItem.addEventListener('click', () => showTransactionDetails(txn));
        container.appendChild(transactionItem);
    });
}

// Update charts
function updateCharts(transactions) {
    const volumeData = processVolumeData(transactions);
    charts.volume.data.labels = volumeData.labels;
    charts.volume.data.datasets[0].data = volumeData.values;
    charts.volume.update();

    const monthlyData = processMonthlyData(transactions);
    charts.monthly.data.labels = monthlyData.labels;
    charts.monthly.data.datasets[0].data = monthlyData.values;
    charts.monthly.update();

    const distributionData = processDistributionData(transactions);
    charts.distribution.data.datasets[0].data = distributionData;
    charts.distribution.update();

    const topTypesData = processTopTypesData(transactions);
    charts.topTypes.data.labels = topTypesData.labels;
    charts.topTypes.data.datasets[0].data = topTypesData.values;
    charts.topTypes.update();
}

// Process volume chart data
function processVolumeData(transactions) {
    const typeCounts = {};
    transactions.forEach(txn => {
        if (txn.transaction_type) {
            typeCounts[txn.transaction_type] = (typeCounts[txn.transaction_type] || 0) + 1;
        }
    });
    
    return {
        labels: Object.keys(typeCounts).map(type => getTransactionTypeName(type)),
        values: Object.values(typeCounts)
    };
}

// Process monthly chart data
function processMonthlyData(transactions) {
    const monthlyData = {};
    transactions.forEach(txn => {
        if (txn.timestamp) {
            const month = new Date(txn.timestamp).toLocaleString('default', { month: 'short', year: 'numeric' });
            monthlyData[month] = (monthlyData[month] || 0) + 1;
        }
    });
    
    return {
        labels: Object.keys(monthlyData),
        values: Object.values(monthlyData)
    };
}

// Process distribution chart data
function processDistributionData(transactions) {
    let deposits = 0;
    let withdrawals = 0;
    
    transactions.forEach(txn => {
        if (txn.transaction_type && txn.amount) {
            if (['1', '4'].includes(txn.transaction_type)) {
                deposits += txn.amount;
            } else {
                withdrawals += Math.abs(txn.amount);
            }
        }
    });
    
    return [deposits, withdrawals];
}

// Process top types chart data
function processTopTypesData(transactions) {
    const typeCounts = {};
    transactions.forEach(txn => {
        if (txn.transaction_type) {
            typeCounts[txn.transaction_type] = (typeCounts[txn.transaction_type] || 0) + 1;
        }
    });
    
    const sortedTypes = Object.entries(typeCounts)
        .sort(([,a], [,b]) => b - a)
        .slice(0, window.innerWidth <= 768 ? 3 : 5);
    
    return {
        labels: sortedTypes.map(([type]) => getTransactionTypeName(type)),
        values: sortedTypes.map(([,count]) => count)
    };
}

// Get transaction type name
function getTransactionTypeName(type) {
    const types = {
        '1': 'Incoming',
        '2': 'Payment',
        '3': 'Bill',
        '4': 'Deposit',
        '5': 'Airtime',
        '6': 'Cash Power',
        '7': 'Withdrawal',
        '8': 'OTP'
    };
    return types[type] || 'Unknown';
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return window.innerWidth <= 768
        ? date.toLocaleDateString()
        : date.toLocaleString();
}

// Format amount
function formatAmount(amount) {
    return new Intl.NumberFormat('en-RW', {
        style: 'currency',
        currency: 'RWF',
        minimumFractionDigits: window.innerWidth <= 768 ? 0 : 2
    }).format(amount);
}

// Show transaction details
function showTransactionDetails(transaction) {
    const modal = document.getElementById('transactionModal');
    const details = document.getElementById('transactionDetails');
    
    details.innerHTML = `
        <p><strong>Date:</strong> ${formatDate(transaction.timestamp)}</p>
        <p><strong>Amount:</strong> ${formatAmount(transaction.amount)}</p>
        <p><strong>Type:</strong> ${getTransactionTypeName(transaction.transaction_type)}</p>
        <p><strong>Description:</strong> ${transaction.message || 'N/A'}</p>
        <p><strong>Sender:</strong> ${transaction.sender || 'N/A'}</p>
        <p><strong>Recipient:</strong> ${transaction.recipient || 'N/A'}</p>
    `;
    
    modal.style.display = 'block';
}

// Show error message
function showError(message) {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('error-message').innerText = message;
    document.getElementById('error-message').style.display = 'block';
    document.getElementById('transactions').innerHTML = '';
}

// Handle window resize
function handleResize() {
    initializeCharts();
    fetchTransactions();
}

// Event listeners
document.getElementById('search').addEventListener('input', fetchTransactions);
document.getElementById('type').addEventListener('change', fetchTransactions);
$('#date-range').on('apply.daterangepicker', fetchTransactions);
document.querySelector('.close-modal').addEventListener('click', () => {
    document.getElementById('transactionModal').style.display = 'none';
});
window.addEventListener('click', (event) => {
    const modal = document.getElementById('transactionModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});
window.addEventListener('resize', debounce(handleResize, 200));

// Initialize the dashboard
initializeCharts();
fetchTransactions();
