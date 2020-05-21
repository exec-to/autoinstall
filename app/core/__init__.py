# -*- coding: UTF-8 -*-
from app import config
import sqlalchemy as db
from sqlalchemy import Table, Column, Integer, String, MetaData, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import mapper
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

# Сервер
class Server(Base):
    __tablename__ = 'servers'
    id = Column('id', Integer, primary_key=True)
    adman_id = Column(Integer, nullable=False)
    # api_key = Column(String(40), nullable=True)
    maintenance = Column(Boolean, default=False)

    def __init__(self, adman_id):
        self.adman_id = adman_id

# MAC-адреса сервера
class MacTable(Base):
    __tablename__ = 'mac_addr'
    id = Column('id', Integer, primary_key=True)
    server_id = Column(Integer, nullable=False)
    mac_addr = Column(String(20), nullable=False)

    def __init__(self, server_id, mac_addr):
        self.server_id = server_id
        self.mac_addr = mac_addr

class Install(Base):
    __tablename__ = 'installs'
    id = Column('id', Integer, primary_key=True)
    adman_id = Column(Integer, nullable=False)
    os = Column(String(20), nullable=False)
    osver = Column(String(20), nullable=False)
    token = Column(String(32), nullable=False)
    ipaddr = Column(String(32), nullable=False)
    # passwdhash = Column(String(128), nullable=False) # mkpasswd -m sha-512 'пароль'
    status = Column(Integer, default=0)
    # 0 - устанавливается, 1 - завершена, 2 - отменена, 3 - запуск установки (для Windows)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    diskpart = Column(Integer, nullable=False, default=0)

    def __init__(self, adman_id, os, osver, token, ipaddr, diskpart):
        self.adman_id = adman_id
        self.os = os
        self.osver = osver
        self.token = token
        self.ipaddr = ipaddr
        # self.passwdhash = passwdhash
        self.diskpart = diskpart


class Core:
    def __init__(self):
        self.engine = db.create_engine(
            'mysql+mysqlconnector://{user}:{passwd}@{host}:{port}/{db}'
            .format_map(config.database),
            echo=False,
            connect_args={'connect_timeout': 3600},
	    pool_recycle=300
        )

        Base.metadata.create_all(self.engine)
