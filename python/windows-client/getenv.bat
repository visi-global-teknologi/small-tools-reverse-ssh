@echo off

set "envFile=.env"

for /f "usebackq delims=" %%a in ("%envFile%") do (
    set "line=%%a"
    setlocal enabledelayedexpansion
    for /f "delims== tokens=1,2" %%b in ("!line!") do (
        endlocal
        set "key=%%b"
        set "value=%%c"
        setlocal enabledelayedexpansion
        if defined value (
            set "!key!=!value!"
        ) else (
            echo Warning: Invalid line in %envFile%: !line!
        )
    )
    endlocal
)

rem Example usage
echo Variable1: %CMD_EXE%
echo Variable2: %PLINK_EXE%
