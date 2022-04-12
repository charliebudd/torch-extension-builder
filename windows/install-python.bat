
@echo off

set PYTHON_VERSION=%1
echo Finding latest python %PYTHON_VERSION% patch version...
FOR /L %%p IN (20,-1,0) DO (call :tryinstall %%p && exit /B)
EXIT /B %ERRORLEVEL% 

:tryinstall 
set PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%.%~1
set PYTHON_FILE=python-%PYTHON_VERSION%.%~1-amd64.exe
curl --silent -k -L --fail "%PYTHON_URL%/%PYTHON_FILE%" --output "%PYTHON_FILE%" || exit /b
echo Installing python %PYTHON_VERSION%.%~1...
%PYTHON_FILE% /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
del -f "%PYTHON_FILE%"
EXIT /B %ERRORLEVEL%
