import os
import requests
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from dhooks import Webhook
import time

def send_message_periodically(hook, message, interval, count, lock, stop_event):
    for _ in range(count):
        with lock:
            if stop_event.is_set():
                return
            hook.send(message)
            time.sleep(interval)

def nuker(webhook_url, message, interval, count, delete_after, stop_event):
    hook = Webhook(webhook_url)
    send_message_periodically(hook, message, interval, count, threading.Lock(), stop_event)
    if delete_after:
        hook.send("This webhook has forcefully been deleted :gorilla: :middle_finger: :gorilla:")
        x = requests.delete(webhook_url)
        print("Webhook deleted.")

def end():
    print("Successfully nuked webhook\n")
    print("Closing in 10 seconds...")
    time.sleep(10)
    os.system("exit")

def start_gui():
    class App:
        def __init__(self, master):
            self.master = master
            self.running = False
            self.stop_event = threading.Event()
            self.delete_after_var = tk.BooleanVar()
            self.create_widgets()

            icon_path = "Logo.ico"  
            master.iconbitmap(icon_path)

        def start_stop(self):
            if self.running:
                self.running = False
                self.stop_event.set()
                self.start_stop_button.config(text="Start")
            else:
                self.running = True
                self.stop_event.clear()
                self.start_stop_button.config(text="Stop")
                threading.Thread(target=self.execute_process).start()

        def execute_process(self):
            webhook_url = self.webhook_url_entry.get()
            message = self.message_entry.get()
            interval = 1 / self.interval_scale.get()
            count = self.count_scale.get()
            delete_after = self.delete_after_var.get()
            
            if webhook_url and message:
                nuker(webhook_url, message, interval, count, delete_after, self.stop_event)
                messagebox.showinfo("Success", "Webhook process completed successfully.")
                end()
                self.running = False
                self.stop_event.clear()
                self.start_stop_button.config(text="Start")
            else:
                messagebox.showwarning("Error", "Webhook URL and message are required!")
                self.running = False
                self.stop_event.clear()
                self.start_stop_button.config(text="Start")

        def create_widgets(self):
            
            title_label = tk.Label(self.master, text="""
 ▄█        ▄█     ▄████████  ▄██████▄  ███▄▄▄▄   
███       ███    ███    ███ ███    ███ ███▀▀▀██▄ 
███       ███▌   ███    █▀  ███    ███ ███   ███ 
███       ███▌   ███        ███    ███ ███   ███ 
███       ███▌ ▀███████████ ███    ███ ███   ███ 
███       ███           ███ ███    ███ ███   ███ 
███▌    ▄ ███     ▄█    ███ ███    ███ ███   ███ 
█████▄▄██ █▀    ▄████████▀   ▀██████▀   ▀█   █▀  
▀                                                
            """, font=("Courier", 10))
            title_label.grid(row=0, columnspan=2, padx=10, pady=10)

            tk.Label(self.master, text="Webhook URL:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
            tk.Label(self.master, text="Message:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
            tk.Label(self.master, text="Messages per Second:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
            tk.Label(self.master, text="Number of Messages:").grid(row=4, column=0, padx=10, pady=5, sticky="e")

            self.webhook_url_entry = tk.Entry(self.master, width=50)
            self.webhook_url_entry.grid(row=1, column=1, padx=10, pady=5)
            self.message_entry = tk.Entry(self.master, width=50)
            self.message_entry.grid(row=2, column=1, padx=10, pady=5)

            self.interval_scale = tk.Scale(self.master, from_=1, to=10, orient=tk.HORIZONTAL, length=200)
            self.interval_scale.grid(row=3, column=1, padx=10, pady=5)

            self.count_scale = tk.Scale(self.master, from_=1, to=1000, orient=tk.HORIZONTAL, length=200)
            self.count_scale.grid(row=4, column=1, padx=10, pady=5)

            self.delete_after_check = tk.Checkbutton(self.master, text="Delete Webhook After Sending", variable=self.delete_after_var)
            self.delete_after_check.grid(row=5, columnspan=2, padx=10, pady=5)

            self.start_stop_button = tk.Button(self.master, text="Start", command=self.start_stop, width=10)
            self.start_stop_button.grid(row=6, column=0, columnspan=2, padx=10, pady=20)

    root = tk.Tk()
    root.title("Lison | Webhook Spamer | By Doub")
    app = App(root)
    root.mainloop()

start_gui()
