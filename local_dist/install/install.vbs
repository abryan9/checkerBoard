set oWS = WScript.CreateObject("WScript.Shell")
set fso = WScript.CreateObject("Scripting.FileSystemObject")
WinDir = oWS.ExpandEnvironmentStrings("%WinDir%")
sDesktop = oWS.SpecialFolders("Desktop")
sShortcut = sDesktop & "\UWIT RoomCheck.lnk"
if not fso.FileExists(sShortcut) then
	set oLink = oWS.CreateShortcut(sShortcut)
	' WScript.Echo WScript.Arguments(0) & "src\run.vbs " & Chr(34) & WScript.Arguments(0) & Chr(34)
	oLink.TargetPath = "C:\UWApps\checkerBoard\src\run.vbs"
	oLink.WindowStyle = 1
	oLink.Hotkey = "Ctrl+Alt+f"
	oLink.IconLocation = "C:\UWApps\checkerBoard\dist\install\UW_Signature_stacked_brown_cropped.ico, 0"
	oLink.Description = "UWIT CheckerBoard"
	' oLink.WorkingDirectory = sDesktop
	' oLink.Arguments = WScript.Arguments(0)
	oLink.Save
end if