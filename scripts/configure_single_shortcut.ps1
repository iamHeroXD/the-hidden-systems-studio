$wsh = New-Object -ComObject WScript.Shell
$desktop = [System.Environment]::GetFolderPath('Desktop')
$shortcutPath = Join-Path $desktop "THE HIDDEN SYSTEMS STUDIO.lnk"
$shortcut = $wsh.CreateShortcut($shortcutPath)
$shortcut.TargetPath = "f:\Work\bragvideoyt\start_studio.bat"
$shortcut.WorkingDirectory = "f:\Work\bragvideoyt"
$shortcut.WindowStyle = 1
$shortcut.Description = "The Hidden Systems Studio - Autonomous AI Animated Documentary Production Suite"
$shortcut.IconLocation = "f:\Work\bragvideoyt\assets\studio_icon.ico,0"
$shortcut.Save()

Write-Host "Single Desktop shortcut configured cleanly with icon!"
