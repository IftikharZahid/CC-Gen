// Luhn algorithm implementation
function luhnCheck(number) {
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

function calculateLuhnCheckDigit(number) {
    let checksum = 0;
    const digits = String(number).split('').map(Number);
    
    for (let i = 0; i < digits.length; i++) {
        let digit = digits[digits.length - 1 - i];
        if (i % 2 === 1) {
            digit *= 2;
            if (digit > 9) digit -= 9;
        }
        checksum += digit;
    }
    
    return (10 - (checksum % 10)) % 10;
}

function generateValidCardNumber(binNumber) {
    const remainingLength = 15 - binNumber.length;
    let middleDigits = '';
    
    for (let i = 0; i < remainingLength - 1; i++) {
        middleDigits += Math.floor(Math.random() * 10);
    }
    
    const partialNumber = binNumber + middleDigits;
    const checkDigit = calculateLuhnCheckDigit(partialNumber);
    return partialNumber + checkDigit;
}

function generateRandomExpiry() {
    const month = Math.floor(Math.random() * 12) + 1;
    const year = Math.floor(Math.random() * 7) + 24;
    return {
        month: month.toString().padStart(2, '0'),
        year: year.toString()
    };
}

function generateFixedExpiry() {
    const month = document.getElementById('monthSelect').value;
    const year = document.getElementById('yearInput').value.trim() || '24';
    return {
        month: month,
        year: year.padStart(2, '0')
    };
}

function generateRandomCVV() {
    return Array.from({length: 3}, () => Math.floor(Math.random() * 10)).join('');
}

function getCVV() {
    const cvvOption = document.querySelector('input[name="cvvOption"]:checked').value;
    if (cvvOption === 'manual') {
        const manualCVV = document.getElementById('manualCVV').value.trim();
        return manualCVV || generateRandomCVV();
    }
    return generateRandomCVV();
}

let generatedCards = [];

// Initialize event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Date option toggle
    const dateRadios = document.querySelectorAll('input[name="dateOption"]');
    const dateOptions = document.getElementById('dateOptions');
    
    dateRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'fixed') {
                dateOptions.classList.add('active');
            } else {
                dateOptions.classList.remove('active');
            }
        });
    });
    
    // CVV option toggle
    const cvvRadios = document.querySelectorAll('input[name="cvvOption"]');
    const cvvOptions = document.getElementById('cvvOptions');
    
    cvvRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'manual') {
                cvvOptions.classList.add('active');
                document.getElementById('manualCVV').focus();
            } else {
                cvvOptions.classList.remove('active');
            }
        });
    });
    
    // Generate button
    document.getElementById('generateBtn').addEventListener('click', generateCards);
    
    // Copy all button
    document.getElementById('copyBtn').addEventListener('click', copyAllCards);
    
    // Clear all button
    document.getElementById('clearBtn').addEventListener('click', clearAllCards);
    
    // Enter key support for BIN input
    document.getElementById('binInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            generateCards();
        }
    });
    
    // Input validation for BIN
    document.getElementById('binInput').addEventListener('input', function() {
        this.value = this.value.replace(/[^0-9]/g, '').slice(0, 6);
    });
    
    // Input validation for year
    document.getElementById('yearInput').addEventListener('input', function() {
        this.value = this.value.replace(/[^0-9]/g, '').slice(0, 2);
    });
    
    // Input validation for manual CVV
    document.getElementById('manualCVV').addEventListener('input', function() {
        this.value = this.value.replace(/[^0-9]/g, '').slice(0, 3);
    });
    
    // Quantity input validation
    document.getElementById('quantityInput').addEventListener('change', function() {
        let value = parseInt(this.value);
        if (isNaN(value) || value < 1) this.value = 1;
        if (value > 100) this.value = 100;
    });
});

function generateCards() {
    const bin = document.getElementById('binInput').value.trim();
    const quantity = parseInt(document.getElementById('quantityInput').value) || 10;
    const dateOption = document.querySelector('input[name="dateOption"]:checked').value;
    const generateBtn = document.getElementById('generateBtn');

    // Validate BIN
    if (!bin || bin.length !== 6) {
        alert('BIN must be exactly 6 digits!');
        document.getElementById('binInput').focus();
        return;
    }

    // Validate manual CVV if selected
    const cvvOption = document.querySelector('input[name="cvvOption"]:checked').value;
    if (cvvOption === 'manual') {
        const manualCVV = document.getElementById('manualCVV').value.trim();
        if (!manualCVV || manualCVV.length !== 3 || !/^\d+$/.test(manualCVV)) {
            alert('Please enter a valid 3-digit CVV');
            document.getElementById('manualCVV').focus();
            return;
        }
    }

    // Validate fixed date if selected
    if (dateOption === 'fixed') {
        const year = document.getElementById('yearInput').value.trim();
        if (!year || year.length !== 2 || !/^\d+$/.test(year)) {
            alert('Please enter a valid 2-digit year (e.g., 24 for 2024)');
            document.getElementById('yearInput').focus();
            return;
        }
    }

    // Update UI
    generateBtn.disabled = true;
    generateBtn.innerHTML = '<span class="btn-icon">⏳</span> Generating...';

    // Generate cards
    setTimeout(() => {
        try {
            generatedCards = [];
            
            for (let i = 0; i < quantity; i++) {
                const cardNumber = generateValidCardNumber(bin);
                const expiry = dateOption === 'fixed' ? generateFixedExpiry() : generateRandomExpiry();
                const cvv = getCVV();
                
                // Format: 411111363135951|01|24|567
                const cardData = {
                    number: cardNumber,
                    expiry: expiry,
                    cvv: cvv,
                    index: i + 1,
                    formatted: `${cardNumber}|${expiry.month}|${expiry.year}|${cvv}`
                };
                
                generatedCards.push(cardData);
            }
            
            displayCards(generatedCards);
            generateBtn.disabled = false;
            generateBtn.innerHTML = '<span class="btn-icon">⚡</span> Generate Cards';
            
        } catch (error) {
            alert('Generation failed: ' + error.message);
            generateBtn.disabled = false;
            generateBtn.innerHTML = '<span class="btn-icon">⚡</span> Generate Cards';
        }
    }, 100);
}

function displayCards(cards) {
    const cardsDisplay = document.getElementById('cardsDisplay');
    const cardsCount = document.getElementById('cardsCount');
    const resultsSection = document.getElementById('resultsSection');
    
    if (cards.length === 0) {
        cardsDisplay.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">💳</div>
                <div class="empty-text">No cards generated!</div>
                <div class="empty-subtext">Click "Generate Cards" to start!</div>
            </div>
        `;
        cardsCount.textContent = '0 cards';
        resultsSection.classList.remove('active');
        return;
    }

    let html = '';
    
    cards.forEach((card, index) => {
        html += `
            <div class="card-item" onclick="copySingleCard(${index})">
                ${card.formatted}
            </div>
        `;
    });

    cardsDisplay.innerHTML = html;
    cardsCount.textContent = `${cards.length} card${cards.length !== 1 ? 's' : ''}`;
    resultsSection.classList.add('active');
}

function copySingleCard(index) {
    const card = generatedCards[index];
    copyToClipboard(card.formatted);
    
    // Show visual feedback on the card
    const cardElement = document.querySelectorAll('.card-item')[index];
    cardElement.classList.add('copied');
    
    // Show toast notification
    showToast('Card copied to clipboard!');
    
    // Remove the copied class after animation
    setTimeout(() => {
        cardElement.classList.remove('copied');
    }, 1000);
}

function copyAllCards() {
    if (generatedCards.length === 0) {
        alert('No cards to copy. Generate cards first.');
        return;
    }

    const allCards = generatedCards.map(card => card.formatted).join('\n');
    copyToClipboard(allCards);
    
    // Show toast notification
    showToast('All cards copied to clipboard!');
    
    // Show feedback on button
    const copyBtn = document.getElementById('copyBtn');
    const originalHTML = copyBtn.innerHTML;
    copyBtn.innerHTML = '<span class="btn-icon">✓</span> Copied!';
    
    setTimeout(() => {
        copyBtn.innerHTML = originalHTML;
    }, 2000);
}

function clearAllCards() {
    generatedCards = [];
    displayCards([]);
}

function showToast(message) {
    const toast = document.getElementById('copyToast');
    const toastText = toast.querySelector('.toast-text');
    
    toastText.textContent = message;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 2000);
}

function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).catch(() => {
            fallbackCopy(text);
        });
    } else {
        fallbackCopy(text);
    }
}

function fallbackCopy(text) {
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
