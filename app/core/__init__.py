# -*- coding: UTF-8 -*-
from app import config
import sqlalchemy as db
from sqlalchemy import Table, Column, Integer, String, MetaData, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import mapper
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Сервер
class Server(Base):
    __tablename__ = 'servers'
    id = Column('id', Integer, primary_key=True)
    adman_id = Column(Integer, nullable=False)
    api_key = Column(String(40), nullable=True)
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


# class InstallProcess(Base):
#     __tablename__ = 'installations'
#     id = Column('id', Integer, primary_key=True)
#     # status
#     # start time
#     # token
#     # OS
#     # Disk partitioning
#     # IP-addr
#     #
#     server_id = Column(Integer, nullable=False)
#     # mac_addr = Column(String(20), nullable=False)
#
# class Networks(Base):
#     __tablename__ = 'networks'
#     id = Column('id', Integer, primary_key=True)
#     subnet = Column(String(20), nullable=False) # 192.168.0.0
#     netmask = Column(String(20), nullable=False)
#     gateway = Column(String(20), nullable=False)

class Core:
    def __init__(self):
        self.engine = db.create_engine(
            'mysql+mysqlconnector://{user}:{passwd}@{host}:{port}/{db}'
            .format_map(config.database),
            echo=False,
            connect_args={'connect_timeout': 10}
        )

        Base.metadata.create_all(self.engine)
