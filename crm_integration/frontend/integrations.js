// Integrations Page JavaScript
const API_BASE = 'http://localhost:8000';

let integrations = {
    linkedin: null,
    telegram: null
};

document.addEventListener('DOMContentLoaded', () => {
    loadIntegrations();
});

async function loadIntegrations() {
    try {
        const response = await fetch(`${API_BASE}/api/integrations`);
        const data = await response.json();
        
        // Map integrations by platform
        data.integrations.forEach(integration => {
            integrations[integration.platform] = integration;
        });
        
        // Update UI
        updateLinkedInUI();
        updateTelegramUI();
        
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('integrations-container').classList.remove('hidden');
    } catch (error) {
        console.error('Error loading integrations:', error);
        document.getElementById('loading').innerHTML = '<p class="text-red-500">Error loading integrations</p>';
    }
}

function updateLinkedInUI() {
    const linkedin = integrations.linkedin;
    
    if (linkedin && linkedin.status === 'connected') {
        // Update status
        document.getElementById('linkedin-status').textContent = 'Connected';
        document.getElementById('linkedin-badge').innerHTML = '<i class="fas fa-circle mr-1 text-green-500"></i>Active';
        document.getElementById('linkedin-badge').className = 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800';
        
        // Show details
        document.getElementById('linkedin-details').classList.remove('hidden');
        document.getElementById('linkedin-account').textContent = linkedin.account_name || linkedin.account_email || '—';
        document.getElementById('linkedin-connected').textContent = formatDate(linkedin.connected_at);
        document.getElementById('linkedin-messages').textContent = linkedin.messages_sent || 0;
        document.getElementById('linkedin-connections').textContent = linkedin.connections_made || 0;
        
        // Update button
        document.getElementById('linkedin-btn').innerHTML = '<i class="fas fa-unlink mr-2"></i>Disconnect';
        document.getElementById('linkedin-btn').className = 'w-full px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors';
        document.getElementById('linkedin-btn').onclick = () => disconnectIntegration('linkedin');
    }
}

function updateTelegramUI() {
    const telegram = integrations.telegram;
    
    if (telegram && telegram.status === 'connected') {
        // Update status
        document.getElementById('telegram-status').textContent = 'Connected';
        document.getElementById('telegram-badge').innerHTML = '<i class="fas fa-circle mr-1 text-green-500"></i>Active';
        document.getElementById('telegram-badge').className = 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800';
        
        // Show details
        document.getElementById('telegram-details').classList.remove('hidden');
        document.getElementById('telegram-bot').textContent = telegram.account_name || '—';
        document.getElementById('telegram-connected').textContent = formatDate(telegram.connected_at);
        document.getElementById('telegram-messages').textContent = telegram.messages_sent || 0;
        
        // Update button
        document.getElementById('telegram-btn').innerHTML = '<i class="fas fa-unlink mr-2"></i>Disconnect';
        document.getElementById('telegram-btn').className = 'w-full px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors';
        document.getElementById('telegram-btn').onclick = () => disconnectIntegration('telegram');
    }
}

// LinkedIn Connection
function connectLinkedIn() {
    document.getElementById('linkedin-modal').classList.remove('hidden');
}

function closeLinkedInModal() {
    document.getElementById('linkedin-modal').classList.add('hidden');
    document.getElementById('linkedin-email').value = '';
    document.getElementById('linkedin-password').value = '';
}

async function saveLinkedInConnection() {
    const email = document.getElementById('linkedin-email').value.trim();
    const password = document.getElementById('linkedin-password').value.trim();
    
    if (!email || !password) {
        alert('Please enter both email and password');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/integrations/linkedin/connect`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            alert('LinkedIn connected successfully!');
            closeLinkedInModal();
            loadIntegrations(); // Reload to show updated status
        } else {
            const error = await response.json();
            alert(`Failed to connect LinkedIn: ${error.detail}`);
        }
    } catch (error) {
        console.error('Error connecting LinkedIn:', error);
        alert('Error connecting LinkedIn');
    }
}

// Telegram Connection
function connectTelegram() {
    document.getElementById('telegram-modal').classList.remove('hidden');
}

function closeTelegramModal() {
    document.getElementById('telegram-modal').classList.add('hidden');
    document.getElementById('telegram-token').value = '';
}

async function saveTelegramConnection() {
    const token = document.getElementById('telegram-token').value.trim();
    
    if (!token) {
        alert('Please enter bot token');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/integrations/telegram/connect`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                bot_token: token
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            alert('Telegram bot connected successfully!');
            closeTelegramModal();
            loadIntegrations(); // Reload to show updated status
        } else {
            const error = await response.json();
            alert(`Failed to connect Telegram: ${error.detail}`);
        }
    } catch (error) {
        console.error('Error connecting Telegram:', error);
        alert('Error connecting Telegram');
    }
}

// Disconnect Integration
async function disconnectIntegration(platform) {
    if (!confirm(`Are you sure you want to disconnect ${platform}?`)) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/integrations/${platform}/disconnect`, {
            method: 'POST'
        });
        
        if (response.ok) {
            alert(`${platform} disconnected successfully`);
            loadIntegrations(); // Reload to show updated status
        } else {
            const error = await response.json();
            alert(`Failed to disconnect: ${error.detail}`);
        }
    } catch (error) {
        console.error('Error disconnecting:', error);
        alert('Error disconnecting integration');
    }
}

// Utility Functions
function formatDate(dateString) {
    if (!dateString) return '—';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

