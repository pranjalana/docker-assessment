from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from datetime import datetime, date, time

app = Flask(__name__)

# Simple database setup
def init_db():
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            doctor_name TEXT NOT NULL,
            appointment_date DATE NOT NULL,
            appointment_time TIME NOT NULL,
            status TEXT DEFAULT 'scheduled'
        )
    ''')
    
    # Add sample data
    cursor.execute('''
        INSERT OR IGNORE INTO appointments 
        (patient_name, doctor_name, appointment_date, appointment_time)
        VALUES 
        ('John Smith', 'Dr. Alice Cooper', '2024-01-15', '10:00'),
        ('Emma Johnson', 'Dr. Brian Miller', '2024-01-15', '11:00')
    ''')
    
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/appointments')
def appointments():
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM appointments ORDER BY appointment_date, appointment_time')
    appointments = cursor.fetchall()
    conn.close()
    
    return render_template('appointments.html', appointments=appointments)

@app.route('/api/appointments', methods=['POST'])
def create_appointment():
    data = request.json
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO appointments (patient_name, doctor_name, appointment_date, appointment_time)
        VALUES (?, ?, ?, ?)
    ''', (data['patient_name'], data['doctor_name'], data['date'], data['time']))
    
    conn.commit()
    appointment_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'success': True, 'appointment_id': appointment_id})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
