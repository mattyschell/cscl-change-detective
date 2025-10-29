set PYTHON1=C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
set PYTHON2=C:\Users\%USERNAME%\AppData\Local\Programs\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
if exist "%PYTHON1%" (
    set PROPY=%PYTHON1%
) else if exist "%PYTHON2%" (
    set PROPY=%PYTHON2%
) 
call %PROPY% .\test\test_interrogator_polygon.py
call %PROPY% .\test\test_interrogator_point.py
call %PROPY% .\test\test_interrogator_line.py
call %PROPY% .\test\test_interrogator_polygon_agol.py
set PGUSER=postgres
set PGDATABASE=postgres
set PGHOST=localhost
%PROPY% .\test\test_interrogator_polygon_postgis.py
%PROPY% .\test\test_interrogator_point_postgis.py