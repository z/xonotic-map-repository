from sqlalchemy import (MetaData, Table, join, Column, Integer, Boolean,
                        String, DateTime, Float, ForeignKey, and_)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import column_property
from sqlalchemy import UniqueConstraint
from datetime import datetime
from xmr.database import engine
from xmr.database import Base


class ExtendMixin(object):

    def as_dict(self):
        return


class Author(ExtendMixin, Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)


class Library(ExtendMixin, Base):
    __tablename__ = 'library'
    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    map_package_id = Column(ForeignKey('map_package.id'))
    map_package = relationship("MapPackage", foreign_keys=[map_package_id])

    __table_args__ = (UniqueConstraint('name', name='uix_library_name'),)


class MapPackage(ExtendMixin, Base):
    __tablename__ = 'map_package'
    id = Column(Integer, primary_key=True)
    pk3_file = Column(String(255))
    shasum = Column(String(64))
    bsp_id = Column(ForeignKey('bsp.id'))
    bsp = relationship("Bsp", foreign_keys=[bsp_id])
    date = Column(DateTime, nullable=False, default=datetime.now())
    filesize = Column(Integer)

    __table_args__ = (UniqueConstraint('pk3_file', name='uix_pk3_file'),)


class Bsp(ExtendMixin, Base):
    __tablename__ = 'bsp'
    id = Column(Integer, primary_key=True)
    map_package_id = Column(Integer, ForeignKey('map_package.id'))
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
    gametype_id = Column(ForeignKey('gametype.id'))
    gametype = relationship("Gametype", foreign_keys=[gametype_id])
    entity_id = Column(ForeignKey('entity.id'))
    entity = relationship("Entity", foreign_keys=[entity_id])
    entities_file = Column(String(255))
    waypoints = Column(Boolean)
    license = Column(Boolean)

    #bsp = relationship("MapPackage", backref="bsp")


class Gametype(ExtendMixin, Base):
    __tablename__ = 'gametype'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    __table_args__ = (UniqueConstraint('name', name='uix_gametype'),)


class Entity(ExtendMixin, Base):
    __tablename__ = 'entity'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    __table_args__ = (UniqueConstraint('name', name='uix_entity'),)

