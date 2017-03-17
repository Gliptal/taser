@ECHO OFF

DEL dist\taser.exe 2> nul
START /WAIT pyinstaller --clean --workpath="build" --distpath="dist" --specpath="dist" --add-data="../source/data;data" --onefile --icon="dist/icon.ico" source/taser.py
START /WAIT dist/verpatch.exe dist/taser.exe /va /langid 0x0809 /high %1 /s desc "Generate Tacview .xml files to render SLED profiles." /s product "TAcview SlEds Renderer" /s (c) "CC Attribution-ShareAlike 4.0" /pv %2
RMDIR /S /Q build 2> nul
IF EXIST dist\taser.exe (
    DEL test\generated.xml 2> nul
    CD dist
    START /WAIT taser.exe 64C West-Bomb-Circle -bd 6039 -ba 9800 -ta 7400 -ra 6200 -aa 5700 -ma 4035 -ad 640 -lh 10 -dc -fn ../test/generated
    CD ..\test
    FC correct.xml generated.xml > nul 2> nul
    IF %ERRORLEVEL% EQU 0 (
        ECHO [+]    success
    )
    ELSE (
        ECHO [-]    generating
    )
    CD ..
) ELSE (
    ECHO [-]    freezing
)
