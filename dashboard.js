const API_BASE_URL = 'http://127.0.0.1:5000/api';
let charts = {};

// Initialize date range picker
$(document).ready(function() {
    $('#date-range').daterangepicker({
        opens: window.innerWidth <= 768 ? 'center' : 'left',
        locale: { format: 'YYYY-MM-DD' },
        autoApply: true,
        maxSpan: { days: 30 }
    });
});

// Initialize charts with responsive options
function initializeCharts() {
    const isMobile = window.innerWidth <= 768;
    // Volume by Type Chart
    charts.volume = new Chart(document.getElementById('volumeChart'), {
        type: 'bar',
        data: { labels: [], datasets: [{ label: 'Transaction Volume', data: [], backgroundColor: '#198536' }] },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { labels: { font: { size: isMobile ? 12 : 14 } } } },
            scales: {
                x: { ticks: { maxRotation: isMobile ? 45 : 0, font: { size: isMobile ? 10 : 12 } } },
                y: { ticks: { font: { size: isMobile ? 10 : 12 } } }
            }
        }
    });
    // Monthly Summary Chart
    charts.monthly = new Chart(document.getElementById('monthlyChart'), {
        type: 'line',
        data: { labels: [], datasets: [{ label: 'Monthly Transactions', data: [], borderColor: '#198536', tension: 0.1 }] },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { labels: { font: { size: isMobile ? 12 : 14 } } } },
            scales: {
                x: { ticks: { font: { size: isMobile ? 10 : 12 } } },
                y: { ticks: { font: { size: isMobile ? 10 : 12 } } }
            }
        }
    });
    // Distribution Chart
    charts.distribution = new Chart(document.getElementById('distributionChart'), {
        type: 'pie',
        data: { labels: ['Deposits', 'Withdrawals'], datasets: [{ data: [0, 0], backgroundColor: ['#198536', '#dc3545'] }] },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: isMobile ? 'bottom' : 'top', labels: { font: { size: isMobile ? 12 : 14 } } } }
        }
    });
    // Top Types Chart
    charts.topTypes = new Chart(document.getElementById('topTypesChart'), {
        type: 'doughnut',
        data: { labels: [], datasets: [{ data: [], backgroundColor: ['#198536', '#ffcc00', '#1e3a5f', '#dc3545', '#2196f3'] }] },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: isMobile ? 'bottom' : 'top', labels: { font: { size: isMobile ? 12 : 14 } } } }
        }
    });
}

// Debounce function to limit API calls
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => { clearTimeout(timeout); func(...args); };
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
}, 300);

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
                <div class="transaction-amount">${formatAmount(txn.amount)}</div>
                <div class="transaction-details">${txn.tx_type} - ${formatDate(txn.tx_timestamp)}</div>
                <div class="transaction-message">${txn.raw_body || ''}</div>
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
        typeCounts[txn.tx_type] = (typeCounts[txn.tx_type] || 0) + 1;
    });
    return {
        labels: Object.keys(typeCounts),
        values: Object.values(typeCounts)
    };
}

// Process data for monthly chart
function processMonthlyData(transactions) {
    const monthlyData = {};
    transactions.forEach(txn => {
        const month = new Date(txn.tx_timestamp).toLocaleString('default', { month: 'short', year: 'numeric' });
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
        if (txn.tx_type === 'deposit') {
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
        typeCounts[txn.tx_type] = (typeCounts[txn.tx_type] || 0) + 1;
    });
    const sortedTypes = Object.entries(typeCounts)
        .sort(([,a], [,b]) => b - a)
        .slice(0, window.innerWidth <= 768 ? 3 : 5);
    return {
        labels: sortedTypes.map(([type]) => type),
        values: sortedTypes.map(([,count]) => count)
    };
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

// Show transaction details in modal
function showTransactionDetails(transaction) {
    const modal = document.getElementById('transactionModal');
    const details = document.getElementById('transactionDetails');
    details.innerHTML = `
        <h3>Transaction Details</h3>
        <p><strong>Amount:</strong> ${formatAmount(transaction.amount)}</p>
        <p><strong>Type:</strong> ${transaction.tx_type}</p>
        <p><strong>Date:</strong> ${formatDate(transaction.tx_timestamp)}</p>
        <p><strong>Message:</strong> ${transaction.raw_body || 'N/A'}</p>
        <p><strong>From:</strong> ${transaction.from_party || 'N/A'}</p>
        <p><strong>To:</strong> ${transaction.to_party || 'N/A'}</p>
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
    initializeCharts();
    fetchTransactions();
}

// Event listeners
$(document).ready(function() {
    initializeCharts();
    fetchTransactions();
    $('#search').on('input', fetchTransactions);
    $('#type').on('change', fetchTransactions);
$('#date-range').on('apply.daterangepicker', fetchTransactions);
    $('.close-modal').on('click', function() {
        $('#transactionModal').hide();
    });
    $(window).on('click', function(event) {
        if (event.target === document.getElementById('transactionModal')) {
            $('#transactionModal').hide();
        }
    });
    $(window).on('resize', debounce(handleResize, 200));
}); 