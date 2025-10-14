from flask import Flask, render_template, request, jsonify
import random
import threading
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def luhn_check(number):
    """Luhn algorithm to validate credit card numbers"""
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10 == 0

def calculate_luhn_check_digit(number):
    """Calculate the Luhn check digit for a number"""
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    total = sum(odd_digits)
    for d in even_digits:
        total += sum(digits_of(d * 2))
    return (10 - (total % 10)) % 10

def generate_valid_card_number(bin_number):
    """Generate a credit card number that passes Luhn check"""
    remaining_length = 15 - len(bin_number)
    middle_digits = ''.join(random.choice('0123456789') for _ in range(remaining_length - 1))
    partial_number = bin_number + middle_digits
    check_digit = calculate_luhn_check_digit(partial_number)
    full_number = partial_number + str(check_digit)
    return full_number

def get_card_type(bin_number):
    """Determine card type based on BIN"""
    if bin_number.startswith('4'):
        return "Visa"
    elif bin_number.startswith('5'):
        return "MasterCard"
    elif bin_number.startswith('34') or bin_number.startswith('37'):
        return "Amex"
    elif bin_number.startswith('6'):
        return "Discover"
    else:
        return "Unknown"

def format_card_number(card_number):
    """Format card number with spaces for better readability"""
    return ' '.join([card_number[i:i+4] for i in range(0, len(card_number), 4)])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_cards():
    try:
        data = request.get_json()
        bin_number = data.get('bin', '').strip()
        amount = int(data.get('amount', 10))
        
        # Validate inputs
        if not bin_number.isdigit() or len(bin_number) != 6:
            return jsonify({'error': 'BIN must be exactly 6 digits'}), 400
        
        if amount < 1 or amount > 50:
            return jsonify({'error': 'Amount must be between 1 and 50'}), 400
        
        # Generate cards
        generated_cards = []
        for i in range(amount):
            card_number = generate_valid_card_number(bin_number)
            exp_month = random.randint(1, 12)
            exp_year = random.randint(24, 28)
            exp_date = f"{exp_month:02d}/{exp_year}"
            cvv = ''.join(random.choice('0123456789') for _ in range(3))
            card_type = get_card_type(bin_number)
            
            card_info = {
                'number': card_number,
                'formatted_number': format_card_number(card_number),
                'expiry': exp_date,
                'cvv': cvv,
                'type': card_type,
                'index': i + 1
            }
            generated_cards.append(card_info)
        
        return jsonify({'cards': generated_cards})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
