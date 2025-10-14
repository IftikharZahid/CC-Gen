import tkinter as tk
from tkinter import ttk, messagebox
import threading
import random
import time
import platform

class CreditCardGeneratorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Credit Card Generator")
        
        # Detect screen size for responsiveness
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()
        self.is_mobile = self.screen_width < 768
        
        self.setup_responsive_geometry()
        self.master.configure(bg='#f0f2f5')
        
        # Variables
        self.card_data = []
        self.selected_index = None
        self.is_generating = False
        
        # Create main container with scrollbar
        self.setup_scrollable_main()
        self.setup_ui()
        
    def setup_responsive_geometry(self):
        """Set responsive window size based on screen"""
        if self.is_mobile:
            # Mobile layout
            self.master.geometry("400x600")
            self.font_large = ('Arial', 14)
            self.font_medium = ('Arial', 12)
            self.font_small = ('Arial', 10)
            self.padding = 10
        else:
            # Desktop layout
            self.master.geometry("900x700")
            self.font_large = ('Arial', 12)
            self.font_medium = ('Arial', 10)
            self.font_small = ('Arial', 9)
            self.padding = 20
            
        # Center window
        window_width = 900 if not self.is_mobile else 400
        window_height = 700 if not self.is_mobile else 600
        x = (self.screen_width - window_width) // 2
        y = (self.screen_height - window_height) // 2
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
    def setup_scrollable_main(self):
        """Create scrollable main container"""
        # Create main frame with scrollbar
        self.main_canvas = tk.Canvas(self.master, bg='#f0f2f5', highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.master, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_main = tk.Frame(self.main_canvas, bg='#f0f2f5')
        
        self.scrollable_main.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        
        self.main_canvas.create_window((0, 0), window=self.scrollable_main, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack scrollable area
        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel to canvas
        self.main_canvas.bind("<MouseWheel>", self._on_main_mousewheel)
        self.scrollable_main.bind("<MouseWheel>", self._on_main_mousewheel)
        
    def _on_main_mousewheel(self, event):
        """Handle mouse wheel scrolling for main canvas"""
        self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def setup_ui(self):
        """Setup responsive UI components"""
        # Header
        header_frame = tk.Frame(self.scrollable_main, bg='#ffffff', relief='flat', 
                               highlightbackground='#ddd', highlightthickness=1)
        header_frame.pack(fill='x', padx=self.padding, pady=(self.padding, self.padding//2))
        
        title_font = ('Arial', 16, 'bold') if self.is_mobile else ('Arial', 20, 'bold')
        subtitle_font = ('Arial', 9) if self.is_mobile else ('Arial', 11)
        
        tk.Label(header_frame, text="💳 Credit Card Generator", 
                font=title_font, bg='#ffffff', fg='#2c3e50').pack(pady=15)
        
        tk.Label(header_frame, text="Generate valid test credit card numbers for development", 
                font=subtitle_font, bg='#ffffff', fg='#7f8c8d').pack(pady=(0, 15))
        
        # Input Section
        input_frame = tk.Frame(self.scrollable_main, bg='#ffffff', relief='flat', 
                              highlightbackground='#ddd', highlightthickness=1)
        input_frame.pack(fill='x', padx=self.padding, pady=self.padding//2)
        
        self.setup_input_section(input_frame)
        
        # Progress Section
        progress_frame = tk.Frame(self.scrollable_main, bg='#f0f2f5')
        progress_frame.pack(fill='x', padx=self.padding, pady=self.padding//2)
        
        self.setup_progress_section(progress_frame)
        
        # Results Section
        results_frame = tk.Frame(self.scrollable_main, bg='#ffffff', relief='flat', 
                                highlightbackground='#ddd', highlightthickness=1)
        results_frame.pack(fill='both', expand=True, padx=self.padding, pady=self.padding//2)
        
        self.setup_results_section(results_frame)
        
        # Footer
        footer_frame = tk.Frame(self.scrollable_main, bg='#f0f2f5')
        footer_frame.pack(fill='x', padx=self.padding, pady=(self.padding//2, self.padding))
        
        self.setup_footer(footer_frame)
        
    def setup_input_section(self, parent):
        """Setup responsive input section"""
        input_content = tk.Frame(parent, bg='#ffffff', padx=self.padding, pady=self.padding)
        input_content.pack(fill='x')
        
        if self.is_mobile:
            # Stacked layout for mobile
            self.setup_mobile_input(input_content)
        else:
            # Side-by-side layout for desktop
            self.setup_desktop_input(input_content)
            
        # Generate Button
        btn_font = ('Arial', 12, 'bold') if self.is_mobile else ('Arial', 12, 'bold')
        self.generate_btn = tk.Button(input_content, text="🚀 Generate Credit Cards", 
                                     font=btn_font, bg='#3498db', fg='white',
                                     relief='flat', bd=0, height=2, cursor='hand2',
                                     command=self.start_generation)
        self.generate_btn.pack(fill='x', pady=(15, 0))
        
    def setup_mobile_input(self, parent):
        """Mobile input layout"""
        # BIN Input
        bin_frame = tk.Frame(parent, bg='#ffffff')
        bin_frame.pack(fill='x', pady=8)
        
        tk.Label(bin_frame, text="BIN (First 6 digits)", font=self.font_medium, 
                bg='#ffffff', fg='#2c3e50').pack(anchor='w')
        
        self.bin_entry = tk.Entry(bin_frame, font=self.font_medium, relief='solid', bd=1)
        self.bin_entry.pack(fill='x', pady=(5, 0))
        self.bin_entry.insert(0, "411111")
        
        # Amount Input
        amount_frame = tk.Frame(parent, bg='#ffffff')
        amount_frame.pack(fill='x', pady=8)
        
        tk.Label(amount_frame, text="Number of Cards (1-50)", font=self.font_medium, 
                bg='#ffffff', fg='#2c3e50').pack(anchor='w')
        
        self.amount_entry = tk.Entry(amount_frame, font=self.font_medium, relief='solid', bd=1)
        self.amount_entry.pack(fill='x', pady=(5, 0))
        self.amount_entry.insert(0, "10")
        
    def setup_desktop_input(self, parent):
        """Desktop input layout"""
        input_grid = tk.Frame(parent, bg='#ffffff')
        input_grid.pack(fill='x')
        
        # BIN Input
        bin_frame = tk.Frame(input_grid, bg='#ffffff')
        bin_frame.grid(row=0, column=0, sticky='ew', padx=(0, 10))
        
        tk.Label(bin_frame, text="BIN (First 6 digits)", font=self.font_medium, 
                bg='#ffffff', fg='#2c3e50').pack(anchor='w')
        tk.Label(bin_frame, text="Enter the first 6 digits", 
                font=self.font_small, bg='#ffffff', fg='#7f8c8d').pack(anchor='w', pady=(0, 5))
        
        self.bin_entry = tk.Entry(bin_frame, font=self.font_medium, relief='solid', bd=1)
        self.bin_entry.pack(fill='x', pady=(0, 10))
        self.bin_entry.insert(0, "411111")
        
        # Amount Input
        amount_frame = tk.Frame(input_grid, bg='#ffffff')
        amount_frame.grid(row=0, column=1, sticky='ew', padx=(10, 0))
        
        tk.Label(amount_frame, text="Number of Cards", font=self.font_medium, 
                bg='#ffffff', fg='#2c3e50').pack(anchor='w')
        tk.Label(amount_frame, text="How many to generate (1-50)", 
                font=self.font_small, bg='#ffffff', fg='#7f8c8d').pack(anchor='w', pady=(0, 5))
        
        self.amount_entry = tk.Entry(amount_frame, font=self.font_medium, relief='solid', bd=1)
        self.amount_entry.pack(fill='x', pady=(0, 10))
        self.amount_entry.insert(0, "10")
        
        input_grid.columnconfigure(0, weight=1)
        input_grid.columnconfigure(1, weight=1)
        
    def setup_progress_section(self, parent):
        """Setup progress section"""
        self.progress = ttk.Progressbar(parent, mode='determinate', length=100)
        self.progress.pack(fill='x')
        
        self.status_label = tk.Label(parent, text="Ready to generate", 
                                   font=self.font_small, bg='#f0f2f5', fg='#27ae60')
        self.status_label.pack(anchor='w', pady=(5, 0))
        
    def setup_results_section(self, parent):
        """Setup results section with cards display"""
        # Results Header
        results_header = tk.Frame(parent, bg='#f8f9fa', padx=self.padding, pady=12)
        results_header.pack(fill='x')
        
        title_font = ('Arial', 12, 'bold') if self.is_mobile else ('Arial', 14, 'bold')
        tk.Label(results_header, text="Generated Cards", font=title_font, 
                bg='#f8f9fa', fg='#2c3e50').pack(side='left')
        
        # Action Buttons
        self.setup_action_buttons(results_header)
        
        # Cards Display Area
        display_frame = tk.Frame(parent, bg='#ffffff')
        display_frame.pack(fill='both', expand=True, padx=self.padding, pady=self.padding)
        
        self.setup_cards_display(display_frame)
        
    def setup_action_buttons(self, parent):
        """Setup responsive action buttons"""
        btn_frame = tk.Frame(parent, bg='#f8f9fa')
        btn_frame.pack(side='right')
        
        btn_font = self.font_small
        btn_padding = 3 if self.is_mobile else 5
        
        self.copy_btn = tk.Button(btn_frame, text="📋 Copy Selected", 
                                 font=btn_font, bg='#27ae60', fg='white',
                                 relief='flat', cursor='hand2', command=self.copy_selected)
        self.copy_btn.pack(side='left', padx=btn_padding)
        
        self.copy_all_btn = tk.Button(btn_frame, text="📜 Copy All", 
                                     font=btn_font, bg='#3498db', fg='white',
                                     relief='flat', cursor='hand2', command=self.copy_all)
        self.copy_all_btn.pack(side='left', padx=btn_padding)
        
        self.clear_btn = tk.Button(btn_frame, text="🗑️ Clear", 
                                  font=btn_font, bg='#e74c3c', fg='white',
                                  relief='flat', cursor='hand2', command=self.clear_results)
        self.clear_btn.pack(side='left', padx=btn_padding)
        
    def setup_cards_display(self, parent):
        """Setup cards display area"""
        # Create Text widget with scrollbar
        text_container = tk.Frame(parent, bg='#ffffff')
        text_container.pack(fill='both', expand=True)
        
        # Text widget for displaying cards
        text_font = ('Consolas', 9) if self.is_mobile else ('Consolas', 10)
        self.cards_text = tk.Text(text_container, wrap=tk.WORD, font=text_font, 
                                 bg='#2c3e50', fg='#ecf0f1', selectbackground='#3498db',
                                 relief='flat', bd=1, padx=10, pady=10, spacing1=2,
                                 cursor='arrow')
        
        # Scrollbars
        scrollbar_y = ttk.Scrollbar(text_container, orient='vertical', command=self.cards_text.yview)
        scrollbar_x = ttk.Scrollbar(text_container, orient='horizontal', command=self.cards_text.xview)
        
        self.cards_text.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # Pack widgets
        self.cards_text.pack(side='left', fill='both', expand=True)
        scrollbar_y.pack(side='right', fill='y')
        scrollbar_x.pack(side='bottom', fill='x')
        
        # Configure text tags for colors
        self.setup_text_tags()
        
        # Make text read-only but selectable
        self.cards_text.config(state=tk.DISABLED)
        
    def setup_text_tags(self):
        """Configure text colors and styles"""
        self.cards_text.tag_configure('header', foreground='#f39c12', font=('Consolas', 10, 'bold'))
        self.cards_text.tag_configure('number', foreground='#3498db', font=('Consolas', 10, 'bold'))
        self.cards_text.tag_configure('expiry', foreground='#27ae60', font=('Consolas', 10))
        self.cards_text.tag_configure('cvv', foreground='#e74c3c', font=('Consolas', 10, 'bold'))
        self.cards_text.tag_configure('type', foreground='#9b59b6', font=('Consolas', 10))
        self.cards_text.tag_configure('separator', foreground='#7f8c8d', font=('Consolas', 10))
        self.cards_text.tag_configure('index', foreground='#f39c12', font=('Consolas', 10, 'bold'))
        
    def setup_footer(self, parent):
        """Setup footer section"""
        warning_font = ('Arial', 8) if self.is_mobile else ('Arial', 9)
        
        tk.Label(parent, text="⚠️ For testing and development purposes only", 
                font=warning_font, bg='#f0f2f5', fg='#e74c3c').pack()
        
        tk.Label(parent, text="Generated cards are not valid for real transactions", 
                font=warning_font, bg='#f0f2f5', fg='#7f8c8d').pack(pady=(2, 0))
        
    # Core functionality methods (same as before but optimized)
    def luhn_check(self, number):
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
    
    def calculate_luhn_check_digit(self, number):
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
    
    def generate_valid_card_number(self, bin_number):
        """Generate a credit card number that passes Luhn check"""
        remaining_length = 15 - len(bin_number)
        middle_digits = ''.join(random.choice('0123456789') for _ in range(remaining_length - 1))
        partial_number = bin_number + middle_digits
        check_digit = self.calculate_luhn_check_digit(partial_number)
        full_number = partial_number + str(check_digit)
        return full_number
    
    def get_card_type(self, bin_number):
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
    
    def format_card_number(self, card_number):
        """Format card number with spaces for better readability"""
        return ' '.join([card_number[i:i+4] for i in range(0, len(card_number), 4)])
    
    def validate_inputs(self):
        """Validate user inputs"""
        bin_number = self.bin_entry.get().strip()
        amount_str = self.amount_entry.get().strip()
        
        if not bin_number.isdigit():
            return False, "BIN must contain only digits"
        if len(bin_number) != 6:
            return False, "BIN must be exactly 6 digits"
        
        try:
            amount = int(amount_str)
            if amount < 1:
                return False, "Amount must be at least 1"
            if amount > 50:
                return False, "Amount must be 50 or less"
        except ValueError:
            return False, "Please enter a valid number for amount"
        
        return True, ""
    
    def start_generation(self):
        """Start the credit card generation process"""
        if self.is_generating:
            return
            
        is_valid, error_msg = self.validate_inputs()
        if not is_valid:
            messagebox.showerror("Input Error", error_msg)
            return
        
        self.clear_results()
        
        bin_number = self.bin_entry.get().strip()
        amount = int(self.amount_entry.get().strip())
        
        self.is_generating = True
        self.generate_btn.config(state='disabled', text='⏳ Generating...', bg='#95a5a6')
        self.progress['value'] = 0
        self.status_label.config(text=f"Starting generation of {amount} cards...", fg='#f39c12')
        
        thread = threading.Thread(target=self.generate_cards_thread, args=(bin_number, amount))
        thread.daemon = True
        thread.start()
    
    def generate_cards_thread(self, bin_number, amount):
        """Generate cards in a separate thread"""
        try:
            generated_cards = []
            
            for i in range(amount):
                card_number = self.generate_valid_card_number(bin_number)
                exp_month = random.randint(1, 12)
                exp_year = random.randint(24, 28)
                exp_date = f"{exp_month:02d}/{exp_year}"
                cvv = ''.join(random.choice('0123456789') for _ in range(3))
                card_type = self.get_card_type(bin_number)
                
                card_info = {
                    'number': card_number,
                    'formatted_number': self.format_card_number(card_number),
                    'expiry': exp_date,
                    'cvv': cvv,
                    'type': card_type,
                    'index': i + 1
                }
                generated_cards.append(card_info)
                
                progress = (i + 1) / amount * 100
                self.master.after(0, lambda p=progress, idx=i: self.update_progress(p, idx + 1))
                time.sleep(0.02)  # Shorter delay for faster generation
            
            self.master.after(0, lambda: self.display_results(generated_cards))
            
        except Exception as e:
            self.master.after(0, lambda: self.generation_failed(str(e)))
    
    def update_progress(self, progress, current):
        """Update progress bar and status"""
        self.progress['value'] = progress
        self.status_label.config(text=f"Generating card {current}... ({progress:.0f}%)", fg='#f39c12')
    
    def display_results(self, cards):
        """Display generated cards in the text widget with colors"""
        self.is_generating = False
        self.generate_btn.config(state='normal', text='🚀 Generate Credit Cards', bg='#3498db')
        self.progress['value'] = 100
        
        # Enable text widget for writing
        self.cards_text.config(state=tk.NORMAL)
        self.cards_text.delete(1.0, tk.END)
        
        # Add header
        self.cards_text.insert(tk.END, "Generated Credit Cards:\n", 'header')
        self.cards_text.insert(tk.END, "=" * 50 + "\n\n", 'header')
        
        # Display each card with colorful formatting
        for card in cards:
            # Store card data
            self.card_data.append(card)
            
            # Insert card with colors
            self.cards_text.insert(tk.END, f"#{card['index']:02d} ", 'index')
            self.cards_text.insert(tk.END, "• ", 'separator')
            self.cards_text.insert(tk.END, f"{card['formatted_number']}", 'number')
            self.cards_text.insert(tk.END, " • ", 'separator')
            self.cards_text.insert(tk.END, f"{card['expiry']}", 'expiry')
            self.cards_text.insert(tk.END, " • ", 'separator')
            self.cards_text.insert(tk.END, f"{card['cvv']}", 'cvv')
            self.cards_text.insert(tk.END, " • ", 'separator')
            self.cards_text.insert(tk.END, f"{card['type']}", 'type')
            self.cards_text.insert(tk.END, "\n")
        
        # Add footer
        self.cards_text.insert(tk.END, f"\nTotal: {len(cards)} cards generated\n", 'header')
        self.cards_text.insert(tk.END, "Click and drag to select, then Ctrl+C to copy", 'separator')
        
        # Make text read-only but selectable
        self.cards_text.config(state=tk.DISABLED)
        
        self.status_label.config(text=f"✅ Successfully generated {len(cards)} credit cards!", fg='#27ae60')
        
        # Scroll to top
        self.cards_text.see(1.0)
    
    def generation_failed(self, error_msg):
        """Handle generation failure"""
        self.is_generating = False
        self.generate_btn.config(state='normal', text='🚀 Generate Credit Cards', bg='#3498db')
        self.progress['value'] = 0
        self.status_label.config(text=f"❌ Generation failed", fg='#e74c3c')
        messagebox.showerror("Generation Error", f"Failed to generate cards:\n{error_msg}")
    
    def copy_selected(self):
        """Copy selected text from cards display"""
        try:
            selected_text = self.cards_text.get(tk.SEL_FIRST, tk.SEL_LAST)
            if selected_text.strip():
                self.master.clipboard_clear()
                self.master.clipboard_append(selected_text.strip())
                self.status_label.config(text="✅ Selected text copied to clipboard!", fg='#27ae60')
                return
        except:
            pass
        
        # If no text selected, copy all
        self.copy_all()
    
    def copy_all(self):
        """Copy all cards to clipboard"""
        if not self.card_data:
            messagebox.showwarning("No Cards", "No cards generated yet.")
            return
        
        all_cards = []
        for card_info in self.card_data:
            card_text = f"{card_info['number']}|{card_info['expiry']}|{card_info['cvv']}"
            all_cards.append(card_text)
        
        self.master.clipboard_clear()
        self.master.clipboard_append('\n'.join(all_cards))
        self.status_label.config(text=f"✅ All {len(all_cards)} cards copied to clipboard!", fg='#27ae60')
    
    def clear_results(self):
        """Clear all generated results"""
        self.cards_text.config(state=tk.NORMAL)
        self.cards_text.delete(1.0, tk.END)
        self.cards_text.config(state=tk.DISABLED)
        self.card_data = []
        self.selected_index = None
        self.progress['value'] = 0
        self.status_label.config(text="Ready to generate", fg='#27ae60')

def main():
    root = tk.Tk()
    
    # Set minimum window size
    root.minsize(380, 500)
    
    # Create the application
    app = CreditCardGeneratorGUI(root)
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
