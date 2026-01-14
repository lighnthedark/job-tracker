from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database setup function
def init_db():
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            position TEXT NOT NULL,
            date_applied TEXT NOT NULL,
            status TEXT NOT NULL,
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database when app starts
@app.route('/')
def index():
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute('SELECT * FROM jobs ORDER BY date_applied DESC')
    jobs = c.fetchall()
    conn.close()
    return render_template('index.html', jobs=jobs)

@app.route('/add', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        company = request.form['company']
        position = request.form['position']
        date_applied = request.form['date_applied']
        status = request.form['status']
        notes = request.form.get('notes', '')
        
        conn = sqlite3.connect('jobs.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO jobs (company, position, date_applied, status, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (company, position, date_applied, status, notes))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('add_job.html')



if __name__ == '__main__':
    app.run(debug=True)