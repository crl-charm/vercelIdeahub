from __future__ import annotations

import base64
from io import BytesIO

import qrcode

from app.services.base_service import BaseService


class IdeaService(BaseService):
    """Idea-specific utility service operations."""

    def generate_qr(self, idea_id: int) -> str:
        """Generate a base64 PNG QR payload for the idea URL token."""
        qr = qrcode.QRCode(version=1, box_size=8, border=2)
        qr.add_data(f"idea:{idea_id}")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
        return f"data:image/png;base64,{encoded}"
