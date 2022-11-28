import sqlalchemy as db
from sqlalchemy import create_engine, Column, String, Table, Integer, Float, DateTime
from sqlalchemy.orm import Session, sessionmaker, declarative_base
import urllib.parse
import sys, random, os, uuid
import datetime

Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'
    accountId = Column(String(255), primary_key=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
    username = Column(String(255))

class Player(Base):
    __tablename__ = 'players'
    playerId = Column(String(255), primary_key=True)
    firstname = Column(String(255))
    lastname = Column(String(255))
    age = Column(Integer)
    gender = Column(String(255))
    skillLevel = Column(Float)

class Tournament(Base):
    __tablename__ = 'tournaments'
    tournamentId = Column(String(255), primary_key=True)
    tournamentName = Column(String(255))
    city = Column(String(255))
    requiredLevel = Column(Float)
    size = Column(Integer)

class SparringSession(Base):
    __tablename__ = 'sparringSessions'
    sessionId = Column(String(255), primary_key=True)
    requester = Column(String(255))
    responder = Column(String(255))
    city = Column(String(255))
    dateAndTime = Column(DateTime)
    requiredLevel = Column(Float)

class TournamentPlayers(Base):
    __tablename__ = 'tournamentPlayers'
    tourneyPlayerId = Column(String(255), primary_key=True)
    tourneyId = Column(String(255))