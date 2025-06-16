const API_BASE_URL = 'http://127.0.0.1:5000/api';
let charts = {};

// Initialize date range picker
$(document).ready(function() {
    $('#date-range').daterangepicker({
        opens: window.innerWidth <= 768 ? 'center' : 'left', // Center date picker on mobile
        locale: {
            format: 'YYYY-MM-DD'
        },
        autoApply: true, // Auto-apply dates for better mobile UX
        maxSpan: {
            days: 30 // Limit date range to improve performance
        }
    });
});

// Initialize charts with responsive options
function initializeCharts() {
    const isMobile = window.innerWidth <= 768;

    // Volume by Type Chart
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
                            size: isMobile ? 12 : 14 // Smaller font on mobile
                        }
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        maxRotation: isMobile ? 45 : 0, // Rotate labels on mobile
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

    // Monthly Summary Chart
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

    // Distribution Chart
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
                    position: isMobile ? 'bottom' : 'top', // Move legend to bottom on mobile
                    labels: {
                        font: {
                            size: isMobile ? 12 : 14
                        }
                    }
                }
            }
        }
    });

    // Top Types Chart
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

// Debounce function to limit API calls
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
    
    let url = `${API_BASE_URL}/transactions`;
    const params = new URLSearchParams();
    
    if (searchInput) params.append('search', searchInput);
    if (typeSelect) params.append('type', typeSelect);
    if (dateRange) {
        params.append('date_from', dateRange.startDate.format('YYYY-MM-DD'));
        params.append('date_to', dateRange.endDate.format('YYYY-MM-DD'));
    }
    
    if (params.toString()) url += `?${params.toString()}`;

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        
        const data = await response.json();
        displayTransactions(data);
        updateCharts(data);
    } catch (error) {
        console.error('Error fetching transactions:', error);
        showError('Failed to load transactions. Please try again later.');
    }
}, 300); // 300ms debounce

// Display transactions in the list
function displayTransactions(transactions) {
    const container = document.getElementById('transactions');
    container.innerHTML = '';

    if (!transactions || transactions.length === 0) {
        container.innerHTML = '<div class="loading">No transactions found</div>';
        return;
    }

    transactions.forEach(txn => {
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

// Update all charts with new data
function updateCharts(transactions) {
    // Update Volume Chart
    const volumeData = processVolumeData(transactions);
    charts.volume.data.labels = volumeData.labels;
    charts.volume.data.datasets[0].data = volumeData.values;
    charts.volume.update();

    // Update Monthly Chart
    const monthlyData = processMonthlyData(transactions);
    charts.monthly.data.labels = monthlyData.labels;
    charts.monthly.data.datasets[0].data = monthlyData.values;
    charts.monthly.update();

    // Update Distribution Chart
    const distributionData = processDistributionData(transactions);
    charts.distribution.data.datasets[0].data = distributionData;
    charts.distribution.update();

    // Update Top Types Chart
    const topTypesData = processTopTypesData(transactions);
    charts.topTypes.data.labels = topTypesData.labels;
    charts.topTypes.data.datasets[0].data = topTypesData.values;
    charts.topTypes.update();
}

// Process data for volume chart
function processVolumeData(transactions) {
    const typeCounts = {};
    transactions.forEach(txn => {
        typeCounts[txn.transaction_type] = (typeCounts[txn.transaction_type] || 0) + 1;
    });
    
    return {
        labels: Object.keys(typeCounts).map(type => getTransactionTypeName(type)),
        values: Object.values(typeCounts)
    };
}

// Process data for monthly chart
function processMonthlyData(transactions) {
    const monthlyData = {};
    transactions.forEach(txn => {
        const month = new Date(txn.timestamp).toLocaleString('default', { month: 'short', year: 'numeric' });
        monthlyData[month] = (monthlyData[month] || 0) + 1;
    });
    
    return {
        labels: Object.keys(monthlyData),
        values: Object.values(monthlyData)
    };
}

// Process data for distribution chart
function processDistributionData(transactions) {
    let deposits = 0;
    let withdrawals = 0;
    
    transactions.forEach(txn => {
        if (['1', '4'].includes(txn.transaction_type)) {
            deposits += txn.amount;
        } else {
            withdrawals += Math.abs(txn.amount);
        }
    });
    
    return [deposits, withdrawals];
}

// Process data for top types chart
function processTopTypesData(transactions) {
    const typeCounts = {};
    transactions.forEach(txn => {
        typeCounts[txn.transaction_type] = (typeCounts[txn.transaction_type] || 0) + 1;
    });
    
    const sortedTypes = Object.entries(typeCounts)
        .sort(([,a], [,b]) => b - a)
        .slice(0, window.innerWidth <= 768 ? 3 : 5); // Show fewer types on mobile
    
    return {
        labels: sortedTypes.map(([type]) => getTransactionTypeName(type)),
        values: sortedTypes.map(([,count]) => count)
    };
}

// Helper function to get transaction type name
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
        ? date.toLocaleDateString() // Simpler date format on mobile
        : date.toLocaleString();
}

// Format amount
function formatAmount(amount) {
    return new Intl.NumberFormat('en-RW', {
        style: 'currency',
        currency: 'RWF',
        minimumFractionDigits: window.innerWidth <= 768 ? 0 : 2 // Less precision on mobile
    }).format(amount);
}

// Show transaction details in modal
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
    const container = document.getElementById('transactions');
    container.innerHTML = `<div class="error">${message}</div>`;
}

// Handle window resize
function handleResize() {
    initializeCharts(); // Reinitialize charts on resize
    fetchTransactions(); // Refresh data to adjust for new screen size
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
