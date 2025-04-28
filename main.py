import re
import tkinter as tk
import math
from tkinter import ttk
import json
from datetime import datetime

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Advanced Scientific Calculator")
        self.window.geometry("600x800")
        self.window.config(bg="#1e1e2e")
        self.window.resizable(True, True)
        self.window.minsize(500, 700)
        
        self.expression = ""
        self.memory = 0
        self.history = []
        self.is_dark_theme = True
        self.is_radians = True  # Default to radians mode
        
        self.setup_ui()
        self.setup_keyboard_bindings()
        
    def setup_ui(self):
        # Main container
        self.main_container = tk.Frame(self.window, bg="#1e1e2e")
        self.main_container.pack(expand=True, fill="both")
        
        # Top bar for mode buttons
        self.top_bar = tk.Frame(self.main_container, bg="#2d2d3a", height=50)
        self.top_bar.pack(fill="x", padx=20, pady=(20, 0))
        self.top_bar.pack_propagate(False)  # Prevent shrinking
        
        # Mode toggle buttons in top bar
        self.rad_btn = tk.Button(self.top_bar, text="RAD", font=("Segoe UI", 16, "bold"),
                               command=self.toggle_angle_mode, bg="#3b3b4d", fg="white",
                               relief="flat", bd=0, width=8, height=1)
        self.rad_btn.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.theme_btn = tk.Button(self.top_bar, text="🌓", font=("Segoe UI", 16),
                                 command=self.toggle_theme, bg="#3b3b4d", fg="white",
                                 relief="flat", bd=0, width=4, height=1)
        self.theme_btn.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Main display
        self.equation = tk.StringVar()
        self.entry = tk.Entry(self.main_container, textvariable=self.equation, font=("Segoe UI", 24),
                            bg="#2d2d3a", fg="#ffffff", bd=0, justify='right', insertbackground='white')
        self.entry.pack(fill='x', padx=20, pady=10, ipady=15)
        
        # History display
        self.history_frame = tk.Frame(self.main_container, bg="#1e1e2e", height=100)
        self.history_frame.pack(fill='x', padx=20, pady=5)
        self.history_text = tk.Text(self.history_frame, height=3, font=("Segoe UI", 12),
                                  bg="#2d2d3a", fg="#ffffff", bd=0)
        self.history_text.pack(fill='both', expand=True)
        
        # Button frame
        self.frame = tk.Frame(self.main_container, bg="#1e1e2e")
        self.frame.pack(expand=True, fill="both", padx=20, pady=10)
        
        # Configure grid
        for i in range(9):
            self.frame.rowconfigure(i, weight=1)
        for j in range(5):
            self.frame.columnconfigure(j, weight=1)
            
        # Memory buttons
        memory_buttons = [
            ('MC', 0, 0, self.memory_clear, "#e74c3c"),
            ('MR', 0, 1, self.memory_recall, "#f39c12"),
            ('M+', 0, 2, self.memory_add, "#27ae60"),
            ('M-', 0, 3, self.memory_subtract, "#27ae60"),
            ('MS', 0, 4, self.memory_store, "#27ae60")
        ]
        
        for btn in memory_buttons:
            self.create_button(*btn)
            
        # Scientific functions - Row 1
        scientific_buttons1 = [
            ('sin', 1, 0, lambda: self.scientific_function('sin'), "#3b3b4d"),
            ('cos', 1, 1, lambda: self.scientific_function('cos'), "#3b3b4d"),
            ('tan', 1, 2, lambda: self.scientific_function('tan'), "#3b3b4d"),
            ('log', 1, 3, lambda: self.scientific_function('log'), "#3b3b4d"),
            ('ln', 1, 4, lambda: self.scientific_function('ln'), "#3b3b4d")
        ]
        
        for btn in scientific_buttons1:
            self.create_button(*btn)
            
        # Scientific functions - Row 2
        scientific_buttons2 = [
            ('asin', 2, 0, lambda: self.scientific_function('asin'), "#3b3b4d"),
            ('acos', 2, 1, lambda: self.scientific_function('acos'), "#3b3b4d"),
            ('atan', 2, 2, lambda: self.scientific_function('atan'), "#3b3b4d"),
            ('x²', 2, 3, lambda: self.scientific_function('square'), "#3b3b4d"),
            ('√', 2, 4, lambda: self.scientific_function('sqrt'), "#3b3b4d")
        ]
        
        for btn in scientific_buttons2:
            self.create_button(*btn)
            
        # Constants and special functions
        constant_buttons = [
            ('π', 3, 0, lambda: self.press(str(math.pi)), "#3b3b4d"),
            ('e', 3, 1, lambda: self.press(str(math.e)), "#3b3b4d"),
            ('x!', 3, 2, lambda: self.scientific_function('factorial'), "#3b3b4d"),
            ('1/x', 3, 3, lambda: self.scientific_function('reciprocal'), "#3b3b4d"),
            ('|x|', 3, 4, lambda: self.scientific_function('abs'), "#3b3b4d")
        ]
        
        for btn in constant_buttons:
            self.create_button(*btn)
            
        # Regular calculator buttons
        regular_buttons = [
            ('C', 4, 0, self.clear, "#e74c3c"), ('DEL', 4, 1, self.delete, "#f39c12"),
            ('(', 4, 2), (')', 4, 3), ('^', 4, 4),
            ('7', 5, 0), ('8', 5, 1), ('9', 5, 2), ('/', 5, 3), ('mod', 5, 4),
            ('4', 6, 0), ('5', 6, 1), ('6', 6, 2), ('*', 6, 3), ('exp', 6, 4),
            ('1', 7, 0), ('2', 7, 1), ('3', 7, 2), ('-', 7, 3), ('10^x', 7, 4),
            ('0', 8, 0), ('.', 8, 1), ('%', 8, 2), ('+', 8, 3), ('=', 8, 4, self.equalpress, "#27ae60")
        ]
        
        for btn in regular_buttons:
            self.create_button(*btn)
            
    def create_button(self, text, row, col, command=None, color="#3b3b4d"):
        btn = tk.Button(self.frame, text=text, font=("Segoe UI", 18),
                       bg=color, fg="white", activebackground="#5c5c7a",
                       activeforeground="white", relief="flat", bd=0,
                       padx=20, pady=20,
                       command=command or (lambda t=text: self.press(t)))
        btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
        
    def toggle_angle_mode(self):
        self.is_radians = not self.is_radians
        self.rad_btn.config(text="RAD" if self.is_radians else "DEG")
        
    def scientific_function(self, func):
        try:
            current = float(self.expression or "0")
            if func == 'sin':
                result = math.sin(current if self.is_radians else math.radians(current))
            elif func == 'cos':
                result = math.cos(current if self.is_radians else math.radians(current))
            elif func == 'tan':
                result = math.tan(current if self.is_radians else math.radians(current))
            elif func == 'asin':
                result = math.asin(current)
                if not self.is_radians:
                    result = math.degrees(result)
            elif func == 'acos':
                result = math.acos(current)
                if not self.is_radians:
                    result = math.degrees(result)
            elif func == 'atan':
                result = math.atan(current)
                if not self.is_radians:
                    result = math.degrees(result)
            elif func == 'log':
                result = math.log10(current)
            elif func == 'ln':
                result = math.log(current)
            elif func == 'square':
                result = current ** 2
            elif func == 'sqrt':
                result = math.sqrt(current)
            elif func == 'factorial':
                result = math.factorial(int(current))
            elif func == 'reciprocal':
                result = 1 / current
            elif func == 'abs':
                result = abs(current)
                
            self.expression = str(result)
            self.equation.set(self.expression)
            self.add_to_history(f"{func}({current}) = {result}")
        except:
            self.equation.set("Error")
            self.expression = ""
            
    def press(self, num):
        self.expression += str(num)
        self.equation.set(self.expression)
        
    def equalpress(self):
        try:
            # Replace special characters and functions
            expr = self.expression.replace('^', '**')
            expr = expr.replace('π', str(math.pi))
            expr = expr.replace('e', str(math.e))
            expr = expr.replace('mod', '%')
            
            # Handle implicit multiplication
            expr = re.sub(r'(\d)(\()', r'\1*(', expr)
            
            result = str(eval(expr))
            self.equation.set(result)
            self.expression = result
            
            # Add to history
            self.add_to_history(f"{self.expression} = {result}")
            
        except Exception as e:
            self.equation.set("Error")
            self.expression = ""
            
    def clear(self):
        self.expression = ""
        self.equation.set("")
        
    def delete(self):
        self.expression = self.expression[:-1]
        self.equation.set(self.expression)
        
    def memory_clear(self):
        self.memory = 0
        
    def memory_recall(self):
        self.expression = str(self.memory)
        self.equation.set(self.expression)
        
    def memory_add(self):
        try:
            self.memory += float(self.expression or "0")
        except:
            pass
            
    def memory_subtract(self):
        try:
            self.memory -= float(self.expression or "0")
        except:
            pass
            
    def memory_store(self):
        try:
            self.memory = float(self.expression or "0")
        except:
            pass
            
    def add_to_history(self, calculation):
        self.history.append(calculation)
        if len(self.history) > 3:
            self.history.pop(0)
        self.history_text.delete(1.0, tk.END)
        self.history_text.insert(tk.END, "\n".join(self.history))
        
    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        bg_color = "#1e1e2e" if self.is_dark_theme else "#ffffff"
        fg_color = "#ffffff" if self.is_dark_theme else "#000000"
        entry_bg = "#2d2d3a" if self.is_dark_theme else "#f0f0f0"
        
        self.window.config(bg=bg_color)
        self.main_container.config(bg=bg_color)
        self.frame.config(bg=bg_color)
        self.entry.config(bg=entry_bg, fg=fg_color)
        self.history_text.config(bg=entry_bg, fg=fg_color)
        
    def setup_keyboard_bindings(self):
        self.window.bind('<Return>', lambda e: self.equalpress())
        self.window.bind('<BackSpace>', lambda e: self.delete())
        self.window.bind('<Escape>', lambda e: self.clear())
        for i in range(10):
            self.window.bind(str(i), lambda e, num=i: self.press(num))
        self.window.bind('+', lambda e: self.press('+'))
        self.window.bind('-', lambda e: self.press('-'))
        self.window.bind('*', lambda e: self.press('*'))
        self.window.bind('/', lambda e: self.press('/'))
        self.window.bind('.', lambda e: self.press('.'))
        self.window.bind('(', lambda e: self.press('('))
        self.window.bind(')', lambda e: self.press(')'))
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calc = Calculator()
    calc.run()