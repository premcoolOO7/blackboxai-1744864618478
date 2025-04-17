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

class DevToolkitCLI:
    def __init__(self):
        self.create_database()

    def create_database(self):
        self.conn = sqlite3.connect('dev_toolkit.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS snippets
                         (id INTEGER PRIMARY KEY, title TEXT, code TEXT, tags TEXT, created_at TIMESTAMP)''')
        self.conn.commit()

    def save_snippet(self, title, code, tags):
        if title and code.strip():
            self.c.execute("INSERT INTO snippets (title, code, tags, created_at) VALUES (?, ?, ?, ?)",
                          (title, code, tags, datetime.now()))
            self.conn.commit()
            print("Snippet saved successfully!")
        else:
            print("Error: Title and code are required!")

    def extract_text_from_pdf(self, file_path):
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    def narrate_pdf(self, text):
        if text:
            tts = gTTS(text=text, lang='en')
            audio_file = "narration.mp3"
            tts.save(audio_file)
            os.system(f"start {audio_file}")  # Adjust for your OS if needed
        else:
            print("Error: No text to narrate!")

    def run(self):
        while True:
            print("\nDev Toolkit CLI")
            print("1. Save Snippet")
            print("2. Upload PDF and Narrate")
            print("3. Exit")
            choice = input("Choose an option: ")

            if choice == '1':
                title = input("Enter snippet title: ")
                code = input("Enter snippet code: ")
                tags = input("Enter tags (comma-separated): ")
                self.save_snippet(title, code, tags)
            elif choice == '2':
                file_path = input("Enter the path to the PDF file: ")
                text = self.extract_text_from_pdf(file_path)
                print("Extracted Text:\n", text)
                narrate = input("Do you want to narrate this text? (yes/no): ")
                if narrate.lower() == 'yes':
                    self.narrate_pdf(text)
            elif choice == '3':
                break
            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    toolkit = DevToolkitCLI()
    toolkit.run()
