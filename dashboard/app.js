// AI Radar Dashboard
// Loads data from data/processed/items.json and displays it by category

const DATA_PATH = '../../data/processed/items.json';

// Category mapping
const CATEGORIES = {
    'model_releases': 'model-releases',
    'research': 'research',
    'open_source': 'open-source',
    'industry': 'industry',
    'policy': 'policy'
};

// Quick take messages based on data
const QUICK_TAKE_MESSAGES = [
    "The AI ecosystem continues to evolve rapidly. Focus on model releases, agent frameworks, and regulatory developments as key areas to watch.",
    "Major developments in AI agents and multimodal models are shaping the industry. Stay tuned for more updates.",
    "Open-source AI tools are gaining momentum. Developers are increasingly adopting agent frameworks for production.",
    "Regulatory discussions around AI safety are intensifying globally. Organizations should monitor policy developments."
];

// Initialize dashboard
async function init() {
    try {
        const response = await fetch(DATA_PATH);
        if (!response.ok) {
            throw new Error('Failed to load data');
        }
        
        const items = await response.json();
        
        // Update last updated time
        document.getElementById('last-updated').textContent = 
            `Last updated: ${new Date().toLocaleString()}`;
        
        // Group items by category
        const grouped = groupByCategory(items);
        
        // Render each category
        renderCategory('model-releases', grouped['model_releases'] || []);
        renderCategory('research', grouped['research'] || []);
        renderCategory('open-source', grouped['open_source'] || []);
        renderCategory('industry', grouped['industry'] || []);
        renderCategory('policy', grouped['policy'] || []);
        
        // Set quick take
        setQuickTake(items);
        
    } catch (error) {
        console.error('Error loading data:', error);
        showError();
    }
}

// Group items by category
function groupByCategory(items) {
    const grouped = {};
    
    for (const item of items) {
        const category = item.category || 'industry';
        if (!grouped[category]) {
            grouped[category] = [];
        }
        grouped[category].push(item);
    }
    
    // Sort by date (newest first)
    for (const category in grouped) {
        grouped[category].sort((a, b) => {
            return new Date(b.published) - new Date(a.published);
        });
    }
    
    return grouped;
}

// Render a category section
function renderCategory(elementId, items) {
    const container = document.getElementById(elementId);
    
    if (!items || items.length === 0) {
        container.innerHTML = '<p class="empty">No items in this category</p>';
        return;
    }
    
    // Limit to 5 items per category
    const displayItems = items.slice(0, 5);
    
    const html = displayItems.map(item => `
        <div class="item">
            <h3>
                <a href="${item.url || '#'}" target="_blank" rel="noopener">
                    ${escapeHtml(item.title || 'Untitled')}
                </a>
                ${item.language ? `<span class="language">${escapeHtml(item.language)}</span>` : ''}
            </h3>
            <p class="meta">${escapeHtml(item.source || '')} ${item.published ? '• ' + item.published : ''}</p>
            ${item.summary ? `<p class="summary">${escapeHtml(item.summary)}</p>` : ''}
        </div>
    `).join('');
    
    container.innerHTML = html;
}

// Set quick take message
function setQuickTake(items) {
    const quickTakeEl = document.getElementById('quick-take');
    
    // Select a message based on item count
    const itemCount = items.length;
    
    if (itemCount === 0) {
        quickTakeEl.textContent = "No data available. Run the daily pipeline to generate new content.";
    } else if (itemCount < 10) {
        quickTakeEl.textContent = QUICK_TAKE_MESSAGES[0];
    } else if (itemCount < 30) {
        quickTakeEl.textContent = QUICK_TAKE_MESSAGES[1];
    } else {
        quickTakeEl.textContent = QUICK_TAKE_MESSAGES[2];
    }
}

// Show error state
function showError() {
    const sections = ['model-releases', 'research', 'open-source', 'industry', 'policy'];
    
    for (const id of sections) {
        document.getElementById(id).innerHTML = 
            '<p class="empty">Error loading data. Please run the daily pipeline first.</p>';
    }
    
    document.getElementById('quick-take').textContent = 
        'Unable to load data. Run: python scripts/run_daily.py';
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', init);
