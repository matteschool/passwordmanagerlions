import json
import re
import random
import string
import csv

# Caesar cipher encryption and decryption functions (pre-implemented)
def caesar_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shifted = ord(char) + shift
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
            encrypted_text += chr(shifted)
        else:
            encrypted_text += char
    return encrypted_text

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

# Password strength checker function (optional)
def is_strong_password(password):
    return (
        len(password) >= 8 and
        any(char.islower() for char in password) and
        any(char.isupper() for char in password) and
        any(char.isdigit() for char in password)
    )

 
# Password generator function (optional)
def generate_password(length):
    password = random.choice(string.ascii_lowercase)
    password += random.choice(string.ascii_uppercase)
    password += random.choice(string.digits)
    password += ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length - 3))
    
    password_list = list(password)
    random.shuffle(password_list)
    password = ''.join(password_list)

    return password

# Initialize empty lists to store encrypted passwords, websites, and usernames
encrypted_passwords = []
websites = []
usernames = []

# Function to add a new password
def add_password(website=None, username=None, password=None):
    if website is None:
        website = input("Website: ")
    if username is None:
        username = input("Username: ")

    generate_random_password = input("Do you want to generate a random password? (yes/no): ").lower()
    
    if generate_random_password == 'yes':
        password_length = 0
        while True:
            try:
                password_length = int(input("Enter the length of the password (minimum 8 characters): "))
                if password_length >= 8:
                    break
                else:
                    print("Password length must be at least 8 characters.")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
        password = generate_password(password_length)
    elif password is None:
        password = input("Password: ")

    while not is_strong_password(password):
        print("Weak password. Please make sure your password meets the strength criteria.")
        password = input("Password: ")

    encrypted_password = caesar_encrypt(password, shift=3)

    websites.append(website)
    usernames.append(username)
    encrypted_passwords.append(encrypted_password)


# Function to retrieve a password
def get_password():
    global websites, usernames, encrypted_passwords
    
    website_url = input("Insert website (e.g. google.com): ")

    if website_url in websites:
        index = websites.index(website_url)

        username = usernames[index]
        decrypted_password = encrypted_passwords[index]

        decrypted_password = caesar_decrypt(decrypted_password, shift=3)

        print()
        print(f"Website: {website_url}")
        print(f"Username: {username}")
        print(f"Password: {decrypted_password}")
    else:
        print("Website not found.")
    
    return None


# Function to save passwords to a CSV file 
def save_passwords(filename='vault.csv'):
    if not websites or not usernames or not encrypted_passwords:
        print("There is no data to save.")
        return

    data = zip(websites, usernames, encrypted_passwords)

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Website', 'Username', 'Encrypted Password'])
        writer.writerows(data)



# Function to load passwords from a JSON file
def load_passwords():

    global websites, usernames, encrypted_passwords

    with open('vault.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            websites.append(row['Website'])
            usernames.append(row['Username'])
            encrypted_passwords.append(row['Encrypted Password'])

    return None

  
def main():
# implement user interface 

  while True:
    print("\nPassword Manager Menu:")
    print("1. Add Password")
    print("2. Get Password")
    print("3. Save Passwords")
    print("4. Load Passwords")
    print("5. Quit")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        add_password()
    elif choice == "2":
        get_password()
    elif choice == "3":
        save_passwords()
    elif choice == "4":
        passwords = load_passwords()
        print("Passwords loaded successfully!")
    elif choice == "5":
        break
    else:
        print("Invalid choice. Please try again.")

# Execute the main function when the program is run
if __name__ == "__main__":
    main()
