"""
Secure credential management with encryption
"""
import json
import os
from cryptography.fernet import Fernet
from getpass import getpass
import config


class CredentialManager:
    """Manages encrypted storage and retrieval of user credentials"""
    
    def __init__(self):
        self.key_file = config.ENCRYPTION_KEY_FILE
        self.creds_file = config.CREDENTIALS_FILE
        self.cipher = None
        self._initialize_encryption()
    
    def _initialize_encryption(self):
        """Initialize or load the encryption key"""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                key = f.read()
        else:
            # Generate a new encryption key
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
        
        self.cipher = Fernet(key)
    
    def save_credentials(self, username, password):
        """
        Encrypt and save credentials to file
        
        Args:
            username (str): User's username/UID
            password (str): User's password
        """
        credentials = {
            'username': username,
            'password': password
        }
        
        # Convert to JSON and encrypt
        json_data = json.dumps(credentials).encode()
        encrypted_data = self.cipher.encrypt(json_data)
        
        # Save to file
        with open(self.creds_file, 'wb') as f:
            f.write(encrypted_data)
        
        print(f"✓ Credentials saved successfully!")
    
    def load_credentials(self):
        """
        Load and decrypt credentials from file
        
        Returns:
            tuple: (username, password) or (None, None) if not found
        """
        if not os.path.exists(self.creds_file):
            return None, None
        
        try:
            with open(self.creds_file, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt and parse JSON
            decrypted_data = self.cipher.decrypt(encrypted_data)
            credentials = json.loads(decrypted_data.decode())
            
            return credentials['username'], credentials['password']
        except Exception as e:
            print(f"✗ Error loading credentials: {e}")
            return None, None
    
    def credentials_exist(self):
        """Check if credentials are already saved"""
        return os.path.exists(self.creds_file)
    
    def delete_credentials(self):
        """Delete saved credentials"""
        if os.path.exists(self.creds_file):
            os.remove(self.creds_file)
            print("✓ Credentials deleted")
    
    def setup_wizard(self):
        """Interactive setup wizard for first-time configuration"""
        print("\n" + "="*60)
        print("   University WiFi Auto-Login - First Time Setup")
        print("="*60)
        print("\nThis wizard will help you set up automatic WiFi login.")
        print("Your credentials will be encrypted and stored locally.\n")
        
        username = input("Enter your University UID/Username: ").strip()
        password = getpass("Enter your Password (hidden): ")
        
        # Confirm password
        password_confirm = getpass("Confirm Password: ")
        
        if password != password_confirm:
            print("\n✗ Passwords do not match! Please try again.")
            return False
        
        if not username or not password:
            print("\n✗ Username and password cannot be empty!")
            return False
        
        # Save credentials
        self.save_credentials(username, password)
        
        print("\n✓ Setup complete! Your credentials are now encrypted and saved.")
        print("  The auto-login system is ready to use.\n")
        
        return True


if __name__ == "__main__":
    # Test the credential manager
    manager = CredentialManager()
    
    if not manager.credentials_exist():
        manager.setup_wizard()
    else:
        print("Credentials already exist.")
        username, password = manager.load_credentials()
        print(f"Loaded username: {username}")
        print(f"Password loaded: {'*' * len(password)}")
