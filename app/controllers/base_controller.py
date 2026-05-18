from __future__ import annotations


class BaseController:
    """Base interface for all Flask blueprint controllers."""

    blueprint = None

    def register(self, app) -> None:
        app.register_blueprint(self.blueprint)

    def get_dashboard_data(self) -> dict:
        raise NotImplementedError
