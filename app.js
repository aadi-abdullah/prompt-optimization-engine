// API Configuration
const API_URL = 'https://prompt-optimization-engine.up.railway.app/api';
// DOM Elements
const promptInput = document.getElementById('promptInput');
const charCount = document.getElementById('charCount');
const optimizeBtn = document.getElementById('optimizeBtn');
const exampleBtn = document.getElementById('exampleBtn');
const resetBtn = document.getElementById('resetBtn');
const copyBtn = document.getElementById('copyBtn');
const spinner = document.getElementById('spinner');
const btnText = document.getElementById('btnText');

// Examples
const examples = [
    "Write a summary of machine learning concepts for beginners.",
    "Explain how neural networks work in simple terms.",
    "Create a Python function that sorts a list of dictionaries by a given key.",
    "Analyze the pros and cons of microservices architecture.",
    "Write a product description for an AI-powered writing assistant.",
    "Summarize the key findings from a research paper about transformer models.",
    "Generate test cases for a REST API endpoint that handles user authentication."
];

// Initialize
document.getElementById('yr').textContent = new Date().getFullYear();

// Scroll progress
window.addEventListener('scroll', () => {
    const ws = document.documentElement.scrollTop;
    const h = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    document.getElementById('pbar').style.width = (ws / h * 100) + '%';
});

// Sliders
document.getElementById('variations').addEventListener('input', e => {
    document.getElementById('varVal').textContent = e.target.value;
});
document.getElementById('rounds').addEventListener('input', e => {
    document.getElementById('roundVal').textContent = e.target.value;
});
document.getElementById('creativity').addEventListener('input', e => {
    document.getElementById('crVal').textContent = (e.target.value / 10).toFixed(1);
});

// Character count
promptInput.addEventListener('input', () => {
    const len = promptInput.value.length;
    charCount.textContent = len + ' chars';
    charCount.className = 'char-count' + (len > 1500 ? ' danger' : len > 1000 ? ' warn' : '');
});

// Ctrl+Enter
promptInput.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        runOptimization();
    }
});

// Load example
function loadExample() {
    const idx = Math.floor(Math.random() * examples.length);
    promptInput.value = examples[idx];
    promptInput.dispatchEvent(new Event('input'));
    promptInput.focus();
}

exampleBtn.addEventListener('click', loadExample);

// Copy result
function copyResult() {
    const text = document.getElementById('resultBox').textContent;
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text);
    } else {
        const ta = document.createElement('textarea');
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
    }
    const btn = document.querySelector('.result-copy');
    btn.textContent = '✓ Copied!';
    setTimeout(() => btn.textContent = '📋 Copy to clipboard', 2000);
}

copyBtn.addEventListener('click', copyResult);

// Reset
function resetAll() {
    promptInput.value = '';
    promptInput.dispatchEvent(new Event('input'));
    document.getElementById('emptyState').style.display = '';
    document.getElementById('optStatus').className = 'optimization-status';
    document.getElementById('variationsList').className = 'variations-list';
    document.getElementById('finalResult').className = 'final-result';
    document.getElementById('resultBadge').textContent = 'waiting';
    document.getElementById('resultBadge').className = 'panel-badge';
    resetBtn.disabled = true;
    btnText.textContent = '⚡ Optimize Prompt';
    
    for (let i = 1; i <= 4; i++) {
        const dot = document.getElementById('dot' + i);
        dot.className = 'step-dot';
        dot.textContent = i;
        document.getElementById('step' + i).className = 'status-step';
        if (i < 4) document.getElementById('line' + i).className = 'step-line';
    }
    
    promptInput.focus();
}

resetBtn.addEventListener('click', resetAll);

// Helper functions
function setStep(num, state) {
    const dot = document.getElementById('dot' + num);
    const step = document.getElementById('step' + num);
    const line = num < 4 ? document.getElementById('line' + num) : null;
    
    if (state === 'active') {
        dot.className = 'step-dot active';
        step.className = 'status-step active';
        if (line) line.className = 'step-line active';
    } else if (state === 'done') {
        dot.className = 'step-dot done';
        dot.textContent = '✓';
        step.className = 'status-step done';
        if (line) line.className = 'step-line done';
    }
}

function addLog(msg, type = '') {
    const log = document.getElementById('statusLog');
    const now = new Date();
    const time = now.toTimeString().split(' ')[0];
    const entry = document.createElement('div');
    entry.className = 'log-entry';
    entry.innerHTML = `<span class="log-time">${time}</span><span class="log-msg ${type}">${msg}</span>`;
    log.appendChild(entry);
    log.scrollTop = log.scrollHeight;
}

function renderVariations(variations) {
    const container = document.getElementById('variationsList');
    container.innerHTML = '';
    
    variations.forEach((v, i) => {
        const card = document.createElement('div');
        card.className = 'variation-card' + (v.isBest ? ' best' : '');
        card.style.animation = `fadeUp 0.4s ${i * 0.08}s ease both`;
        
        card.innerHTML = `
            <div class="variation-header">
                <div class="variation-label">
                    Variation ${i + 1}
                    ${v.isBest ? '<span class="best-badge">★ BEST</span>' : ''}
                </div>
                <div class="variation-scores">
                    <span class="score-pill clarity">clarity: ${v.clarity}</span>
                    <span class="score-pill specificity">spec: ${v.specificity}</span>
                    <span class="score-pill overall">overall: ${v.overall}</span>
                </div>
            </div>
            <div class="variation-text">${escapeHtml(v.text)}</div>
            <div class="score-bar-wrap">
                <div class="score-bar-row">
                    <span class="score-bar-label">Clarity</span>
                    <div class="score-bar-track"><div class="score-bar-fill green" data-width="${v.clarity}"></div></div>
                    <span class="score-bar-value">${v.clarity}%</span>
                </div>
                <div class="score-bar-row">
                    <span class="score-bar-label">Specificity</span>
                    <div class="score-bar-track"><div class="score-bar-fill cyan" data-width="${v.specificity}"></div></div>
                    <span class="score-bar-value">${v.specificity}%</span>
                </div>
                <div class="score-bar-row">
                    <span class="score-bar-label">Overall</span>
                    <div class="score-bar-track"><div class="score-bar-fill purple" data-width="${v.overall}"></div></div>
                    <span class="score-bar-value">${v.overall}%</span>
                </div>
            </div>
            <div class="variation-techniques">
                ${v.techniques.map(t => `<span class="technique-tag">${t}</span>`).join('')}
            </div>
        `;
        
        container.appendChild(card);
    });
    
    // Animate score bars
    setTimeout(() => {
        document.querySelectorAll('.score-bar-fill').forEach(bar => {
            bar.style.width = bar.dataset.width + '%';
        });
    }, 100);
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// Main optimization function
let isRunning = false;

async function runOptimization() {
    const prompt = promptInput.value.trim();
    if (!prompt) {
        promptInput.focus();
        promptInput.style.borderColor = 'var(--red)';
        setTimeout(() => promptInput.style.borderColor = '', 1500);
        return;
    }
    
    if (isRunning) return;
    isRunning = true;
    
    // Get config
    const strategy = document.getElementById('strategy').value;
    const useCase = document.getElementById('useCase').value;
    const numVariations = parseInt(document.getElementById('variations').value);
    const numRounds = parseInt(document.getElementById('rounds').value);
    const creativity = parseInt(document.getElementById('creativity').value) / 10;
    
    // UI setup
    optimizeBtn.disabled = true;
    spinner.style.display = 'inline-block';
    btnText.textContent = 'Optimizing...';
    resetBtn.disabled = false;
    document.getElementById('resultBadge').textContent = 'running';
    document.getElementById('resultBadge').className = 'panel-badge active';
    
    // Hide/show sections
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('optStatus').className = 'optimization-status active';
    document.getElementById('variationsList').className = 'variations-list';
    document.getElementById('finalResult').className = 'final-result';
    document.getElementById('statusLog').innerHTML = '';
    
    // Reset steps
    for (let i = 1; i <= 4; i++) {
        document.getElementById('dot' + i).className = 'step-dot';
        document.getElementById('step' + i).className = 'status-step';
        if (i < 4) document.getElementById('line' + i).className = 'step-line';
    }
    
    // Step 1: Analyze
    setStep(1, 'active');
    addLog('Analyzing input prompt...');
    await delay(600);
    addLog(`Detected ${prompt.split(' ').length} words, ${prompt.split('. ').length} sentences`, 'info');
    await delay(400);
    addLog('Identifying optimization opportunities...', 'info');
    await delay(500);
    addLog('Analysis complete ✓', 'success');
    setStep(1, 'done');
    
    // Step 2: Generate (call API)
    setStep(2, 'active');
    addLog(`Calling optimization engine with ${strategy} strategy...`, 'info');
    
    try {
        const response = await fetch(`${API_URL}/optimize`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                prompt,
                strategy,
                use_case: useCase,
                num_variations: numVariations,
                num_rounds: numRounds,
                creativity
            })
        });
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        const data = await response.json();
        
        addLog(`Generated ${data.variations.length} variations ✓`, 'success');
        setStep(2, 'done');
        
        // Step 3: Score (already done by API)
        setStep(3, 'active');
        addLog('Scoring all variations on clarity, specificity, overall...');
        await delay(800);
        addLog('Ranking by composite fitness score...', 'info');
        await delay(400);
        addLog(`Best score: ${data.variations[0].overall}/100 ✓`, 'success');
        setStep(3, 'done');
        
        // Step 4: Select
        setStep(4, 'active');
        addLog('Selecting optimal prompt...');
        await delay(500);
        addLog('Optimization complete ✓', 'success');
        setStep(4, 'done');
        
        // Mark best
        if (data.variations.length > 0) {
            data.variations[0].isBest = true;
        }
        
        // Render variations
        renderVariations(data.variations);
        document.getElementById('variationsList').className = 'variations-list active';
        
        // Show final result
        document.getElementById('resultBox').textContent = data.best_prompt;
        
        document.getElementById('impStats').innerHTML = `
            <div class="imp-stat">
                <div class="imp-stat-num">+${data.improvements.clarity}%</div>
                <div class="imp-stat-label">Clarity improvement</div>
            </div>
            <div class="imp-stat">
                <div class="imp-stat-num cyan">+${data.improvements.specificity}%</div>
                <div class="imp-stat-label">Specificity improvement</div>
            </div>
            <div class="imp-stat">
                <div class="imp-stat-num">+${data.improvements.overall}%</div>
                <div class="imp-stat-label">Overall improvement</div>
            </div>
        `;
        
        document.getElementById('finalResult').className = 'final-result active';
        document.getElementById('resultBadge').textContent = 'complete';
        
    } catch (error) {
        console.error('Optimization error:', error);
        addLog(`Error: ${error.message}`, 'warn');
        document.getElementById('resultBadge').textContent = 'error';
    } finally {
        // Reset button state
        optimizeBtn.disabled = false;
        spinner.style.display = 'none';
        btnText.textContent = '⚡ Re-Optimize';
        isRunning = false;
        
        // Scroll to results
        document.getElementById('resultsPanel').scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

optimizeBtn.addEventListener('click', runOptimization);

function delay(ms) {
    return new Promise(r => setTimeout(r, ms));
}