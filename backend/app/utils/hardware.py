import psutil
import shutil
import subprocess
from typing import Dict, Any, Optional

def get_system_telemetry() -> Dict[str, Any]:
    # CPU
    cpu_percent = psutil.cpu_percent(interval=None)
    
    # RAM
    ram = psutil.virtual_memory()
    ram_used_gb = round(ram.used / (1024 ** 3), 2)
    ram_total_gb = round(ram.total / (1024 ** 3), 2)
    ram_percent = ram.percent

    # Disk
    total, used, free = shutil.disk_usage("f:/Work/bragvideoyt")
    disk_free_gb = round(free / (1024 ** 3), 2)
    disk_total_gb = round(total / (1024 ** 3), 2)

    # GPU Check via nvidia-smi if present
    gpu_name = None
    vram_used = None
    vram_total = None

    try:
        smi_out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,memory.used,memory.total", "--format=csv,noheader,nounits"],
            timeout=1.5,
            stderr=subprocess.DEVNULL
        ).decode().strip()
        if smi_out:
            parts = [p.strip() for p in smi_out.splitlines()[0].split(",")]
            if len(parts) >= 3:
                gpu_name = parts[0]
                vram_used = round(float(parts[1]) / 1024, 2)
                vram_total = round(float(parts[2]) / 1024, 2)
    except Exception:
        gpu_name = "Integrated / Software (CPU Fallback active)"

    return {
        "cpu_percent": cpu_percent,
        "ram_used_gb": ram_used_gb,
        "ram_total_gb": ram_total_gb,
        "ram_percent": ram_percent,
        "disk_free_gb": disk_free_gb,
        "disk_total_gb": disk_total_gb,
        "gpu_name": gpu_name,
        "gpu_vram_used_gb": vram_used,
        "gpu_vram_total_gb": vram_total
    }
