import asyncio
import sys
from pathlib import Path
from backend.app.database import init_db, get_production_record
from backend.app.agents.orchestrator import ProductionOrchestrator

async def main():
    print("=== STARTING THE HIDDEN SYSTEMS STUDIO: PILOT PRODUCTION ===", flush=True)
    print("TOPIC: What If The Entire Internet Disappeared For 24 Hours?", flush=True)
    init_db()

    project = ProductionOrchestrator.create_project(
        topic_override="What If The Entire Internet Disappeared For 24 Hours?"
    )
    print(f"Created project: {project.id} in {project.output_dir}", flush=True)

    # Run through stages
    project_dict = get_production_record(project.id)
    stages = project_dict["stages"]

    for idx, stage in enumerate(stages):
        print(f"\n[Stage {idx+1}/18] Running: {stage['name']}...", flush=True)
        success = await ProductionOrchestrator.run_stage(project_dict, idx)
        if not success:
            print(f"FAILED at stage: {stage['name']}", flush=True)
            sys.exit(1)
        # Reload updated record
        project_dict = get_production_record(project.id)
        current_st = project_dict["stages"][idx]
        print(f"--> COMPLETED: {current_st['message']}", flush=True)

    print("\n=== PILOT PRODUCTION SUCCESSFULLY COMPLETED ===", flush=True)
    final_mp4 = Path(project_dict.get('final_mp4_path', ''))
    if final_mp4.exists():
        size_mb = round(final_mp4.stat().st_size / (1024 * 1024), 2)
        print(f"VERIFIED DELIVERABLE: Final MP4 exists ({size_mb} MB) at:\n  {final_mp4}", flush=True)
    else:
        print(f"ERROR: Final MP4 missing at: {final_mp4}", flush=True)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
