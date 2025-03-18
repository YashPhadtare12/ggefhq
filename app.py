from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Load data from JSON file
def load_data():
    if os.path.exists("data.json"):
        with open("data.json", "r") as file:
            return json.load(file)
    return {}

# Save data to JSON file
def save_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

# Home Page
@app.route("/")
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("index.html")

# Add Doctor Page
@app.route("/add-doctor", methods=["GET", "POST"])
def add_doctor():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        data = load_data()
        username = session['username']
        
        new_doctor = {
            "name": request.form["doctor-name"],
            "mobile": request.form["mobile"],
            "email": request.form["email"],
            "gender": request.form["gender"],
            "dob": request.form["dob"],
            "address": request.form["address"],
            "specialization": request.form["specialization"],
            "experience": request.form["experience"],
            "qualification": request.form["qualification"],
            "consultation_fee": request.form["consultation-fee"],
        }
        
        if username not in data:
            data[username] = {"doctors": [], "appointments": [], "patients": []}
        data[username]["doctors"].append(new_doctor)
        save_data(data)
        return redirect(url_for("home"))
    return render_template("add-doctor.html")

# Add Patient Page
@app.route("/add-patient", methods=["GET", "POST"])
def add_patient():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        data = load_data()
        username = session['username']
        
        new_patient = {
            "name": request.form["patient-name"],
            "mobile": request.form["mobile"],
            "email": request.form["email"],
            "gender": request.form["gender"],
            "address": request.form["address"],
            "dob": request.form["dob"],
        }
        
        if username not in data:
            data[username] = {"doctors": [], "appointments": [], "patients": []}
        data[username]["patients"].append(new_patient)
        save_data(data)
        return redirect(url_for("home"))
    return render_template("add-patient.html")

# Schedule Appointment Page
@app.route("/schedule-appointment", methods=["GET", "POST"])
def schedule_appointment():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    data = load_data()
    username = session['username']
    
    if request.method == "POST":
        new_appointment = {
            "patient_name": request.form["patient-name"],
            "doctor": request.form["doctor"],
            "date": request.form["date"],
            "time": request.form["time"],
            "status": "Scheduled",
        }
        
        if username not in data:
            data[username] = {"doctors": [], "appointments": [], "patients": []}
        data[username]["appointments"].append(new_appointment)
        save_data(data)
        return redirect(url_for("view_appointments"))
    
    doctors = data.get(username, {}).get("doctors", [])
    patients = data.get(username, {}).get("patients", [])
    return render_template("schedule-appointments.html", doctors=doctors, patients=patients)

# View Appointments Page
@app.route("/view-appointments")
def view_appointments():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    data = load_data()
    username = session['username']
    appointments = data.get(username, {}).get("appointments", [])
    return render_template("view-appointments.html", appointments=appointments)

# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = load_data()
        username = request.json.get("username")
        password = request.json.get("password")

        # Check if user exists
        user = next((user for user in data.get("users", []) if user["username"] == username and user["password"] == password), None)
        if user:
            session['username'] = username  # Store username in session
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": "Invalid username or password."})
    return render_template("login.html")

# Signup Page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = load_data()
        name = request.json.get("name")
        email = request.json.get("email")
        username = request.json.get("username")
        password = request.json.get("password")

        # Check if username already exists
        if any(user["username"] == username for user in data.get("users", [])):
            return jsonify({"success": False, "message": "Username already exists."})

        # Add new user
        new_user = {
            "name": name,
            "email": email,
            "username": username,
            "password": password,
        }
        if "users" not in data:
            data["users"] = []
        data["users"].append(new_user)
        save_data(data)
        return jsonify({"success": True})
    return render_template("signup.html")

# Logout
@app.route("/logout")
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('login'))

# Run the application
if __name__ == "__main__":
    app.run(debug=True)