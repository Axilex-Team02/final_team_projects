from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'electrician_secret_key' # In production, use a secure random key

def get_db_connection():
    conn = sqlite3.connect('contractor.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        hashed_pw = generate_password_hash(password)
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO Users (username, email, password, role) VALUES (?, ?, ?, ?)',
                         (username, email, hashed_pw, 'user'))
            conn.commit()
        except sqlite3.IntegrityError:
            flash('Username or Email already exists.', 'error')
            conn.close()
            return redirect(url_for('register'))
            
        conn.close()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM Users WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    electricians_count = conn.execute('SELECT COUNT(*) FROM Electricians').fetchone()[0]
    jobs_count = conn.execute('SELECT COUNT(*) FROM Jobs').fetchone()[0]
    tasks_count = conn.execute('SELECT COUNT(*) FROM Tasks').fetchone()[0]
    
    # Recent jobs for dashboard
    recent_jobs = conn.execute('SELECT * FROM Jobs ORDER BY id DESC LIMIT 5').fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', 
                           electricians_count=electricians_count,
                           jobs_count=jobs_count,
                           tasks_count=tasks_count,
                           recent_jobs=recent_jobs)

@app.route('/electricians')
def electricians():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('electricians.html')

@app.route('/jobs')
def jobs():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('jobs.html')

@app.route('/materials')
def materials():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('materials.html')

@app.route('/tasks')
def tasks():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('tasks.html')

@app.route('/reporter')
def reporter():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('reporter.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)
