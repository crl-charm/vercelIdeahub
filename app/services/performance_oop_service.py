from __future__ import annotations

from sqlalchemy import func

from app.models.idea import Idea, IdeaVote
from app.models.user import User
from app.services.base_service import BaseService


class PerformanceService(BaseService):
    """Computes participation and engagement performance metrics."""

    def get_summary(self) -> dict:
        ideas_per_user_rows = (
            self._db.session.query(User.username, func.count(Idea.id).label("count"))
            .outerjoin(Idea, Idea._user_id == User.id)
            .group_by(User.id, User.username)
            .order_by(func.count(Idea.id).desc())
            .all()
        )
        total_ideas = self._db.session.query(func.count(Idea.id)).scalar() or 0
        total_votes = self._db.session.query(func.count(IdeaVote.id)).scalar() or 0
        engagement_rate = float(total_votes / total_ideas) if total_ideas else 0.0

        top_ideas_rows = (
            self._db.session.query(Idea._title, func.count(IdeaVote.id).label("votes"))
            .outerjoin(IdeaVote, IdeaVote._idea_id == Idea.id)
            .group_by(Idea.id, Idea._title)
            .order_by(func.count(IdeaVote.id).desc())
            .limit(5)
            .all()
        )
        return {
            "ideas_per_user": [{"username": r.username, "count": int(r.count)} for r in ideas_per_user_rows],
            "engagement_rate": engagement_rate,
            "avg_votes_per_idea": float(total_votes / total_ideas) if total_ideas else 0.0,
            "top_ideas": [{"title": r._title, "votes": int(r.votes)} for r in top_ideas_rows],
        }

    def get_dashboard_data(self) -> dict:
        return self.get_summary()
