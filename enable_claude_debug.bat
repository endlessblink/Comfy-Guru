@echo off
echo === Enable Claude Desktop Debug Mode ===
echo.

set "CLAUDE_CONFIG_DIR=%APPDATA%\Claude"
set "DEV_SETTINGS=%CLAUDE_CONFIG_DIR%\developer_settings.json"

REM Create Claude config directory if it doesn't exist
if not exist "%CLAUDE_CONFIG_DIR%" (
    mkdir "%CLAUDE_CONFIG_DIR%"
)

REM Create developer settings file
echo Creating developer settings to enable debug mode...
echo { > "%DEV_SETTINGS%"
echo   "allowDevTools": true >> "%DEV_SETTINGS%"
echo } >> "%DEV_SETTINGS%"

echo.
echo ✓ Debug mode enabled!
echo.
echo Developer settings saved to:
echo %DEV_SETTINGS%
echo.
echo You can now:
echo - Use Command+Option+Shift+I (Mac) or Ctrl+Alt+Shift+I (Windows) to open DevTools
echo - View detailed logs in: %LOCALAPPDATA%\Claude\Logs\
echo.
pause