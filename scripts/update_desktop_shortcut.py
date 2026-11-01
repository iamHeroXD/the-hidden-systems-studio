import os
import subprocess
from pathlib import Path

desktop = Path(os.environ["USERPROFILE"]) / "Desktop"
icon_path = Path(r"f:\Work\bragvideoyt\assets\studio_icon.ico").resolve()
target_bat = Path(r"f:\Work\bragvideoyt\start_studio.bat").resolve()
working_dir = Path(r"f:\Work\bragvideoyt").resolve()

vbs_content = f'''Set WshShell = WScript.CreateObject("WScript.Shell")
Set shortcut = WshShell.CreateShortcut("{desktop}\\THE HIDDEN SYSTEMS STUDIO.lnk")
shortcut.TargetPath = "{target_bat}"
shortcut.WorkingDirectory = "{working_dir}"
shortcut.WindowStyle = 1
shortcut.Description = "The Hidden Systems Studio - Autonomous Documentary Production Suite"
shortcut.IconLocation = "{icon_path},0"
shortcut.Save
'''

vbs_path = Path("create_shortcut.vbs")
vbs_path.write_text(vbs_content, encoding="utf-8")

subprocess.run(["cscript", "//nologo", str(vbs_path)], check=True)
if vbs_path.exists():
    vbs_path.unlink()

print(f"Updated shortcut at {desktop / 'THE HIDDEN SYSTEMS STUDIO.lnk'} with icon {icon_path}")
