from datetime import datetime

from sqlalchemy import Column, Boolean, Integer, String

from database import Base


class GoalEvent(Base):
    __tablename__ = 'goal_events'

    id = Column(Integer, primary_key=True)
    team = Column(Integer, nullable=False)
    timestamp = Column(Integer, nullable=False)

    def serialize(self):
        return {
            key: getattr(self, key)
            for key in ('id', 'team', 'timestamp')
        }


class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    score_red = Column(Integer, nullable=False)
    score_blue = Column(Integer, nullable=False)

    # TODO: move teams into another table, as a relationship
    team_red = Column(String(60), nullable=False)
    team_blue = Column(String(60), nullable=False)

    max_goals = Column(Integer, nullable=False, default=10)
    paused = Column(Boolean, default=False)
    start = Column(Integer, nullable=False)
    end = Column(Integer)
    last_duration = Column(Integer)

    def serialize(self):
        body = {
            key: getattr(self, key)
            for key in (
                'id', 'name', 'score_blue', 'score_red', 'team_blue',
                'team_red', 'max_goals', 'paused'
            )
        }
        body.update({'start': str(datetime.fromtimestamp(self.start))})
        if self.end is not None:
            body.update({'end': str(datetime.fromtimestamp(self.end))})
        return body
