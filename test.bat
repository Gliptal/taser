@ECHO OFF

DEL test\generated.xml 2> nul
CD source
START /WAIT python taser.py 64C West-Bomb-Circle -bd 6039 -ba 9800 -ta 7400 -ra 6200 -aa 5700 -ma 4035 -ad 640 -lh 10 -dc -fn ../test/generated
CD ..\test
FC correct.xml generated.xml > nul 2> nul
IF %ERRORLEVEL% EQU 0 (
    ECHO [+]    success
) ELSE (
    ECHO [-]    fail
)
CD ..
