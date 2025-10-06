// Hospital Scheduler JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Hospital Scheduler loaded');
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
});

// Enhanced appointment booking
function bookAppointment() {
    const patientName = prompt("Enter patient name:");
    if (!patientName) return;
    
    const doctorName = prompt("Enter doctor name:"); 
    if (!doctorName) return;
    
    const date = prompt("Enter date (YYYY-MM-DD):");
    if (!date) return;
    
    const time = prompt("Enter time (HH:MM):");
    if (!time) return;
    
    // Validate date format
    if (!isValidDate(date)) {
        alert('Please enter date in YYYY-MM-DD format');
        return;
    }
    
    // Validate time format
    if (!isValidTime(time)) {
        alert('Please enter time in HH:MM format (24-hour)');
        return;
    }
    
    fetch('/api/appointments', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            patient_name: patientName,
            doctor_name: doctorName, 
            date: date,
            time: time
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('✅ Appointment booked successfully! ID: ' + data.appointment_id);
            // Reload the page to show new appointment
            setTimeout(() => location.reload(), 1000);
        } else {
            alert('❌ Failed to book appointment: ' + data.message);
        }
    })
    .catch(error => {
        alert('❌ Error: ' + error.message);
    });
}

function isValidDate(dateString) {
    const regex = /^\d{4}-\d{2}-\d{2}$/;
    if (!regex.test(dateString)) return false;
    const date = new Date(dateString);
    return date instanceof Date && !isNaN(date);
}

function isValidTime(timeString) {
    const regex = /^([01]?[0-9]|2[0-3]):[0-5][0-9]$/;
    return regex.test(timeString);
}

function bookEmergency() {
    if (confirm('🚨 This is for emergency appointments only. Continue?')) {
        const patientName = prompt("Enter patient name for emergency appointment:");
        const doctorName = prompt("Enter doctor name:");
        
        if (patientName && doctorName) {
            // For now, use the same API but mark as emergency in notes
            const currentDate = new Date().toISOString().split('T')[0];
            const currentTime = new Date().toTimeString().split(' ')[0].substring(0, 5);
            
            fetch('/api/appointments', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    patient_name: patientName + ' (EMERGENCY)',
                    doctor_name: doctorName, 
                    date: currentDate,
                    time: currentTime
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('🚨 EMERGENCY APPOINTMENT BOOKED! ID: ' + data.appointment_id);
                    setTimeout(() => location.reload(), 1000);
                } else {
                    alert('❌ Failed to book emergency appointment: ' + data.message);
                }
            });
        }
    }
}   