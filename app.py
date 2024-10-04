from flask import Flask, request, render_template, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# Connect to MySQL Database
db = mysql.connector.connect(
    host="localhost",
    user="root",          # Your MySQL root user
    passwd="password",    # MySQL root password
    database="srm_portal" # Database name
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['login']  # Ensure this matches your input name
    password = request.form['passwd']  # Ensure this matches your input name

    print(f"Attempting to log in with username: {username}")  # Debug output

    try:
        # Establish the database connection
        db = mysql.connector.connect(
            host="localhost",
            user="root",          # Your MySQL root user
            passwd="password",    # MySQL root password
            database="srm_portal" # Database name
        )
        
        # Create a cursor
        cursor = db.cursor()

        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        print(f"User found: {user}")  # Debug output
        
        if user:
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password")  # Flash an error message
            return redirect(url_for('index'))

    except Error as e:
        print(f"Error: {e}")
        return "An error occurred", 500
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')  # Make sure you have this template

if __name__ == "__main__":
    app.run(debug=True)
