pushd %~dp0

set ARCHICAD_PATH="C:\Program Files\GRAPHISOFT\Archicad 27\Archicad.exe"

set FILE1="%~dp0TestProject01.pla"
set FILE2="%~dp0TestProject02.pla"
set FILE3="%~dp0TestProject03.pla"
set FILE4="%~dp0TestProject04.pla"
set FILE5="%~dp0TestProject05.pla"

rem Start each Archicad instance with the corresponding file
start "" %ARCHICAD_PATH% %FILE1%
start "" %ARCHICAD_PATH% %FILE2%
start "" %ARCHICAD_PATH% %FILE3%
start "" %ARCHICAD_PATH% %FILE4%
start "" %ARCHICAD_PATH% %FILE5%

start "" %ARCHICAD_PATH% "%~dp0TestProject01.pla" -demo
start "" %ARCHICAD_PATH% "%~dp0TestProject02.pla" -demo
start "" %ARCHICAD_PATH% "%~dp0TestProject03.pla" -demo
start "" %ARCHICAD_PATH% "%~dp0TestProject04.pla" -demo
start "" %ARCHICAD_PATH% "%~dp0TestProject05.pla" -demo

rem Return to the original directory
popd
