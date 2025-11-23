@echo off
REM Uninstall Auto WiFi Login startup task
REM This script must be run as Administrator

echo ========================================
echo  Auto WiFi Login - Startup Uninstallation
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

echo Removing scheduled task...
echo.

REM Delete scheduled task
schtasks /delete /tn "AutoWiFiLogin" /f

if %errorLevel% equ 0 (
    echo.
    echo ========================================
    echo  Uninstallation Successful!
    echo ========================================
    echo.
    echo The Auto WiFi Login will no longer run
    echo automatically at startup.
    echo.
    echo To reinstall: run install_startup.bat
    echo.
) else (
    echo.
    echo Uninstallation failed!
    echo The task may not exist or requires different permissions.
    echo.
)

pause
