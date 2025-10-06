from flask import Flask, render_template, request, jsonify
import sqlite3
import os

# Initialize Flask app with correct template path
app = Flask(__name__, template_folder='/app/templates')

def init_db():
    """Initialize the SQLite database"""
    conn = sqlite3.connect('/app/database/hospital.db')
    cursor = conn.cursor()
    
    # Create appointments table
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
    
    # Create patients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mrn TEXT UNIQUE NOT NULL
        )
    ''')
    
    # Create doctors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT NOT NULL
        )
    ''')
    
    # Insert sample data if empty
    cursor.execute('SELECT COUNT(*) FROM appointments')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO appointments 
            (patient_name, doctor_name, appointment_date, appointment_time)
            VALUES 
            ('John Smith', 'Dr. Alice Cooper', '2024-01-15', '10:00'),
            ('Emma Johnson', 'Dr. Brian Miller', '2024-01-15', '11:00')
        ''')
        
        cursor.execute('''
            INSERT INTO patients (name, mrn) 
            VALUES 
            ('John Smith', 'MRN001'),
            ('Emma Johnson', 'MRN002')
        ''')
        
        cursor.execute('''
            INSERT INTO doctors (name, specialization)
            VALUES
            ('Dr. Alice Cooper', 'Cardiology'),
            ('Dr. Brian Miller', 'Neurology')
        ''')
    
    conn.commit()
    conn.close()

@app.route('/')
def home():
    print("🔍 DEBUG: Loading index.html template")
    return render_template('index.html')

@app.route('/appointments')
def appointments():
    conn = sqlite3.connect('/app/database/hospital.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM appointments ORDER BY appointment_date, appointment_time')
    appointments = cursor.fetchall()
    conn.close()
    
    print("🔍 DEBUG: Loading appointments.html template")
    return render_template('appointments.html', appointments=appointments)

@app.route('/api/appointments', methods=['POST'])
def create_appointment():
    data = request.json
    conn = sqlite3.connect('/app/database/hospital.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO appointments (patient_name, doctor_name, appointment_date, appointment_time)
        VALUES (?, ?, ?, ?)
    ''', (data['patient_name'], data['doctor_name'], data['date'], data['time']))
    
    conn.commit()
    appointment_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'success': True, 'appointment_id': appointment_id})

@app.route('/api/doctors')
def get_doctors():
    conn = sqlite3.connect('/app/database/hospital.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, specialization FROM doctors')
    doctors = cursor.fetchall()
    conn.close()
    
    doctor_list = []
    for doctor in doctors:
        doctor_list.append({
            'id': doctor[0],
            'name': doctor[1],
            'specialization': doctor[2]
        })
    
    return jsonify(doctors=doctor_list)

@app.route('/api/patients')
def get_patients():
    conn = sqlite3.connect('/app/database/hospital.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, mrn FROM patients')
    patients = cursor.fetchall()
    conn.close()
    
    patient_list = []
    for patient in patients:
        patient_list.append({
            'id': patient[0],
            'name': patient[1],
            'mrn': patient[2]
        })
    
    return jsonify(patients=patient_list)

if __name__ == '__main__':
    print("🚀 Starting Hospital Scheduler...")
    print("📁 Current directory:", os.getcwd())
    print("📁 Templates path:", '/app/templates')
    print("📁 Templates exists:", os.path.exists('/app/templates'))
    if os.path.exists('/app/templates'):
        print("📄 Template files:", os.listdir('/app/templates'))
    
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)