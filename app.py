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
    
    # Calculate stats for dashboard
    c.execute('SELECT COUNT(*) FROM jobs')
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM jobs WHERE status = 'Applied'")
    applied = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM jobs WHERE status = 'Interview'")
    interview = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM jobs WHERE status = 'Offer'")
    offer = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM jobs WHERE status = 'Rejected'")
    rejected = c.fetchone()[0]
    
    conn.close()
    
    stats = {
        'total': total,
        'applied': applied,
        'interview': interview,
        'offer': offer,
        'rejected': rejected
    }
    
    return render_template('index.html', jobs=jobs, stats=stats)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
