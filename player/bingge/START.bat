@echo off
setlocal EnableExtensions
cd /d "%~dp0"
echo ========================================
echo  BinggePlayer LAUNCHER_V5
echo ========================================
echo.

REM --- 1) py launcher (often works right after install) ---
where py >nul 2>nul
if not errorlevel 1 (
  echo Using: py -3
  py -3 server.py
  goto end
)

REM --- 2) python on PATH ---
where python >nul 2>nul
if not errorlevel 1 (
  echo Using: python from PATH
  python server.py
  goto end
)

REM --- 3) common user install folders (no PATH needed) ---
if exist "%LocalAppData%\Programs\Python\Python314\python.exe" (
  echo Using: %LocalAppData%\Programs\Python\Python314\python.exe
  "%LocalAppData%\Programs\Python\Python314\python.exe" server.py
  goto end
)
if exist "%LocalAppData%\Programs\Python\Python313\python.exe" (
  echo Using: Python313
  "%LocalAppData%\Programs\Python\Python313\python.exe" server.py
  goto end
)
if exist "%LocalAppData%\Programs\Python\Python312\python.exe" (
  echo Using: Python312
  "%LocalAppData%\Programs\Python\Python312\python.exe" server.py
  goto end
)

REM --- 4) any Python3* under LocalAppData ---
for /d %%D in ("%LocalAppData%\Programs\Python\Python*") do (
  if exist "%%D\python.exe" (
    echo Using: %%D\python.exe
    "%%D\python.exe" server.py
    goto end
  )
)

REM --- 5) Program Files ---
for /d %%D in ("%ProgramFiles%\Python*") do (
  if exist "%%D\python.exe" (
    echo Using: %%D\python.exe
    "%%D\python.exe" server.py
    goto end
  )
)

echo.
echo [ERROR] Python still not found.
echo 1. Open the Python installer again
echo 2. Click Install Now and wait until FINISHED
echo 3. RESTART the computer once
echo 4. Double-click START.bat again
echo.
echo If black window shows Chinese garbage like erver.py
echo you are still using the OLD folder. Delete it and unzip v4.
echo.
pause
:end
endlocal
