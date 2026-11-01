from typing import Dict, Any
from backend.app.config import settings
from backend.app.database import get_connection

class CostTracker:
    # Estimated pricing per 1k tokens or audio minutes
    COST_MAP = {
        "gemini_input_1k": 0.000125,
        "gemini_output_1k": 0.000375,
        "tts_per_minute": 0.000, # Edge-TTS is free; Kokoro is free
        "video_render_cost": 0.000 # Local FFmpeg
    }

    @staticmethod
    def record_usage(production_id: str, provider: str, units: float, unit_type: str) -> float:
        rate = 0.0
        if "gemini" in provider.lower():
            rate = CostTracker.COST_MAP.get(f"gemini_{unit_type}_1k", 0.0002) / 1000.0
        cost = units * rate

        conn = get_connection()
        try:
            conn.execute(
                "INSERT INTO production_logs (production_id, stage_key, level, message, timestamp) VALUES (?, ?, ?, ?, datetime('now'))",
                (production_id, "cost_tracker", "INFO", f"Cost incurred: ${cost:.4f} via {provider} ({units} {unit_type})")
            )
            # Update production cost_estimate_usd
            conn.execute(
                "UPDATE productions SET cost_estimate_usd = cost_estimate_usd + ? WHERE id = ?",
                (cost, production_id)
            )
            conn.commit()
        except Exception as e:
            print(f"Error recording cost: {e}")
        finally:
            conn.close()
        return cost

    @staticmethod
    def get_summary() -> Dict[str, float]:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(cost_estimate_usd) FROM productions WHERE created_at >= date('now', 'start of day')")
            daily = cursor.fetchone()[0] or 0.0
            cursor.execute("SELECT SUM(cost_estimate_usd) FROM productions WHERE created_at >= date('now', 'start of month')")
            monthly = cursor.fetchone()[0] or 0.0
            return {
                "daily_cost_usd": round(daily, 4),
                "monthly_cost_usd": round(monthly, 4),
                "daily_limit_usd": settings.daily_spend_limit_usd,
                "monthly_limit_usd": settings.monthly_spend_limit_usd,
                "budget_alert": daily >= settings.daily_spend_limit_usd or monthly >= settings.monthly_spend_limit_usd
            }
        except Exception:
            return {"daily_cost_usd": 0.0, "monthly_cost_usd": 0.0, "daily_limit_usd": 10.0, "monthly_limit_usd": 150.0, "budget_alert": False}
        finally:
            conn.close()
