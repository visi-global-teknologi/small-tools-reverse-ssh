@echo off
set SERVER_USERNAME=root
set SERVER_IP=66.42.49.122
set SERVER_PORT=3387
set SERVER_PASSWORD=fJ}2nWG$yV6ocyU$
set LOCAL_PORT=3389
set LOCAL_HOST=localhost

echo Starting reverse ssh connection....
echo %SERVER_PASSWORD% | plink.exe -ssh -pw %SERVER_PASSWORD% -N -R %SERVER_PORT%:%LOCAL_HOST%:%LOCAL_PORT% %SERVER_USERNAME%@%SERVER_IP%
