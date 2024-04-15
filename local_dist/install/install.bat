@echo off

@Set "SCRIPT=%TEMP%/CheckerBoard-%RANDOM%-%RANDOM%.vbs"
@(  echo Set oWS = WScript.CreateObject("WScript.Shell"^)
	echo sDesktop = oWS.SpecialFolders("Desktop")
    echo Set oLink = oWS.CreateShortcut(sDesktop & "\CheckerBoard.lnk")
    echo oLink.TargetPath = oWS.ScriptFullName
	echo oLink.WindowStyle = 1
	echo oLink.Hotkey = "Ctrl+Alt+f"
	echo oLink.IconLocation = "notepad.exe, 0"
	echo oLink.Description = "UWIT CheckerBoard"
    echo oLink.WorkingDirectory = sDesktop
	echo oLink.Arguments = oWS.ScriptFullName & "..\..\src\checkerBoard.py"
    echo oLink.Save
)>"%SCRIPT%"
@"%__AppDir__%cscript.exe" // NoLogo "%SCRIPT%"
@Del "%SCRIPT%"