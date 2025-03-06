import pyautogui
import time
import random
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import nltk
from nltk.corpus import wordnet
from typing import List

# Configure PyAutoGUI failsafe
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

nltk.download('wordnet', quiet=True)

class TypingManager:
    def __init__(self):
        self.typed_text: List[str] = []
        self.paused = False

    def random_typing_delay(self) -> float:
        return random.uniform(0.1, 0.3)

    def safe_type(self, text: str, interval: float = None):
        try:
            if interval is None:
                interval = self.random_typing_delay()
            pyautogui.typewrite(text, interval=interval)
            time.sleep(0.1)  # Additional delay between words
        except pyautogui.FailSafeException:
            raise Exception("Failsafe triggered during typing")
    
    def type_text_sequential(self, text: str, long_pause_after_period: float):
        words = text.split()
        for word in words:
            while self.paused:
                time.sleep(0.1)  # Wait while paused
            self.typed_text.append(word)
            self.safe_type(word + " ")
            
            if "." in word:
                time.sleep(long_pause_after_period)

    def toggle_pause(self):
        self.paused = not self.paused

typing_manager = TypingManager()

def start_typing(file_path: str, delay_speed: float, misspell_chance: float, 
                 long_pause_after_period: float, paragraph_delay: float, button: tk.Button):
    button.config(state=tk.DISABLED)
    
    def typing_task():
        try:
            time.sleep(0.5)  # Short delay before starting
            time.sleep(3)  # Initial delay
            
            with open(file_path, 'r') as f:
                for line in f:
                    if line.strip() == "":
                        time.sleep(paragraph_delay)
                        continue
                     # Use the latest slider values during typing
            
                    typing_manager.type_text_sequential(line.strip(), long_pause_after_period)
                    time.sleep(delay_speed)
            
            messagebox.showinfo("Success", "Typing complete!")
        except pyautogui.FailSafeException:
            messagebox.showerror("Error", "Failsafe triggered - typing aborted")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            button.config(state=tk.NORMAL)
    
    threading.Thread(target=typing_task, daemon=True).start()

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        print("Debug - Slider Values:")
        print(f"Delay Speed: {delay_speed_var.get()}")
        print(f"Misspell Chance: {misspell_chance_var.get()}")
        print(f"Long Pause After Period: {long_pause_var.get()}")
        print(f"Paragraph Delay: {paragraph_delay_var.get()}")
        threading.Thread(target=start_typing, args=(
            file_path,
            delay_speed_var.get(),
            misspell_chance_var.get(),
            long_pause_var.get(),
            paragraph_delay_var.get(),
            select_button
        ), daemon=True).start()

def toggle_pause():
    typing_manager.toggle_pause()
    pause_button.config(text="Resume" if typing_manager.paused else "Pause")

# GUI Setup
root = tk.Tk()
root.title("Auto Typer")
root.geometry("400x400")

label = tk.Label(root, text="Select a text file to type:")
label.pack(pady=10)

select_button = tk.Button(root, text="Select File", command=select_file)
select_button.pack(pady=10)

pause_button = tk.Button(root, text="Pause", command=toggle_pause)
pause_button.pack(pady=10)

# Sliders for settings
delay_speed_var = tk.DoubleVar(value=0.05)
misspell_chance_var = tk.DoubleVar(value=0.1)
long_pause_var = tk.DoubleVar(value=1.0)
paragraph_delay_var = tk.DoubleVar(value=2.0)

tk.Label(root, text="Typing Speed").pack()
tk.Scale(root, from_=0.01, to=1.0, resolution=0.01, orient='horizontal', variable=delay_speed_var).pack()

tk.Label(root, text="Misspell Chance").pack()
tk.Scale(root, from_=0.0, to=0.5, resolution=0.01, orient='horizontal', variable=misspell_chance_var).pack()

tk.Label(root, text="Pause After Period").pack()
tk.Scale(root, from_=0.5, to=3.0, resolution=0.1, orient='horizontal', variable=long_pause_var).pack()

tk.Label(root, text="Paragraph Delay").pack()
tk.Scale(root, from_=0.5, to=5.0, resolution=0.5, orient='horizontal', variable=paragraph_delay_var).pack()

exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.pack(pady=10)

root.mainloop()
