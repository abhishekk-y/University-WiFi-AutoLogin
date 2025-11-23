"""
University WiFi Auto-Login System
Automatically detects and authenticates with the university WiFi captive portal
"""
import time
import requests
import logging
from datetime import datetime
from colorama import init, Fore, Style
import config
from credential_manager import CredentialManager

# Initialize colorama for Windows
init(autoreset=True)


class AutoLogin:
    """Main auto-login application"""
    
    def __init__(self):
        self.cred_manager = CredentialManager()
        self.username = None
        self.password = None
        self.session = requests.Session()
        self._setup_logging()
        self._load_credentials()
    
    def _setup_logging(self):
        """Configure logging system"""
        logging.basicConfig(
            level=getattr(logging, config.LOG_LEVEL),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(config.LOG_FILE),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _load_credentials(self):
        """Load credentials from encrypted storage"""
        self.username, self.password = self.cred_manager.load_credentials()
        
        if not self.username or not self.password:
            print(f"{Fore.RED}✗ No credentials found!")
            print(f"{Fore.YELLOW}Please run setup.py first to configure your credentials.")
            exit(1)
    
    def _print_status(self, message, status="info"):
        """Print colored status messages"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if status == "success":
            print(f"{Fore.GREEN}[{timestamp}] ✓ {message}")
        elif status == "error":
            print(f"{Fore.RED}[{timestamp}] ✗ {message}")
        elif status == "warning":
            print(f"{Fore.YELLOW}[{timestamp}] ⚠ {message}")
        else:
            print(f"{Fore.CYAN}[{timestamp}] ℹ {message}")
    
    def check_internet_connectivity(self):
        """
        Check if internet is accessible (not behind captive portal)
        
        Returns:
            bool: True if internet is accessible, False if login required
        """
        for test_url in config.TEST_URLS:
            try:
                response = self.session.get(
                    test_url,
                    timeout=config.REQUEST_TIMEOUT,
                    allow_redirects=True
                )
                
                # Check if we're redirected to the auth page
                if config.AUTH_URL_PATTERN in response.url:
                    return False
                
                # Successfully connected to internet
                if response.status_code == 200:
                    return True
                    
            except requests.RequestException:
                continue
        
        return False
    
    def perform_login(self):
        """
        Perform the login operation to the captive portal
        
        Returns:
            bool: True if login successful, False otherwise
        """
        try:
            self._print_status("Attempting to login...", "info")
            
            # Prepare login payload
            payload = {
                config.USERNAME_FIELD: self.username,
                config.PASSWORD_FIELD: self.password
            }
            
            # Submit login form
            response = self.session.post(
                config.LOGIN_URL,
                data=payload,
                timeout=config.REQUEST_TIMEOUT,
                allow_redirects=True
            )
            
            # Give it a moment to process
            time.sleep(2)
            
            # Verify login was successful by checking internet connectivity
            if self.check_internet_connectivity():
                self._print_status("Login successful! Internet access granted.", "success")
                self.logger.info(f"Successfully logged in as {self.username}")
                return True
            else:
                self._print_status("Login may have failed. Will retry...", "warning")
                self.logger.warning("Login appeared to fail - still behind captive portal")
                return False
                
        except requests.RequestException as e:
            self._print_status(f"Login failed: {str(e)}", "error")
            self.logger.error(f"Login error: {str(e)}")
            return False
    
    def run(self):
        """Main loop - continuously monitor and auto-login"""
        print(f"\n{Style.BRIGHT}{Fore.CYAN}{'='*60}")
        print(f"   University WiFi Auto-Login System")
        print(f"   Access Made By Tuskk")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        print(f"{Fore.GREEN}✓ Credentials loaded for: {self.username}")
        print(f"{Fore.CYAN}ℹ Monitoring network status every 2 seconds (instant detection)...")
        print(f"{Fore.YELLOW}⚠ Press Ctrl+C to stop\n")
        
        self.logger.info("Auto-login service started")
        
        try:
            while True:
                # Check if we need to login
                if not self.check_internet_connectivity():
                    self._print_status("Authentication required - Internet not accessible", "warning")
                    
                    # Attempt login
                    if self.perform_login():
                        self._print_status("You are now connected to the internet!", "success")
                    else:
                        self._print_status(f"Retrying in {config.RETRY_DELAY} seconds...", "warning")
                        time.sleep(config.RETRY_DELAY)
                        continue
                else:
                    # Already logged in
                    self._print_status("✓ Already logged in - Internet access active", "success")
                
                # Wait before next check
                time.sleep(config.CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Auto-login service stopped by user.")
            self.logger.info("Auto-login service stopped by user")
        except Exception as e:
            self._print_status(f"Unexpected error: {str(e)}", "error")
            self.logger.error(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    app = AutoLogin()
    app.run()
