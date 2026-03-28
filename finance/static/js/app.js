let currentRankings = [];

async function loadCustomers() {
    try {
        const response = await axios.get('/customers');
        const select = document.getElementById('customerSelect');

        response.data.forEach(customer => {
            const option = document.createElement('option');
            option.value = customer.id;
            const riskLevel = customer.risk_tolerance < 0.4 ? 'Conservative' :
                customer.risk_tolerance > 0.7 ? 'Aggressive' : 'Balanced';
            option.textContent = `${customer.name} (${riskLevel} Investor)`;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading customers:', error);
    }
}

async function loadPersonalizedRankings(customerId) {
    const loadingIndicator = document.getElementById('loadingIndicator');
    const stockGrid = document.getElementById('stockGrid');
    const emptyState = document.getElementById('emptyState');

    loadingIndicator.classList.remove('hidden');
    stockGrid.innerHTML = '';
    emptyState.classList.add('hidden');

    try {
        // Get the state of the Dodo toggle
        const useDodo = document.getElementById('useDodoToggle').checked;

        const response = await axios.get(`/rankings/${customerId}`, {
            params: { use_dodo: useDodo }
        });
        currentRankings = response.data;

        loadingIndicator.classList.add('hidden');
        displayStocks(currentRankings);
    } catch (error) {
        loadingIndicator.classList.add('hidden');
        console.error('Error loading rankings:', error);
        stockGrid.innerHTML = '<div class="col-span-full text-center text-red-600 p-8">Error loading rankings. Please try again.</div>';
    }
}

function displayStocks(stocks) {
    const stockGrid = document.getElementById('stockGrid');

    stocks.forEach(stock => {
        const changeClass = stock.change_percent >= 0 ? 'positive' : 'negative';
        const changeSymbol = stock.change_percent >= 0 ? '+' : '';
        const trendIcon = stock.change_percent >= 0 ? '↗' : '↘';

        const card = document.createElement('div');
        card.className = 'stock-card bg-white rounded-lg p-6 cursor-pointer hover:bg-gray-50';
        card.innerHTML = `
            <div class="flex justify-between items-start mb-4">
                <div class="flex-1">
                    <div class="flex items-center gap-2 mb-2">
                        <h3 class="text-lg font-bold text-gray-900">${stock.symbol}</h3>
                        <span class="rank-badge text-white text-xs px-2 py-1 rounded-full font-medium">#${stock.rank_position}</span>
                    </div>
                    <p class="text-sm text-gray-600 font-medium">${stock.company_name}</p>
                    <p class="text-xs text-gray-500 mt-1 line-clamp-2">${stock.description || getSectorDescription(stock.sector)}</p>
                </div>
                <div class="text-right ml-4">
                    <div class="text-2xl font-bold text-gray-900">$${stock.current_price.toFixed(2)}</div>
                    <div class="${changeClass} text-sm font-semibold flex items-center justify-end gap-1">
                        <span>${trendIcon}</span>
                        <span>${changeSymbol}${stock.change_percent.toFixed(2)}%</span>
                    </div>
                </div>
            </div>
            
            <div class="mb-4">
                <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-semibold text-gray-700">Last Month Orders</span>
                    <span class="text-xs font-bold text-blue-600">${stock.last_month_orders.toLocaleString()}</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-blue-600 h-2 rounded-full progress-bar" style="width: ${(stock.last_month_orders / 10000) * 100}%"></div>
                </div>
            </div>
            
            <div class="flex items-center justify-between text-sm">
                <div class="flex items-center gap-4">
                    <span class="text-gray-500">Sector:</span>
                    <span class="text-gray-900 font-medium">${stock.sector}</span>
                </div>
                <div class="live-orders">
                    ${stock.market_cap}B Valuation
                </div>
            </div>
            
            <div class="mt-4 pt-4 border-t border-gray-200">
                <p class="text-xs text-gray-600 leading-relaxed" title="${stock.reasoning}">
                    <span class="font-semibold">Why this stock:</span> ${stock.reasoning.length > 80 ? stock.reasoning.substring(0, 80) + '...' : stock.reasoning}
                </p>
            </div>
        `;

        card.addEventListener('click', () => showStockDetails(stock.symbol));
        stockGrid.appendChild(card);
    });
}

function getSectorDescription(sector) {
    const descriptions = {
        'technology': 'Leading AI, gaming, and communication platforms shaping digital future',
        'finance': 'Fintech innovators building next-generation financial infrastructure',
        'consumer': 'Digital platforms transforming how people live, shop, and connect',
        'industrial': 'Aerospace and space technology pioneers revolutionizing travel',
        'healthcare': 'Biotechnology and medical device innovations',
        'energy': 'Renewable energy and sustainable power solutions',
        'real_estate': 'Commercial property and development projects',
        'utilities': 'Smart grid and essential infrastructure services'
    };
    return descriptions[sector] || 'Private company in emerging markets';
}

async function showStockDetails(symbol) {
    try {
        const response = await axios.get(`/stocks/${symbol}`);
        const stock = response.data;

        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black bg-opacity-50 modal-backdrop flex items-center justify-center z-50 p-4';
        modal.innerHTML = `
            <div class="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6">
                <div class="flex justify-between items-start mb-6">
                    <div>
                        <h2 class="text-2xl font-bold text-gray-900">${stock.symbol}</h2>
                        <p class="text-lg text-gray-600">${stock.company.name}</p>
                    </div>
                    <button onclick="this.closest('.fixed').remove()" class="text-gray-400 hover:text-gray-600 text-2xl font-bold">&times;</button>
                </div>
                
                <div class="grid grid-cols-2 gap-4 mb-6">
                    <div class="bg-gray-50 p-4 rounded-lg">
                        <p class="text-sm text-gray-500 mb-1">Current Price</p>
                        <p class="text-xl font-bold text-gray-900">$${stock.current_price.toFixed(2)}</p>
                    </div>
                    <div class="bg-gray-50 p-4 rounded-lg">
                        <p class="text-sm text-gray-500 mb-1">Market Cap</p>
                        <p class="text-xl font-bold text-gray-900">$${stock.company.market_cap}B</p>
                    </div>
                </div>
                
                <div class="mb-6">
                    <h3 class="text-lg font-semibold text-gray-900 mb-2">Company Overview</h3>
                    <p class="text-gray-600">${stock.company.description}</p>
                    <div class="mt-3 grid grid-cols-3 gap-4 text-sm">
                        <div><span class="font-medium">Sector:</span> ${stock.company.sector}</div>
                        <div><span class="font-medium">Founded:</span> ${stock.company.founded_year}</div>
                        <div><span class="font-medium">Employees:</span> ${stock.company.employee_count.toLocaleString()}</div>
                        <div><span class="font-medium">Revenue:</span> $${stock.company.revenue}B</div>
                        <div><span class="font-medium">Volume:</span> ${stock.latest_price.volume.toLocaleString()}</div>
                        <div><span class="font-medium">Daily Change:</span> <span class="${stock.latest_price.change_percent >= 0 ? 'positive' : 'negative'}">${stock.latest_price.change_percent >= 0 ? '+' : ''}${stock.latest_price.change_percent.toFixed(2)}%</span></div>
                    </div>
                </div>
                
                <div class="mb-6">
                    <h3 class="text-lg font-semibold text-gray-900 mb-2">Recent News</h3>
                    <div class="space-y-2">
                        ${stock.recent_news.map(news => `
                            <div class="border-l-4 border-blue-500 pl-3 py-1">
                                <p class="font-medium text-gray-900">${news.headline}</p>
                                <p class="text-sm text-gray-600">${news.summary}</p>
                                <p class="text-xs text-gray-500 mt-1">Sentiment: <span class="font-medium">${news.sentiment}</span> (Impact: ${(news.impact_score * 100).toFixed(0)}%)</p>
                            </div>
                        `).join('')}
                    </div>
                </div>
                
                <div>
                    <h3 class="text-lg font-semibold text-gray-900 mb-2">Products</h3>
                    <div class="space-y-2">
                        ${stock.products.map(product => `
                            <div class="flex justify-between items-center p-2 bg-gray-50 rounded">
                                <div>
                                    <p class="font-medium text-gray-900">${product.name}</p>
                                    <p class="text-sm text-gray-600">${product.description}</p>
                                </div>
                                <div class="text-right">
                                    <span class="text-sm font-medium text-blue-600">${(product.success_score * 100).toFixed(0)}% Success</span>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    } catch (error) {
        console.error('Error loading stock details:', error);
        alert('Error loading stock details');
    }
}

// Event listeners
document.getElementById('customerSelect').addEventListener('change', (e) => {
    const customerId = e.target.value;
    if (customerId) {
        // Show trading tabs
        document.getElementById('tradingTabs').classList.remove('hidden');

        // Load rankings by default
        loadPersonalizedRankings(customerId);
    } else {
        // Hide trading tabs
        document.getElementById('tradingTabs').classList.add('hidden');

        // Hide all tab contents
        document.getElementById('rankingsContent').classList.add('hidden');
        document.getElementById('portfolioContent').classList.add('hidden');
        document.getElementById('transactionsContent').classList.add('hidden');

        // Reset to rankings tab
        showTab('rankings');
    }
});

// Event listener for Dodo toggle
document.getElementById('useDodoToggle').addEventListener('change', (e) => {
    const customerId = document.getElementById('customerSelect').value;
    if (customerId) {
        // Reload rankings with new Dodo setting
        loadPersonalizedRankings(customerId);
    }
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadCustomers();
    setupTradingTabs();
});

function setupTradingTabs() {
    // Add tab switching functionality
    const rankingsTab = document.getElementById('rankingsTab');
    const portfolioTab = document.getElementById('portfolioTab');
    const transactionsTab = document.getElementById('transactionsTab');

    if (rankingsTab && portfolioTab && transactionsTab) {
        rankingsTab.addEventListener('click', () => showTab('rankings'));
        portfolioTab.addEventListener('click', () => showTab('portfolio'));
        transactionsTab.addEventListener('click', () => showTab('transactions'));
    }
}

function showTab(tabName) {
    // Hide all tab contents
    document.getElementById('rankingsContent').classList.add('hidden');
    document.getElementById('portfolioContent').classList.add('hidden');
    document.getElementById('transactionsContent').classList.add('hidden');

    // Remove active state from all tabs
    document.getElementById('rankingsTab').classList.remove('bg-blue-600', 'text-white');
    document.getElementById('portfolioTab').classList.remove('bg-blue-600', 'text-white');
    document.getElementById('transactionsTab').classList.remove('bg-blue-600', 'text-white');

    // Show selected tab and set active state
    document.getElementById(tabName + 'Content').classList.remove('hidden');
    document.getElementById(tabName + 'Tab').classList.add('bg-blue-600', 'text-white');

    // Load data for the selected tab
    const customerId = document.getElementById('customerSelect').value;
    if (customerId) {
        if (tabName === 'portfolio') {
            loadPortfolio(customerId);
        } else if (tabName === 'transactions') {
            loadTransactions(customerId);
        }
    }
}

async function loadPortfolio(customerId) {
    try {
        const response = await axios.get(`/portfolio/${customerId}`);
        const portfolio = response.data;

        // Sort portfolio holdings by market value in descending order
        portfolio.holdings.sort((a, b) => b.market_value - a.market_value);

        const portfolioContent = document.getElementById('portfolioContent');
        portfolioContent.innerHTML = `
            <div class="bg-white rounded-lg p-6 border border-gray-200">
                <h3 class="text-xl font-bold text-gray-900 mb-4">Portfolio Summary</h3>
                
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                    <div class="bg-gray-50 p-4 rounded-lg">
                        <p class="text-sm text-gray-500 mb-1">Available Cash</p>
                        <p class="text-2xl font-bold text-gray-900">$${portfolio.cash.toLocaleString()}</p>
                    </div>
                    <div class="bg-gray-50 p-4 rounded-lg">
                        <p class="text-sm text-gray-500 mb-1">Total Market Value</p>
                        <p class="text-2xl font-bold text-gray-900">$${portfolio.total_market_value.toLocaleString()}</p>
                    </div>
                    <div class="bg-gray-50 p-4 rounded-lg">
                        <p class="text-sm text-gray-500 mb-1">Total Cost Basis</p>
                        <p class="text-2xl font-bold text-gray-900">$${portfolio.total_cost.toLocaleString()}</p>
                    </div>
                    <div class="bg-gray-50 p-4 rounded-lg">
                        <p class="text-sm text-gray-500 mb-1">Total P&L</p>
                        <p class="text-2xl font-bold ${portfolio.total_unrealized_pnl >= 0 ? 'positive' : 'negative'}">
                            $${Math.abs(portfolio.total_unrealized_pnl).toLocaleString()}
                        </p>
                        <p class="text-sm ${portfolio.total_unrealized_pnl >= 0 ? 'positive' : 'negative'}">
                            ${portfolio.total_unrealized_pnl >= 0 ? '+' : ''}${portfolio.total_unrealized_pnl_percent.toFixed(2)}%
                        </p>
                    </div>
                </div>
                
                <h4 class="text-lg font-semibold text-gray-900 mb-3">Holdings</h4>
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Symbol</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quantity</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Avg Cost</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Current Price</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Market Value</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">P&L</th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            ${portfolio.holdings.map(holding => `
                                <tr>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${holding.symbol}</td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${holding.quantity}</td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">$${holding.avg_cost.toFixed(2)}</td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">$${holding.current_price.toFixed(2)}</td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">$${holding.market_value.toFixed(2)}</td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm">
                                        <span class="${holding.unrealized_pnl >= 0 ? 'positive' : 'negative'} font-medium">
                                            $${Math.abs(holding.unrealized_pnl).toFixed(2)} (${holding.unrealized_pnl_percent >= 0 ? '+' : ''}${holding.unrealized_pnl_percent.toFixed(2)}%)
                                        </span>
                                    </td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
                
                            </div>
        `;
    } catch (error) {
        console.error('Error loading portfolio:', error);
    }
}

async function loadTransactions(customerId) {
    try {
        const response = await axios.get(`/transactions/${customerId}`);
        const data = response.data;

        const transactionsContent = document.getElementById('transactionsContent');
        transactionsContent.innerHTML = `
            <div class="bg-white rounded-lg p-6 border border-gray-200">
                <h3 class="text-xl font-bold text-gray-900 mb-4">Transaction History</h3>
                
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Symbol</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quantity</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total Value</th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            ${data.transactions.map(transaction => `
                                <tr>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                        ${new Date(transaction.timestamp).toLocaleDateString()}
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${transaction.symbol}</td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm">
                                        <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${transaction.type === 'buy'
                ? 'bg-green-100 text-green-800'
                : 'bg-red-100 text-red-800'
            }">
                                            ${transaction.type.toUpperCase()}
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${transaction.quantity}</td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">$${transaction.price.toFixed(2)}</td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">$${transaction.total_value.toFixed(2)}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        `;
    } catch (error) {
        console.error('Error loading transactions:', error);
    }
}

function showTradeModal() {
    const customerId = document.getElementById('customerSelect').value;
    if (!customerId) {
        alert('Please select a customer profile first');
        return;
    }

    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-black bg-opacity-50 modal-backdrop flex items-center justify-center z-50 p-4';
    modal.innerHTML = `
        <div class="bg-white rounded-lg max-w-md w-full p-6">
            <div class="flex justify-between items-center mb-4">
                <h3 class="text-lg font-bold text-gray-900">Place New Trade</h3>
                <button onclick="this.closest('.fixed').remove()" class="text-gray-400 hover:text-gray-600 text-2xl font-bold">&times;</button>
            </div>
            
            <form onsubmit="executeTrade(event)">
                <input type="hidden" id="tradeCustomerId" value="${customerId}">
                
                <div class="mb-4">
                    <label for="tradeSymbol" class="block text-sm font-medium text-gray-700 mb-2">Stock Symbol</label>
                    <input type="text" id="tradeSymbol" required 
                           class="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                           placeholder="e.g., OPENAI, SPACEX">
                </div>
                
                <div class="mb-4">
                    <label for="tradeType" class="block text-sm font-medium text-gray-700 mb-2">Trade Type</label>
                    <select id="tradeType" required 
                            class="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <option value="buy">Buy</option>
                        <option value="sell">Sell</option>
                    </select>
                </div>
                
                <div class="mb-6">
                    <label for="tradeQuantity" class="block text-sm font-medium text-gray-700 mb-2">Quantity</label>
                    <input type="number" id="tradeQuantity" required min="1"
                           class="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                           placeholder="Number of shares">
                </div>
                
                <div class="flex gap-3">
                    <button type="submit" class="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition">
                        Execute Trade
                    </button>
                    <button type="button" onclick="this.closest('.fixed').remove()" 
                            class="flex-1 bg-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-400 transition">
                        Cancel
                    </button>
                </div>
            </form>
        </div>
    `;
    document.body.appendChild(modal);
}

async function executeTrade(event) {
    event.preventDefault();

    const customerId = document.getElementById('tradeCustomerId').value;
    const symbol = document.getElementById('tradeSymbol').value.toUpperCase();
    const transactionType = document.getElementById('tradeType').value;
    const quantity = parseInt(document.getElementById('tradeQuantity').value);

    try {
        const response = await axios.post('/trade', {
            customer_id: customerId,
            symbol: symbol,
            transaction_type: transactionType,
            quantity: quantity
        });

        if (response.data.success) {
            alert('Trade executed successfully!');
            document.querySelector('.fixed').remove();

            // Reload current tab data
            const activeTab = document.querySelector('[class*="bg-blue-600"]').id;
            if (activeTab === 'portfolioTab') {
                loadPortfolio(customerId);
            } else if (activeTab === 'transactionsTab') {
                loadTransactions(customerId);
            }
        }
    } catch (error) {
        console.error('Error executing trade:', error);
        console.log('Error response:', error.response);
        console.log('Error data:', error.response?.data);

        let errorMessage = 'Unknown error occurred';

        if (error.response?.data?.detail) {
            errorMessage = error.response.data.detail;
        } else if (error.response?.data?.message) {
            errorMessage = error.response.data.message;
        } else if (error.message) {
            errorMessage = error.message;
        } else if (typeof error === 'string') {
            errorMessage = error;
        }

        alert('Error executing trade: ' + errorMessage);
    }
}
