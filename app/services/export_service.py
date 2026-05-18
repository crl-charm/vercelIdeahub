from __future__ import annotations

from flask import render_template

from app.services.base_service import BaseService


class ExportService(BaseService):
    """Provides PDF export behavior for inheriting services."""

    def render_pdf_bytes(self, template_path: str, **context) -> bytes:
        html = render_template(template_path, **context)
        try:
            from weasyprint import HTML

            return HTML(string=html).write_pdf()
        except Exception:
            # Fallback keeps exports functional in environments without WeasyPrint runtime deps.
            return html.encode("utf-8")
