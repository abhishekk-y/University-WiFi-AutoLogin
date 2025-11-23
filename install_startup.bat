@echo off
REM Install Auto WiFi Login as a startup task
REM This script must be run as Administrator

echo ========================================
echo  Auto WiFi Login - Startup Installation
echo ========================================
echo.

REM Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Error: This script requires Administrator privileges!
    echo Please right-click and select "Run as Administrator"
    pause
    exit /b 1
)

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"
set "PYTHON_SCRIPT=%SCRIPT_DIR%autologin.py"

REM Check if autologin.py exists
if not exist "%PYTHON_SCRIPT%" (
    echo Error: autologin.py not found in %SCRIPT_DIR%
    pause
    exit /b 1
)

echo Installing scheduled task...
echo.

REM Create scheduled task
schtasks /create /tn "AutoWiFiLogin" /tr "pythonw \"%PYTHON_SCRIPT%\"" /sc onlogon /rl highest /f

if %errorLevel% equ 0 (
    echo.
    echo ========================================
    echo  Installation Successful!
    echo ========================================
    echo.
    echo The Auto WiFi Login will now run automatically
    echo when you log in to Windows.
    echo.
    echo To disable: run uninstall_startup.bat
    echo To stop now: taskkill /f /im pythonw.exe
    echo.
) else (
    echo.
    echo Installation failed!
    echo Please check the error messages above.
    echo.
)

pause
