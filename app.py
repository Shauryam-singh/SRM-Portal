from flask import Flask, request, render_template, redirect, url_for
import MySQLdb

app = Flask(__name__)

# Connect to MySQL Database
db = MySQLdb.connect(host="localhost", user="root", passwd="password", db="srm_portal")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    netid = request.form['login']
    password = request.form['passwd']
    
    cursor = db.cursor()
    cursor.execute("SELECT * FROM students WHERE netid=%s AND password=%s", (netid, password))
    student = cursor.fetchone()
    
    if student:
        return redirect(url_for('dashboard'))  # If valid, redirect to dashboard
    else:
        return "Invalid credentials", 401

@app.route('/dashboard')
def dashboard():
    return "Welcome to your dashboard!"

if __name__ == "__main__":
    app.run(debug=True)
