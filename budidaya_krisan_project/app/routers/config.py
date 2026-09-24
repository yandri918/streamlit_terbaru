"""
Config Router — Webhook & Notification Settings
GET  /api/v1/config/webhook    - Get webhook config
POST /api/v1/config/webhook    - Save webhook config
POST /api/v1/config/webhook/test - Send test notification
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from app.schemas.common import ApiResponse
from app.services.notification_service import (
    get_webhook_config, save_webhook_config, send_test_notification
)

router = APIRouter(prefix="/config", tags=["Config"])


class WebhookConfigPayload(BaseModel):
    webhook_url: Optional[str] = ""
    is_enabled: bool = False


@router.get("/webhook", response_model=ApiResponse)
def get_webhook():
    config = get_webhook_config()
    return ApiResponse.ok(config)


@router.post("/webhook", response_model=ApiResponse)
def save_webhook(payload: WebhookConfigPayload):
    save_webhook_config(payload.webhook_url or "", payload.is_enabled)
    return ApiResponse.ok(None, "Konfigurasi webhook berhasil disimpan.")


@router.post("/webhook/test", response_model=ApiResponse)
def test_webhook():
    success = send_test_notification()
    if success:
        return ApiResponse.ok(None, "Pesan uji coba berhasil dikirim.")
    return ApiResponse.fail("Gagal mengirim uji coba. Pastikan URL webhook valid dan aktif.")


class ClerkAuthConfigPayload(BaseModel):
    clerk_publishable_key: Optional[str] = ""
    clerk_secret_key: Optional[str] = ""


@router.get("/auth", response_model=ApiResponse)
def get_auth_config():
    from app.config import settings
    return ApiResponse.ok({
        "clerk_publishable_key": settings.CLERK_PUBLISHABLE_KEY or "",
        "is_configured": bool(settings.CLERK_PUBLISHABLE_KEY),
    })


@router.post("/auth", response_model=ApiResponse)
def save_auth_config(payload: ClerkAuthConfigPayload):
    from app.config import settings
    import os
    if payload.clerk_publishable_key:
        settings.CLERK_PUBLISHABLE_KEY = payload.clerk_publishable_key
        os.environ["CLERK_PUBLISHABLE_KEY"] = payload.clerk_publishable_key
    if payload.clerk_secret_key:
        settings.CLERK_SECRET_KEY = payload.clerk_secret_key
        os.environ["CLERK_SECRET_KEY"] = payload.clerk_secret_key
    return ApiResponse.ok({
        "clerk_publishable_key": settings.CLERK_PUBLISHABLE_KEY or "",
        "is_configured": bool(settings.CLERK_PUBLISHABLE_KEY),
    }, "Konfigurasi Clerk Authentication berhasil disimpan.")
