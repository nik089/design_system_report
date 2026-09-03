@echo off
cd /d "%~dp0"
python main.py --input government_ux4g_website_urls.md --concurrency 8 --timeout 18 >scan_stdout.txt 2>scan_stderr.txt
echo Exit code: %ERRORLEVEL%
echo === STDOUT ===
type scan_stdout.txt
echo === STDERR (last 60 lines) ===
powershell -Command "Get-Content scan_stderr.txt | Select-Object -Last 60"
