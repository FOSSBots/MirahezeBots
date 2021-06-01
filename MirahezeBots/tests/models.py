"""SQL models for sopel database."""
import sys

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class NickNames(Base):
    """Model for 'nicknames' table."""

    __tablename__ = 'nicknames'
    plugin = Column(String, primary_key=True)
    key = Column(String, primary_key=True)
    value = Column(String)

    def __str__(self):
        """Return main output."""
        return f'{self.__tablename__} <{self.key}, {self.value}>'


class NickValues(Base):
    """Model for 'nick_values' table."""

    __tablename__ = 'nick_values'
    nick_id = Column(Integer, primary_key=True)
    key = Column(String, primary_key=True)
    value = Column(String)

    def __str__(self):
        """Return main output."""
        return NickNames.__str__(self)


class ChannelValues(Base):
    """Model for 'channel_values' table."""

    __tablename__ = 'channel_values'
    channel = Column(String, primary_key=True)
    key = Column(String, primary_key=True)
    value = Column(String)

    def __str__(self):
        """Return main output."""
        return NickNames.__str__(self)


class PluginValues(Base):
    """Model for 'plugin_values' table."""

    __tablename__ = 'plugin_values'
    plugin = Column(String, primary_key=True)
    key = Column(String, primary_key=True)
    value = Column(String)

    def __str__(self):
        """Return main output."""
        return NickNames.__str__(self)


class Welcome(Base):
    """Model for 'welcome' table."""

    __tablename__ = 'welcome'
    welcome_id = Column(Integer, primary_key=True)
    nick_id = Column(Integer)
    account = Column(String)
    channel = Column(String)
    timestamp = Column(String)
    message = Column(String)

    def __str__(self):
        """Return main output."""
        return Welcome.__str__(self)


if __name__ == '__main__':
    try:
        engine = create_engine(f'sqlite:///{sys.argv[1]}', echo=True)
    except IndexError:
        engine = create_engine('sqlite:///example-model.db', echo=True)
    Base.metadata.create_all(engine)
