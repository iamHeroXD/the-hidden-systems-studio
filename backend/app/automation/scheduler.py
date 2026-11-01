import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, Any
from backend.app.config import settings

TASK_NAME = "HiddenSystemsStudioDailyProducer"

class AutomationScheduler:
    @staticmethod
    def get_status() -> Dict[str, Any]:
        """
        Queries Windows Task Scheduler to inspect the registered daily background task.
        """
        registered = False
        next_run = "06:00:00"
        status_text = "Idle"

        try:
            cmd = ["schtasks", "/query", "/tn", TASK_NAME, "/fo", "LIST"]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if res.returncode == 0:
                registered = True
                for line in res.stdout.splitlines():
                    if "Next Run Time:" in line:
                        next_run = line.split(":", 1)[1].strip()
                    if "Status:" in line:
                        status_text = line.split(":", 1)[1].strip()
        except Exception:
            pass

        return {
            "task_name": TASK_NAME,
            "registered": registered,
            "enabled": settings.daily_schedule_enabled,
            "scheduled_time": settings.daily_schedule_time,
            "next_run_time": next_run,
            "status": status_text,
            "standalone_independent_mode": True
        }

    @staticmethod
    def register_windows_task(time_str: str = "06:00") -> bool:
        """
        Creates or updates a Windows Scheduled Task running daily at the given time.
        Invokes python background runner without requiring any IDE to remain open.
        """
        python_exe = sys.executable
        runner_script = Path("f:/Work/bragvideoyt/backend/daily_runner.py").resolve()
        
        # Ensure runner script exists
        if not runner_script.exists():
            runner_script.write_text("""import asyncio
from backend.app.database import init_db
from backend.app.agents.orchestrator import ProductionOrchestrator

async def main():
    init_db()
    project = ProductionOrchestrator.create_project()
    print(f"Daily automation launched production: {project.id}")
    await ProductionOrchestrator.run_full_pipeline(project.id)
    print("Daily automation run complete.")

if __name__ == '__main__':
    asyncio.run(main())
""", encoding="utf-8")

        action_cmd = f'"{python_exe}" "{runner_script}"'
        cmd = [
            "schtasks", "/create",
            "/tn", TASK_NAME,
            "/tr", action_cmd,
            "/sc", "DAILY",
            "/st", time_str,
            "/f" # force overwrite
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        return res.returncode == 0

    @staticmethod
    def unregister_windows_task() -> bool:
        cmd = ["schtasks", "/delete", "/tn", TASK_NAME, "/f"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        return res.returncode == 0
