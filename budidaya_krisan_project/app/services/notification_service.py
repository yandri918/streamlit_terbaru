"""
Notification Service — WhatsApp / Webhook Dispatcher
Budidaya Krisan Pro
"""
import json
import logging
from typing import Dict, Optional
import requests
from app.services.db import get_db

logger = logging.getLogger(__name__)


def get_webhook_config() -> Dict:
    with get_db() as conn:
        row = conn.execute("SELECT * FROM webhook_config WHERE id=1").fetchone()
        if row:
            return dict(row)
        return {"webhook_url": "", "is_enabled": 0}


def save_webhook_config(webhook_url: str, is_enabled: bool) -> bool:
    from datetime import datetime
    now = datetime.now().isoformat()
    with get_db() as conn:
        conn.execute(
            "INSERT INTO webhook_config(id, webhook_url, is_enabled, updated_at) "
            "VALUES(1, ?, ?, ?) "
            "ON CONFLICT(id) DO UPDATE SET webhook_url=excluded.webhook_url, "
            "is_enabled=excluded.is_enabled, updated_at=?",
            [webhook_url, 1 if is_enabled else 0, now, now]
        )
    return True


def send_growth_notification(batch_code: str, variety: str, week: int,
                              height: float, health_score: float, grade: str,
                              deviation: float) -> bool:
    """Send growth record notification via webhook."""
    config = get_webhook_config()
    if not config.get("is_enabled") or not config.get("webhook_url"):
        return False

    deviation_text = f"+{deviation:.1f}%" if deviation >= 0 else f"{deviation:.1f}%"
    stars = "⭐⭐⭐⭐⭐" if health_score >= 85 else (
            "⭐⭐⭐⭐" if health_score >= 70 else (
            "⭐⭐⭐" if health_score >= 55 else "⭐⭐"))

    message = (
        f"🌸 BUDIDAYA KRISAN PRO — Update Pertumbuhan\n"
        f"🌱 {variety} | Batch: {batch_code}\n"
        f"📅 Minggu ke-{week}\n"
        f"📏 Tinggi: {height} cm ({deviation_text} vs standar)\n"
        f"💚 Health Score: {health_score:.1f} / 100 {stars}\n"
        f"🎯 Grade AI: {grade}\n"
        f"---\n"
        f"🤖 Budidaya Krisan Pro | AI Monitoring System"
    )

    return _dispatch(config["webhook_url"], message)


def send_test_notification() -> bool:
    config = get_webhook_config()
    if not config.get("webhook_url"):
        return False
    return _dispatch(config["webhook_url"],
                     "🌸 Uji Coba Notifikasi — Budidaya Krisan Pro berfungsi dengan baik! ✅")


def _dispatch(webhook_url: str, message: str) -> bool:
    """Dispatch message to webhook URL."""
    try:
        # Generic webhook (Discord, n8n, custom)
        payload = {"content": message, "text": message, "message": message}
        resp = requests.post(webhook_url, json=payload, timeout=10)
        resp.raise_for_status()

        # Update last_sent_at
        from datetime import datetime
        now = datetime.now().isoformat()
        with get_db() as conn:
            conn.execute("UPDATE webhook_config SET last_sent_at=? WHERE id=1", [now])
        return True
    except Exception as e:
        logger.error(f"Webhook dispatch failed: {e}")
        return False
