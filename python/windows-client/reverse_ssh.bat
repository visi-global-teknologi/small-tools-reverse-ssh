@echo off
set SERVER_USERNAME=root
set SERVER_IP=159.89.207.228
set SERVER_PORT=xxxx
set SERVER_PASSWORD=xxxx
set LOCAL_PORT=3389
set LOCAL_HOST=localhost

echo Starting reverse ssh connection....
echo %SERVER_PASSWORD% y | plink.exe -ssh -pw %SERVER_PASSWORD% -N -R %SERVER_PORT%:%LOCAL_HOST%:%LOCAL_PORT% %SERVER_USERNAME%@%SERVER_IP%
