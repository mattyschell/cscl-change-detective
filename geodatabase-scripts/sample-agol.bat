set ENV=dev
set SRCDB=xxxx
set BASEPATH=C:\gis
set EVIDENCEROOM=%BASEPATH%\cscl-change-detective\evidenceroom\%ENV%
set CSCLGDB=%BASEPATH%\Connections\oracle19c\%ENV%\CSCL-%SRCDB%\cscl_read_only.sde
set CSCLLAYER=CSCL_PUB.XYZ
set CSCLLAYERNAME=XYZ
set CSCLLAYERCOLS=XYZ_ID
set EXTERNALLAYER=https://services5.arcgis.com/1234567/ArcGIS/rest/services/xyz/FeatureServer/0
set EXTERNALLAYERCOLS=XYZ_ID
set LOGDIR=%BASEPATH%\cscl-change-detective\geodatabase-scripts\logs\%ENV%
set NOTIFY=xxx@xxx.xxx.xxx
set NOTIFYFROM=xxx@xxx.xxx.xx
set SMTPFROM=xxxx.xxxx
REM set PROPY=c:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
set PROPY=C:\Users\%USERNAME%\AppData\Local\Programs\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
set BATLOG=%LOGDIR%\%ENV%-%CSCLLAYERNAME%.log
echo investigating %ENV% %CSCLLAYER% on %date% at %time% > %BATLOG%
CALL %PROPY% %BASEPATH%\cscl-change-detective\src\py\investigate.py %CSCLGDB% %CSCLLAYER% %CSCLLAYERCOLS% %EXTERNALLAYER% %EXTERNALLAYERCOLS% %EVIDENCEROOM% %LOGDIR%
if %ERRORLEVEL% NEQ 0 (
    echo. >> %BATLOG%
    echo cscl-change-detective failed to run >> %BATLOG%
    %PROPY% %BASEPATH%\cscl-change-detective\src\py\notify.py ": %CSCLLAYERNAME% cscl-change-detective failed to run" %NOTIFY% NOLOG %LOGDIR% %NOTIFYFROM% %SMTPFROM%
    EXIT /B 0
) 
%PROPY% %BASEPATH%\cscl-change-detective\src\py\notify.py ": %CSCLLAYERNAME% cscl-change-detective" %NOTIFY% %CSCLLAYERNAME% %LOGDIR% %NOTIFYFROM% %SMTPFROM%
echo. >> %BATLOG% && echo completed %ENV% %CSCLLAYER% on %date% at %time% >> %BATLOG%
   