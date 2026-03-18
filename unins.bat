@echo off
echo.
echo  Uninstalling Yoink...
echo.

powershell -Command "$p = [System.Environment]::GetEnvironmentVariable('Path', 'Machine'); $p = $p -replace ';C:\\Yoink', '' -replace 'C:\\Yoink;', '' -replace 'C:\\Yoink', ''; [System.Environment]::SetEnvironmentVariable('Path', $p, 'Machine')"

if %errorlevel% neq 0 (
    echo  [!] Failed to remove from PATH. Try running as Administrator.
    pause
    exit /b 1
)

echo  [+] Removed C:\Yoink from PATH.

if exist "C:\Yoink" (
    rmdir /s /q "C:\Yoink"
    echo  [+] Deleted C:\Yoink.
) else (
    echo  [=] C:\Yoink not found, nothing to delete.
)

echo.
echo  Yoink has been uninstalled. Open a new terminal to apply PATH changes.
echo.
pause
