@ECHO OFF
g:
cd G:/py-astronomy/script

ECHO Click any key to build
PAUSE
ECHO Building........
pyinstaller --noconfirm --onefile --console --icon "G:/py-astronomy/src/ico/blackhole.ico" --name "PYlanatarium"  "G:/py-astronomy/src/main.py"


@RD /S /Q "G:/py-astronomy/script/build"
del "PYlanatarium.spec"
PAUSE