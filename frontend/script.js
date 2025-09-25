async function search() {
    const query = document.getElementById('queryInput').value.trim();
    const searchBtn = document.getElementById('searchBtn');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const error = document.getElementById('error');

    // Hide previous results and errors
    results.classList.add('hidden');
    error.classList.add('hidden');

    if (!query) {
        showError('Please enter a research query');
        return;
    }

    // Disable button and show loading
    searchBtn.disabled = true;
    searchBtn.textContent = 'Researching...';
    loading.classList.remove('hidden');

    try {
        const response = await fetch('/api/research', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Research failed');
        }

        const data = await response.json();
        displayResults(data);

    } catch (err) {
        showError(err.message);
    } finally {
        searchBtn.disabled = false;
        searchBtn.textContent = 'Research';
        loading.classList.add('hidden');
    }
}

function displayResults(data) {
    const summaryElement = document.getElementById('summary');
    const sourcesElement = document.getElementById('sources');
    const statsElement = document.getElementById('stats');
    const results = document.getElementById('results');

    // Display summary with markdown-like formatting
    summaryElement.innerHTML = formatSummary(data.summary);

    // Display sources (up to 15)
    sourcesElement.innerHTML = data.sources.map((source, index) => `
        <div class="source-item">
            <div class="source-title">${source.title || 'No title available'}</div>
            <div class="source-snippet">${source.snippet || 'No description available'}</div>
            <div class="source-meta">
                <span>${source.source}</span>
                <a href="${source.link}" target="_blank" rel="noopener noreferrer">Visit Source →</a>
            </div>
        </div>
    `).join('');

    // Display statistics
    statsElement.innerHTML = `
        <div class="stat-item">
            <div class="stat-value">${data.word_count}</div>
            <div class="stat-label">Words Generated</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">${data.sources.length}</div>
            <div class="stat-label">Sources Analyzed</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">${data.processing_time.toFixed(2)}s</div>
            <div class="stat-label">Processing Time</div>
        </div>
    `;

    results.classList.remove('hidden');
    
    // Smooth scroll to results
    results.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function formatSummary(summary) {
    // Enhanced markdown to HTML conversion
    let html = summary
        // Headers
        .replace(/#### (.*?)(\n|$)/g, '<h4>$1</h4>')
        .replace(/### (.*?)(\n|$)/g, '<h3>$1</h3>')
        .replace(/## (.*?)(\n|$)/g, '<h2>$1</h2>')
        .replace(/# (.*?)(\n|$)/g, '<h1>$1</h1>')
        // Bold and italic
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        // Code and code blocks
        .replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
        .replace(/`(.*?)`/g, '<code>$1</code>')
        // Lists
        .replace(/\n- (.*?)(\n|$)/g, '<li>$1</li>')
        .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
        .replace(/\n\d+\. (.*?)(\n|$)/g, '<li>$1</li>')
        .replace(/(<li>.*<\/li>)/s, '<ol>$1</ol>')
        // Line breaks and paragraphs
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>');

    // Wrap in paragraph if needed
    if (!html.startsWith('<')) {
        html = '<p>' + html + '</p>';
    }

    return html;
}

function showError(message) {
    const errorElement = document.getElementById('error');
    errorElement.textContent = message;
    errorElement.classList.remove('hidden');
    
    // Smooth scroll to error
    errorElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Allow pressing Enter to search
document.getElementById('queryInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        search();
    }
});

// Add some interactive effects
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('queryInput');
    input.focus();
    
    // Add floating animation to header
    const header = document.querySelector('header');
    if (header) {
        header.style.animation = 'float 6s ease-in-out infinite';
    }
});

// Add floating animation
const style = document.createElement('style');
style.textContent = `
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
`;
document.head.appendChild(style);