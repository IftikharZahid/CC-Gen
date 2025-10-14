// Card checker implementation
class CardChecker {
    constructor() {
        this.results = [];
        this.isChecking = false;
        this.init();
    }

    init() {
        this.bindEvents();
    }

    bindEvents() {
        document.getElementById('checkBtn').addEventListener('click', () => this.checkCards());
        document.getElementById('clearBtn').addEventListener('click', () => this.clearAll());
        document.getElementById('exportBtn').addEventListener('click', () => this.exportResults());
        
        // Enter key support for textarea
        document.getElementById('cardsInput').addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                this.checkCards();
            }
        });
    }

    parseCards(input) {
        const lines = input.split('\n').filter(line => line.trim());
        const cards = [];

        lines.forEach(line => {
            const trimmed = line.trim();
            
            // Support multiple formats:
            // 1. Full format: 4111111111111111|01|25|123
            // 2. Card number only: 4111111111111111
            if (trimmed.includes('|')) {
                const parts = trimmed.split('|');
                if (parts[0] && this.isValidCardNumber(parts[0])) {
                    cards.push({
                        number: parts[0],
                        expiry: parts[1] && parts[2] ? `${parts[1]}|${parts[2]}` : null,
                        cvv: parts[3] || null,
                        original: trimmed
                    });
                }
            } else if (this.isValidCardNumber(trimmed)) {
                cards.push({
                    number: trimmed,
                    expiry: null,
                    cvv: null,
                    original: trimmed
                });
            }
        });

        return cards;
    }

    isValidCardNumber(number) {
        const cleaned = number.replace(/\s/g, '');
        return /^\d{13,19}$/.test(cleaned) && this.luhnCheck(cleaned);
    }

    luhnCheck(number) {
        const digits = String(number).split('').map(Number);
        const oddDigits = digits.reverse().filter((_, index) => index % 2 === 0);
        const evenDigits = digits.reverse().filter((_, index) => index % 2 === 1);
        
        let checksum = oddDigits.reduce((sum, digit) => sum + digit, 0);
        
        for (let digit of evenDigits) {
            const doubled = digit * 2;
            checksum += doubled > 9 ? doubled - 9 : doubled;
        }
        
        return checksum % 10 === 0;
    }

    async simulateCardCheck(card) {
        // Very fast simulation for bulk processing
        await new Promise(resolve => setTimeout(resolve, 10 + Math.random() * 20));
        
        // Realistic status simulation
        const randomFactor = Math.random();
        
        if (randomFactor < 0.4) { // 40% live
            return 'live';
        } else if (randomFactor < 0.7) { // 30% dead
            return 'dead';
        } else { // 30% unknown
            return 'unknown';
        }
    }

    async checkCards() {
        const input = document.getElementById('cardsInput').value.trim();
        const checkBtn = document.getElementById('checkBtn');
        const loadingOverlay = document.getElementById('loadingOverlay');

        if (!input) {
            alert('Please enter at least one credit card to check.');
            return;
        }

        const cards = this.parseCards(input);
        
        if (cards.length === 0) {
            alert('No valid credit cards found. Please check your input format.');
            return;
        }

        // Update UI
        this.isChecking = true;
        checkBtn.disabled = true;
        checkBtn.innerHTML = '<span class="btn-icon">⏳</span> Checking...';
        loadingOverlay.classList.add('active');

        try {
            this.results = [];
            let completed = 0;

            // Process ALL cards with proper progress tracking
            for (let i = 0; i < cards.length; i++) {
                if (!this.isChecking) break; // Allow cancellation
                
                const card = cards[i];
                const status = await this.simulateCardCheck(card);
                
                this.results.push({
                    ...card,
                    status: status,
                    checkedAt: new Date().toISOString()
                });

                completed++;
                const progress = Math.round((completed / cards.length) * 100);
                document.getElementById('loadingProgress').textContent = `${progress}%`;

                // Update UI more frequently for better feedback
                if (completed % 5 === 0 || completed === cards.length) {
                    // Force UI update
                    await new Promise(resolve => setTimeout(resolve, 0));
                }
            }

            this.displayResults();
            
        } catch (error) {
            console.error('Error checking cards:', error);
            alert('Error checking cards: ' + error.message);
        } finally {
            this.isChecking = false;
            checkBtn.disabled = false;
            checkBtn.innerHTML = '<span class="btn-icon">🔍</span> Check Cards';
            loadingOverlay.classList.remove('active');
        }
    }

    displayResults() {
        const cardsDisplay = document.getElementById('cardsDisplay');
        const cardsCount = document.getElementById('cardsCount');
        const resultsSection = document.getElementById('resultsSection');
        const statsContainer = document.getElementById('statsContainer');

        if (this.results.length === 0) {
            cardsDisplay.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">🔍</div>
                    <div class="empty-text">No cards checked</div>
                    <div class="empty-subtext">Enter cards and click "Check Cards" to start</div>
                </div>
            `;
            cardsCount.textContent = '0 cards';
            resultsSection.classList.remove('active');
            statsContainer.style.display = 'none';
            return;
        }

        // Calculate stats
        const liveCount = this.results.filter(r => r.status === 'live').length;
        const deadCount = this.results.filter(r => r.status === 'dead').length;
        const unknownCount = this.results.filter(r => r.status === 'unknown').length;

        // Update stats
        document.getElementById('liveCount').textContent = liveCount;
        document.getElementById('deadCount').textContent = deadCount;
        document.getElementById('unknownCount').textContent = unknownCount;

        // Display cards
        let html = '';
        
        this.results.forEach((result, index) => {
            const statusClass = `status-${result.status}`;
            const statusBadge = result.status.toUpperCase();
            
            html += `
                <div class="card-item" onclick="cardChecker.copyCard(${index})">
                    <span class="status-badge ${statusClass}">${statusBadge}</span>
                    <span class="card-number">${this.formatCardNumber(result.number)}</span>
                    ${result.expiry ? `<span class="card-details">${result.expiry}${result.cvv ? ` | ${result.cvv}` : ''}</span>` : ''}
                </div>
            `;
        });

        cardsDisplay.innerHTML = html;
        cardsCount.textContent = `${this.results.length} card${this.results.length !== 1 ? 's' : ''}`;
        resultsSection.classList.add('active');
        statsContainer.style.display = 'grid';
        
        // Auto-scroll to results
        setTimeout(() => {
            resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 300);
    }

    formatCardNumber(number) {
        return number.replace(/(\d{4})/g, '$1 ').trim();
    }

    copyCard(index) {
        const card = this.results[index];
        const textToCopy = card.original;
        
        this.copyToClipboard(textToCopy);
        
        // Show visual feedback
        const cardElement = document.querySelectorAll('.card-item')[index];
        cardElement.classList.add('copied');
        
        // Show toast notification
        this.showToast('Card copied to clipboard!');
        
        // Remove the copied class after animation
        setTimeout(() => {
            cardElement.classList.remove('copied');
        }, 1000);
    }

    exportResults() {
        if (this.results.length === 0) {
            alert('No results to export.');
            return;
        }

        const csvContent = this.results.map(result => 
            `"${result.number}","${result.status}","${result.expiry || ''}","${result.cvv || ''}"`
        ).join('\n');

        const csv = `Card Number,Status,Expiry,CVV\n${csvContent}`;
        
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `card-checker-results-${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);

        this.showToast('Results exported successfully!');
    }

    clearAll() {
        document.getElementById('cardsInput').value = '';
        this.results = [];
        this.displayResults();
    }

    copyToClipboard(text) {
        if (navigator.clipboard && window.isSecureContext) {
            navigator.clipboard.writeText(text).catch(() => {
                this.fallbackCopy(text);
            });
        } else {
            this.fallbackCopy(text);
        }
    }

    fallbackCopy(text) {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.opacity = '0';
        document.body.appendChild(textArea);
        textArea.select();
        
        try {
            document.execCommand('copy');
        } catch (err) {
            console.error('Fallback copy failed:', err);
            alert('Copy failed. Please select and copy manually.');
        }
        
        document.body.removeChild(textArea);
    }

    showToast(message) {
        const toast = document.getElementById('copyToast');
        const toastText = toast.querySelector('.toast-text');
        
        toastText.textContent = message;
        toast.classList.add('show');
        
        setTimeout(() => {
            toast.classList.remove('show');
        }, 2000);
    }
}

// Initialize card checker
const cardChecker = new CardChecker();
// Add cancel functionality
document.getElementById('cancelBtn').addEventListener('click', () => {
    cardChecker.isChecking = false;
});
