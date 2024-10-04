import mysql.connector
import time
import os

# Function to read username and password from file
def read_credentials():
    with open('credentials.txt', 'r') as file:
        lines = file.readlines()
        # Extract username and password
        username = lines[0].split(":")[1].strip()
        password = lines[1].split(":")[1].strip()
        return username, password

# Function to update the database with new credentials
def update_db(username, password):
    try:
        # Establish database connection (replace with your DB credentials)
        db = mysql.connector.connect(
            host="localhost",
            user="root",          # Your MySQL root user
            passwd="password",    # MySQL root password
            database="srm_portal" # Database name
        )
        cursor = db.cursor()

        # Update username and password in your desired table (adjust to your schema)
        cursor.execute("UPDATE users SET password=%s WHERE username=%s", (password, username))
        
        db.commit()
        print(f"Updated user: {username} with new password.")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    finally:
        cursor.close()
        db.close()

# Function to monitor the file for changes
def monitor_credentials_file():
    last_mtime = 0
    while True:
        try:
            # Get the file modification time
            mtime = os.path.getmtime('credentials.txt')
            if mtime != last_mtime:
                last_mtime = mtime
                print("Detected changes in credentials file.")
                
                # Read the new credentials and update the database
                username, password = read_credentials()
                update_db(username, password)

            # Sleep for a few seconds before checking again
            time.sleep(5)

        except FileNotFoundError:
            print("Credentials file not found. Make sure 'credentials.txt' exists.")
            break

if __name__ == "__main__":
    monitor_credentials_file()
