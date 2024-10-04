from flask import Flask, request, render_template, redirect, url_for, flash, session
import mysql.connector
from mysql.connector import Error
from PIL import Image, ImageDraw, ImageFont
import random
import string
import io
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# Function to generate CAPTCHA text
def generate_captcha_text(length=6):
    """Generate a random CAPTCHA text."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Function to generate CAPTCHA image
def generate_captcha_image(captcha_text):
    """Generate a CAPTCHA image."""
    # Create an image with white background
    img = Image.new('RGB', (150, 50), color='white')
    d = ImageDraw.Draw(img)
    
    # Optionally, you can specify a font here (default used here)
    font = ImageFont.load_default()

    # Draw the CAPTCHA text on the image
    d.text((10, 10), captcha_text, fill=(0, 0, 0), font=font)
    
    # Save the image to a bytes buffer
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    
    # Return the base64 encoded image
    return base64.b64encode(buf.getvalue()).decode('utf-8')

@app.route('/')
def index():
    # Generate a new CAPTCHA when rendering the index page
    captcha_text = generate_captcha_text()
    session['expected_captcha'] = captcha_text  # Store expected CAPTCHA in session
    captcha_image = generate_captcha_image(captcha_text)  # Generate CAPTCHA image
    return render_template('index.html', captcha_image=captcha_image)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['login']  # Ensure this matches your input name
    password = request.form['passwd']  # Ensure this matches your input name
    captcha_input = request.form['ccode']  # Get CAPTCHA input

    expected_captcha = session.get('expected_captcha')

    # Validate the CAPTCHA
    if captcha_input.strip().upper() != expected_captcha.strip().upper():  # Case insensitive comparison
        flash("Invalid CAPTCHA. Please try again.")
        return redirect(url_for('index'))

    try:
        # Establish the database connection inside the route
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="password",
            database="srm_portal"
        )
        cursor = db.cursor()

        # Check the username and password in the database
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        if user:
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password")
            return redirect(url_for('index'))

    except Error as e:
        flash(f"An error occurred: {e}")
        return redirect(url_for('index'))
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
