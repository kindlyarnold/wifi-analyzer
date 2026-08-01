@echo off
REM WiFi Network Security Analyzer - Windows Launcher
REM This script will show you what to do while Docker builds

cls
echo.
echo ================================================================================
echo         WiFi NETWORK SECURITY ANALYZER - SETUP & WAIT SCREEN
echo ================================================================================
echo.
echo.
echo STATUS CHECK:
echo =============
echo.

REM Check Docker
docker images | findstr wifi-analyzer
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [!] Docker image 'wifi-analyzer' is still BUILDING...
    echo [!] This typically takes 5-10 minutes on first run
    echo.
) else (
    echo.
    echo [+] WiFi Analyzer Docker image is READY!
    echo.
)

echo.
echo WHAT'S HAPPENING:
echo ================
echo.
echo 1. Docker is downloading and installing:
echo    - Debian Linux (base OS)
echo    - Nmap (network scanning)
echo    - Hydra (credential testing)
echo    - Python 3 (analysis engine)
echo.
echo 2. Building will complete automatically
echo    - Check back in a few minutes
echo    - Size: ~450 MB compressed
echo.
echo.
echo TO USE THE TOOL:
echo ================
echo.
echo Once the Docker image is built, run these commands in PowerShell:
echo.
echo Basic Scan (2-5 min):
echo -----
echo docker run --rm --privileged --network host ^
echo   -v %cd%/output:/output ^
echo   wifi-analyzer:latest 192.168.1.0/24
echo.
echo.
echo Full Analysis (5-15 min):
echo -----
echo docker run --rm --privileged --network host ^
echo   -v %cd%/output:/output ^
echo   wifi-analyzer:latest 192.168.1.0/24 -c -a
echo.
echo.
echo DOCUMENTATION:
echo ===============
echo.
echo Open these files to learn more:
echo  - README.md (Quick start)
echo  - USAGE_GUIDE.md (Complete manual)
echo  - PROJECT_SUMMARY.md (How it works)
echo.
echo.
echo FILES LOCATION:
echo ===============
echo.
echo Current directory:
echo %cd%
echo.
echo.
echo NEXT: Wait 5 minutes, then check build status again
echo       Command: docker images | findstr wifi-analyzer
echo.
echo ================================================================================
pause
