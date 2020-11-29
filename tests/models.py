import sys

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class NickNames(Base):
    __tablename__ = 'nicknames'
    plugin = Column(String, primary_key=True)
    key = Column(String, primary_key=True)
    value = Column(String)

    def __str__(self):
        return '%s <%s, %s>' % (self.__tablename__, self.key, self.value,)


class NickValues(Base):
    __tablename__ = 'nick_values'
    nick_id = Column(Integer, primary_key=True)
    key = Column(String, primary_key=True)
    value = Column(String)

    def __str__(self):
        return NickNames.__str__(self)


class ChannelValues(Base):
    __tablename__ = 'channel_values'
    channel = Column(String, primary_key=True)
    key = Column(String, primary_key=True)
    value = Column(String)

    def __str__(self):
        return NickNames.__str__(self)


class PluginValues(Base):
    __tablename__ = 'plugin_values'
    plugin = Column(String, primary_key=True)
    key = Column(String, primary_key=True)
    value = Column(String)

    def __str__(self):
        return NickNames.__str__(self)


class Welcome(Base):
    __tablename__ = 'welcome'
    welcome_id = Column(Integer, primary_key=True)
    nick_id = Column(Integer)
    account = Column(String)
    channel = Column(String)
    timestamp = Column(String)
    message = Column(String)

    def __str__(self):
        return Welcome.__str__(self)


if __name__ == '__main__':
    try:
        engine = create_engine('sqlite:///{0}'.format(sys.argv[1]), echo=True)
    except IndexError:
        print('argument not provided')
        engine = create_engine('sqlite:///example-model.db', echo=True)
    Base.metadata.create_all(engine)
