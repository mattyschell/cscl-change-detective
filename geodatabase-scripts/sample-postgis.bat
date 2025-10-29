set ENV=dev
set SRCDB=xxxx
set BASEPATH=C:\gis
set EVIDENCEROOM=%BASEPATH%\cscl-change-detective\evidenceroom\%ENV%
set CSCLGDB=%BASEPATH%\Connections\oracle19c\%ENV%\CSCL-%SRCDB%\cscl_read_only.sde
set CSCLLAYER=CSCL.XYZ
set CSCLLAYERNAME=XYZ
set CSCLLAYERCOLS=XYZ_ID
set EXTERNALSOURCE=abcdatabase
set POSTGISTABLE=XYZ
set EXTERNALLAYERCOLS=XYZ_ID
set EXTERNALWHERECLAUSE="value='SpreadLoveItsTheBrooklynWay'"
set LOGDIR=%BASEPATH%\cscl-change-detective\geodatabase-scripts\logs\%ENV%
set NOTIFY=xxx@xxx.xxx.xxx
set NOTIFYFROM=xxx@xxx.xxx.xxx
set SMTPFROM=xxxx.xxxx
set PYTHON1=C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
set PYTHON2=C:\Users\%USERNAME%\AppData\Local\Programs\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
if exist "%PYTHON1%" (
    set PROPY=%PYTHON1%
) else if exist "%PYTHON2%" (
    set PROPY=%PYTHON2%
) 
set BATLOG=%LOGDIR%\%ENV%-%CSCLLAYERNAME%.log
echo investigating %ENV% %CSCLLAYER% on %date% at %time% > %BATLOG%
CALL %PROPY% %BASEPATH%\cscl-change-detective\py\investigate.py ^
             %CSCLGDB% ^
             %CSCLLAYER% ^
             %CSCLLAYERCOLS% ^
             %EXTERNALSOURCE% ^
             %EXTERNALLAYERCOLS% ^
             %EVIDENCEROOM% ^
             %LOGDIR% ^
             --postgistable %POSTGISTABLE% ^
             --externalwhereclause %EXTERNALWHERECLAUSE% 
if %ERRORLEVEL% NEQ 0 (
    echo. >> %BATLOG%
    echo cscl-change-detective failed to run >> %BATLOG%
    %PROPY% %BASEPATH%\cscl-change-detective\py\notify.py ": %CSCLLAYERNAME% cscl-change-detective failed to run" %NOTIFY% NOLOG %LOGDIR% %NOTIFYFROM% %SMTPFROM%
    EXIT /B 0
) 
%PROPY% %BASEPATH%\cscl-change-detective\py\notify.py ": %CSCLLAYERNAME% cscl-change-detective" %NOTIFY% %CSCLLAYERNAME% %LOGDIR% %NOTIFYFROM% %SMTPFROM%
echo. >> %BATLOG% && echo completed %ENV% %CSCLLAYER% on %date% at %time% >> %BATLOG%
   