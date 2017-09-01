@ECHO OFF

DEL   dist\taser.exe 2> nul
START /WAIT pyinstaller --clean --workpath="build" --distpath="dist" --specpath="dist" --add-data="../source/data;data" --onefile --icon="dist/icon.ico" source/taser.py
START /WAIT dist/verpatch.exe dist/taser.exe /va /langid 0x0809 /high %1 /s desc "Generate Tacview .xml files to render SLED profiles." /s product "TAcview SLEDs Renderer" /s copyright "CC Attribution-ShareAlike 4.0" /pv %2
RMDIR /S /Q build 2> nul

IF EXIST dist\taser.exe (
    CD    dist

    DEL   ..\test\generated.xml 2> nul
    START /WAIT taser.exe -d -f ../test/generated -c -lh 10 -ad 640 -bd 6039 -ba 9800 -ta 7400 -ra 6200 -aa 5700 -ma 4035 range 64C West-Bomb-Circle
    FC    ..\test\correct.xml ..\test\generated.xml > nul 2> nul
    IF %ERRORLEVEL% EQU 0 (
        ECHO [+]    "range" success
    ) ELSE (
        ECHO [-]    "range" generating
    )

    DEL   ..\test\generated.xml 2> nul
    START /WAIT taser.exe -d -f ../test/generated -c -ah 355 -lh 10 -ad 640 -bd 6039 -ba 9800 -ta 7400 -ra 6200 -aa 5700 -ma 4035 coords 36.40.51.N 115.40.26.W 3035
    FC    ..\test\correct.xml ..\test\generated.xml > nul 2> nul
    IF %ERRORLEVEL% EQU 0 (
        ECHO [+]    "coords" success
    ) ELSE (
        ECHO [-]    "coords" fail
    )
) ELSE (
    ECHO [-]    packaging
)
