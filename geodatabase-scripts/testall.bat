set PROPY=C:\Users\%USERNAME%\AppData\Local\Programs\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
REM set PROPY=c:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
call %PROPY% .\src\py\test_interrogator_polygon.py
call %PROPY% .\src\py\test_interrogator_point.py
call %PROPY% .\src\py\test_interrogator_line.py