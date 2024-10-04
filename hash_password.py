import bcrypt

def hash_password(plain_password):
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed_password

if __name__ == "__main__":
    # Example usage
    plain_password = input("Enter password to hash: ")
    hashed = hash_password(plain_password)
    print("Hashed password:", hashed.decode('utf-8'))  # Decode to print it as a string
