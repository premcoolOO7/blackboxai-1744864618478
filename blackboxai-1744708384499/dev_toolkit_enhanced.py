import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import sqlite3
import uuid
import hashlib
import json
import pyperclip
import time
import requests
from datetime import datetime
import re
from PyPDF2 import PdfReader
from gtts import gTTS
import os

class DevToolkit:
    def __init__(self, root):
        self.root = root
        self.root.title("Developer Productivity Suite")
        self.root.geometry("1200x800")
        
        self.create_database()
        self.create_ui()
        
    def create_database(self):
        self.conn = sqlite3.connect('dev_toolkit.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS snippets
                         (id INTEGER PRIMARY KEY, title TEXT, code TEXT, tags TEXT, created_at TIMESTAMP)''')
        self.conn.commit()

    def create_ui(self):
        notebook = ttk.Notebook(self.root)
        
        # Snippet Manager Tab
        snippet_frame = ttk.Frame(notebook)
        self.create_snippet_ui(snippet_frame)
        
        # API Tester Tab
        api_frame = ttk.Frame(notebook)
        self.create_api_tester_ui(api_frame)
        
        # Regex Tester Tab
        regex_frame = ttk.Frame(notebook)
        self.create_regex_tester_ui(regex_frame)
        
        # Code Utilities Tab
        utils_frame = ttk.Frame(notebook)
        self.create_utils_ui(utils_frame)

        # Word Manipulator Tab
        word_manipulator_frame = ttk.Frame(notebook)
        self.create_word_manipulator_ui(word_manipulator_frame)
        
        notebook.add(snippet_frame, text="Code Snippets")
        notebook.add(api_frame, text="API Tester")
        notebook.add(regex_frame, text="Regex Tester")
        notebook.add(utils_frame, text="Code Utilities")
        notebook.add(word_manipulator_frame, text="Word Manipulator")
        notebook.pack(expand=1, fill="both")

    def create_word_manipulator_ui(self, parent):
        ttk.Label(parent, text="Upload PDF:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Button(parent, text="Browse", command=self.upload_pdf).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.pdf_text_area = scrolledtext.ScrolledText(parent, width=100, height=20)
        self.pdf_text_area.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        
        ttk.Button(parent, text="Narrate", command=self.narrate_pdf).grid(row=2, column=0, pady=10, sticky="ew")

    def upload_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.extract_text_from_pdf(file_path)

    def extract_text_from_pdf(self, file_path):
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        self.pdf_text_area.delete(1.0, tk.END)
        self.pdf_text_area.insert(tk.END, text)

    def narrate_pdf(self):
        text = self.pdf_text_area.get("1.0", tk.END).strip()
        if text:
            tts = gTTS(text=text, lang='en')
            audio_file = "narration.mp3"
            tts.save(audio_file)
            os.system(f"start {audio_file}")  # This will work on Windows; adjust for other OS if needed
        else:
            messagebox.showerror("Error", "No text to narrate!")

    # Existing methods (create_snippet_ui, create_api_tester_ui, create_regex_tester_ui, create_utils_ui, save_snippet, search_snippets, show_snippet_details, send_api_request, test_regex, generate_uuid, generate_timestamp, generate_hash) remain unchanged.

if __name__ == "__main__":
    root = tk.Tk()
    app = DevToolkit(root)
    root.mainloop()
