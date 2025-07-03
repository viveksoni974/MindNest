from flask import Flask, request, jsonify, render_template
from transformers import pipeline
import sqlite3
import os

app = Flask(__name__)
sentiment_model = pipeline("sentiment-analysis")

def init_db():
    if not os.path.exists('journal.db'):
        conn = sqlite3.connect('journal.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE journal (id INTEGER PRIMARY KEY AUTOINCREMENT, entry TEXT, mood TEXT)''')
        conn.commit()
        conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/journal', methods = ['POST'])
def journal():
    data = request.get_json()
    entry = data.get('entry', '')
    mood = sentiment_model(entry)[0]['label']
    conn = sqlite3.connect('journal.db')
    c = conn.cursor()
    c.execute('INSERT INTO journal (entry, mood) VALUES (?, ?)', (entry, mood))
    conn.commit()
    conn.close()
    return jsonify({'mood': mood})

@app.route('/entries', methods = ['GET'])
def entries():
    conn = sqlite3.connect('journal.db')
    c = conn.cursor()
    c.execute('SELECT * FROM journal')
    rows = c.fetchall()
    conn.close()

    return jsonify(rows)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)