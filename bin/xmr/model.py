from sqlalchemy import (MetaData, Table, join, Column, Integer, Boolean,
                        String, DateTime, Float, ForeignKey, and_)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import column_property
from datetime import datetime
from database import engine
from database import Base


class ExtendMixin(object):

    def as_dict(self):
        return


class Author(ExtendMixin, Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)


library_map_package = Table('library_map_package', Base.metadata,
    Column('library_id', Integer, ForeignKey('library.id')),
    Column('map_package_id', Integer, ForeignKey('map_package.id'))
)


class Library(ExtendMixin, Base):
    __tablename__ = 'library'
    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    maps = relationship("MapPackage", secondary=library_map_package, backref="parents")


map_package_bsp = Table('map_package_bsp', Base.metadata,
    Column('map_package_id', Integer, ForeignKey('library.id')),
    Column('bsp_id', Integer, ForeignKey('bsp.id'))
)


class MapPackage(ExtendMixin, Base):
    __tablename__ = 'map_package'
    id = Column(Integer, primary_key=True)
    pk3_file = Column(String(255))
    shasum = Column(String(64))
    bsp = relationship("Bsp", secondary=map_package_bsp, backref="parents")
    date = Column(DateTime, nullable=False, default=datetime.now())
    filesize = Column(Integer)


class Bsp(ExtendMixin, Base):
    __tablename__ = 'bsp'
    id = Column(Integer, primary_key=True)
    pk3_file = Column(String(255))
    bsp_name = Column(String(255))
    bsp_file = Column(String(255))
    map_file = Column(String(255))
    mapshot = Column(String(255))
    radar = Column(String(255))
    title = Column(String(255))
    description = Column(String(600))
    mapinfo = Column(String(255))
    author = Column(String(100))
    entities_file = Column(String(255))
    waypoints = Column(Boolean)
    license = Column(Boolean)


bsp_gametype = Table('bsp_gametype', Base.metadata,
    Column('bsp_id', Integer, ForeignKey('bsp.id')),
    Column('gametype_id', Integer, ForeignKey('gametype.id'))
)

bsp_entity = Table('bsp_entity', Base.metadata,
    Column('bsp_id', Integer, ForeignKey('bsp.id')),
    Column('entity_id', Integer, ForeignKey('entity.id'))
)


class Gametype(ExtendMixin, Base):
    __tablename__ = 'gametype'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))


class Entity(ExtendMixin, Base):
    __tablename__ = 'entity'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))


Base.metadata.create_all(engine)
