@echo off
set SERVER_USERNAME=root
set SERVER_IP=159.89.207.228
set SERVER_PORT=4001
set SERVER_PASSWORD=H41kalGantengSekali
set LOCAL_PORT=3389
set LOCAL_HOST=localhost
set "PLINK_PATH=C:Users\Admin\Documents\small-tools-reverse-ssh\python\windows-client\plink.exe"

echo Starting reverse ssh connection....
echo %SERVER_PASSWORD% y | "%PLINK_PATH%" -ssh -pw %SERVER_PASSWORD% -N -R %SERVER_PORT%:%LOCAL_HOST%:%LOCAL_PORT% %SERVER_USERNAME%@%SERVER_IP%
