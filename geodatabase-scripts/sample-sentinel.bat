set ENV=dev
set BASEPATH=x:\xxx
set DBUSER=xxxx
set DBPASSWORD=xxxx
set DBNAME=xxxx
set DBOWNER=xxxx
set WITHIN=month
set PYTHON1=C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
set PYTHON2=C:\Users\%USERNAME%\AppData\Local\Programs\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
set LOGDIR=%BASEPATH%\geodatabase-scripts\logs\cscl-change-detective
set NOTIFY=xxx@xxx.xxx.xxx
set NOTIFYFROM=xxx@xxx.xxx.xx
set SMTPFROM=xxxx.xxxx
if exist "%PYTHON1%" (
    set PROPY=%PYTHON1%
) else if exist "%PYTHON2%" (
    set PROPY=%PYTHON2%
)
set BATLOG=%LOGDIR%\sentinel.log
echo the sentinel is interrogating %DBOWNER% in %ENV% on %date% at %time% > %BATLOG%
CALL %PROPY% %BASEPATH%\cscl-change-detective\py\sentinel.py ^
             %ENV% ^
             --dbuser %DBUSER% ^
             --dbpassword %DBPASSWORD% ^
             --dbname %DBNAME% ^
             --owner %DBOWNER% ^
             --within %WITHIN%
if %ERRORLEVEL% NEQ 0 (
    echo. >> %BATLOG%
    echo cscl-change-detective sentinel failed to run >> %BATLOG%
    CALL %PROPY% %BASEPATH%\cscl-change-detective\py\notify.py ": %DBOWNER% (%ENV%) cscl-change-detective sentinel failed to run" %NOTIFY% NOLOG %LOGDIR% %NOTIFYFROM% %SMTPFROM%
    EXIT /B 1
) 
CALL %PROPY% %BASEPATH%\cscl-change-detective\py\notify.py ": %DBOWNER% (%ENV%) cscl-change-detective sentinel" %NOTIFY% sentinel- %BASEPATH%\cscl-change-detective\evidenceroom\%ENV% %NOTIFYFROM% %SMTPFROM%
echo. >> %BATLOG% && echo sentinel completed review of %DBOWNER% in %ENV% on %date% at %time% >> %BATLOG%
  