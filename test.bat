@ECHO OFF

CD    source

DEL   ..\test\generated.xml 2> nul
START /WAIT python taser.py -d -f ../test/generated -c -lh 10 -ad 640 -bd 6039 -ba 9800 -ta 7400 -ra 6200 -aa 5700 -ma 4035 range 64C West-Bomb-Circle
FC    ..\test\correct.xml ..\test\generated.xml > nul 2> nul
IF %ERRORLEVEL% EQU 0 (
    ECHO [+]    "range" success
) ELSE (
    ECHO [-]    "range" fail
)

DEL   ..\test\generated.xml 2> nul
START /WAIT python taser.py -d -f ../test/generated -c -ah 355 -lh 10 -ad 640 -bd 6039 -ba 9800 -ta 7400 -ra 6200 -aa 5700 -ma 4035 coords 36.40.51.N 115.40.26.W 3035
FC    ..\test\correct.xml ..\test\generated.xml > nul 2> nul
IF %ERRORLEVEL% EQU 0 (
    ECHO [+]    "coords" success
) ELSE (
    ECHO [-]    "coords" fail
)

CD ..
