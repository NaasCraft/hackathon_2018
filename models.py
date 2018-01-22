from sqlalchemy import Column, Integer, String

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
    team_red = Column(String(60), nullable=False)
    team_blue = Column(String(60), nullable=False)
    max_goals = Column(Integer, nullable=False)

    def serialize(self):
        return {
            key: getattr(self, key)
            for key in (
                'id', 'name', 'score_blue', 'score_red', 'team_blue',
                'team_red', 'max_goals'
            )
        }
