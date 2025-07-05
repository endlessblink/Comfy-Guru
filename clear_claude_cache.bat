@echo off
echo === Claude Desktop Cache Cleaner ===
echo.
echo This will clear Claude Desktop cache to fix extension issues.
echo Please make sure Claude Desktop is COMPLETELY CLOSED before continuing.
echo.
pause

REM Kill any remaining Claude processes
taskkill /F /IM Claude.exe 2>nul
timeout /t 2 >nul

echo.
echo Clearing Claude cache directories...

REM Clear Roaming cache
if exist "%APPDATA%\Claude\Cache" (
    echo Deleting %APPDATA%\Claude\Cache...
    rmdir /s /q "%APPDATA%\Claude\Cache" 2>nul
)

if exist "%APPDATA%\Claude\Code Cache" (
    echo Deleting %APPDATA%\Claude\Code Cache...
    rmdir /s /q "%APPDATA%\Claude\Code Cache" 2>nul
)

REM Clear Local cache
if exist "%LOCALAPPDATA%\Claude\Cache" (
    echo Deleting %LOCALAPPDATA%\Claude\Cache...
    rmdir /s /q "%LOCALAPPDATA%\Claude\Cache" 2>nul
)

if exist "%LOCALAPPDATA%\AnthropicClaude\Cache" (
    echo Deleting %LOCALAPPDATA%\AnthropicClaude\Cache...
    rmdir /s /q "%LOCALAPPDATA%\AnthropicClaude\Cache" 2>nul
)

if exist "%LOCALAPPDATA%\AnthropicClaude\Code Cache" (
    echo Deleting %LOCALAPPDATA%\AnthropicClaude\Code Cache...
    rmdir /s /q "%LOCALAPPDATA%\AnthropicClaude\Code Cache" 2>nul
)

if exist "%LOCALAPPDATA%\AnthropicClaude\GPUCache" (
    echo Deleting %LOCALAPPDATA%\AnthropicClaude\GPUCache...
    rmdir /s /q "%LOCALAPPDATA%\AnthropicClaude\GPUCache" 2>nul
)

if exist "%LOCALAPPDATA%\AnthropicClaude\DawnGraphiteCache" (
    echo Deleting %LOCALAPPDATA%\AnthropicClaude\DawnGraphiteCache...
    rmdir /s /q "%LOCALAPPDATA%\AnthropicClaude\DawnGraphiteCache" 2>nul
)

if exist "%LOCALAPPDATA%\AnthropicClaude\DawnWebGPUCache" (
    echo Deleting %LOCALAPPDATA%\AnthropicClaude\DawnWebGPUCache...
    rmdir /s /q "%LOCALAPPDATA%\AnthropicClaude\DawnWebGPUCache" 2>nul
)

REM Clear extension-specific cache
if exist "%APPDATA%\Claude\Claude Extensions\*.cache" (
    echo Deleting extension cache files...
    del /q "%APPDATA%\Claude\Claude Extensions\*.cache" 2>nul
)

REM Clear temporary extension files
if exist "%TEMP%\claude-extensions-*" (
    echo Deleting temporary extension files...
    rmdir /s /q "%TEMP%\claude-extensions-*" 2>nul
)

echo.
echo === Cache cleared successfully! ===
echo.
echo Next steps:
echo 1. Start Claude Desktop
echo 2. Go to Settings > Extensions
echo 3. Install your extension fresh
echo.
pause