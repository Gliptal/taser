@ECHO OFF

DEL test\generated.xml
CD source
START /WAIT python taser.py 64C West-Bomb-Circle -bd 6039 -ba 9800 -ta 7400 -ra 6200 -aa 5700 -ma 4035 -ad 640 -lh 10 -dc -fn ../test/generated
CD ..\test
FC correct.xml generated.xml > nul
CD ..
IF ERRORLEVEL 1 (
    ECHO [-]    fail
    )
IF NOT ERRORLEVEL 1 (
    ECHO [+]    success
    )
