"""
Setup wizard for the Auto WiFi Login system
"""
import os
import sys
import subprocess
from colorama import init, Fore, Style
from credential_manager import CredentialManager

# Initialize colorama
init(autoreset=True)


def check_dependencies():
    """Check if all required packages are installed"""
    print(f"\n{Fore.CYAN}Checking dependencies...")
    
    required_packages = ['requests', 'cryptography', 'colorama']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"{Fore.GREEN}  ✓ {package}")
        except ImportError:
            print(f"{Fore.RED}  ✗ {package} (missing)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n{Fore.YELLOW}Installing missing packages...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install"
            ] + missing_packages)
            print(f"{Fore.GREEN}✓ All dependencies installed!")
        except subprocess.CalledProcessError:
            print(f"{Fore.RED}✗ Failed to install dependencies.")
            print(f"{Fore.YELLOW}Please run: pip install -r requirements.txt")
            return False
    else:
        print(f"{Fore.GREEN}✓ All dependencies are installed!")
    
    return True


def configure_credentials():
    """Run the credential setup wizard"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"  Credential Configuration")
    print(f"{'='*60}")
    
    manager = CredentialManager()
    
    if manager.credentials_exist():
        print(f"\n{Fore.YELLOW}⚠ Credentials already exist!")
        response = input("Do you want to reconfigure? (y/N): ").strip().lower()
        
        if response != 'y':
            print(f"{Fore.CYAN}Keeping existing credentials.")
            return True
        
        manager.delete_credentials()
    
    return manager.setup_wizard()


def setup_startup_task():
    """Optionally set up Windows Task Scheduler for auto-start"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"  Startup Configuration")
    print(f"{'='*60}")
    
    print(f"\n{Fore.YELLOW}Do you want the auto-login to run at system startup?")
    print("This will create a Windows scheduled task that runs when you log in.")
    
    response = input("Enable auto-start? (Y/n): ").strip().lower()
    
    if response == 'n':
        print(f"{Fore.CYAN}Skipping auto-start configuration.")
        print(f"You can run it later using: install_startup.bat")
        return True
    
    # Check if batch file exists
    batch_file = os.path.join(os.path.dirname(__file__), 'install_startup.bat')
    
    if not os.path.exists(batch_file):
        print(f"{Fore.RED}✗ install_startup.bat not found!")
        print(f"{Fore.YELLOW}Please run it manually after setup completes.")
        return True
    
    try:
        print(f"\n{Fore.CYAN}Running install_startup.bat...")
        print(f"{Fore.YELLOW}Note: This requires administrator privileges.")
        
        # Run the batch file with elevated privileges
        subprocess.run(['powershell', 'Start-Process', batch_file, '-Verb', 'RunAs'], check=True)
        
        print(f"{Fore.GREEN}✓ Startup task configured!")
        return True
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}✗ Failed to configure startup task.")
        print(f"{Fore.YELLOW}You can run install_startup.bat manually later.")
        return True


def test_configuration():
    """Test that credentials can be loaded"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"  Testing Configuration")
    print(f"{'='*60}\n")
    
    try:
        manager = CredentialManager()
        username, password = manager.load_credentials()
        
        if username and password:
            print(f"{Fore.GREEN}✓ Credentials loaded successfully!")
            print(f"  Username: {username}")
            print(f"  Password: {'*' * len(password)}")
            return True
        else:
            print(f"{Fore.RED}✗ Failed to load credentials!")
            return False
    except Exception as e:
        print(f"{Fore.RED}✗ Error: {str(e)}")
        return False


def main():
    """Main setup process"""
    print(f"\n{Style.BRIGHT}{Fore.CYAN}{'='*60}")
    print(f"   University WiFi Auto-Login Setup")
    print(f"   Access Made By Tuskk")
    print(f"{'='*60}{Style.RESET_ALL}")
    
    # Step 1: Check dependencies
    if not check_dependencies():
        return
    
    # Step 2: Configure credentials
    if not configure_credentials():
        print(f"\n{Fore.RED}Setup failed. Please try again.")
        return
    
    # Step 3: Test configuration
    if not test_configuration():
        print(f"\n{Fore.RED}Setup validation failed!")
        return
    
    # Step 4: Optional startup configuration
    setup_startup_task()
    
    # Final message
    print(f"\n{Style.BRIGHT}{Fore.GREEN}{'='*60}")
    print(f"   Setup Complete!")
    print(f"{'='*60}{Style.RESET_ALL}\n")
    print(f"{Fore.CYAN}To start the auto-login service, run:")
    print(f"{Fore.WHITE}  python autologin.py\n")
    print(f"{Fore.CYAN}To run in the background:")
    print(f"{Fore.WHITE}  pythonw autologin.py\n")
    print(f"{Fore.YELLOW}Press any key to exit...")
    input()


if __name__ == "__main__":
    main()
