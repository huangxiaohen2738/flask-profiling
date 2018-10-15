from sqlalchemy import Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Numeric


base = declarative_base()


class Measurements(base):
    __tablename__ = 'flask_profiling_measurements'

    id = Column(Integer, primary_key=True)
    startedAt = Column(Numeric)
    endedAt = Column(Numeric)
    elapsed = Column(Numeric)
    method = Column(Text)
    args = Column(Text)
    kwargs = Column(Text)
    name = Column(Text)
    context = Column(Text)

    def to_dict(self):
        return {
            "id": self.id,
            "startedAt": self.startedAt,
            "endedAt": self.endedAt,
            "elapsed": self.elapsed,
            "method": self.method,
            "args": self.args,
            "kwargs": self.kwargs,
            "name": self.name,
            "context": self.context
        }
