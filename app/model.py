from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, Table
from sqlalchemy.orm import relationship, backref

from sqlalchemy_utils import UUIDType, PhoneNumberType, EmailType, ArrowType


from main import db

person_group_map = Table(
    'person_group_map',
    db.Model.metadata,
    Column('group_id', UUIDType, ForeignKey('group.id')),
    Column('person_id', UUIDType, ForeignKey('person.id')),
)

class Person(db.Model):
    __tablename__ = 'person'

    id = Column(UUIDType, primary_key=True, unique=True, nullable=False)
    name = Column(String, nullable=False)
    room = Column(String)
    phone = Column(PhoneNumberType)
    email = Column(EmailType)
    # Koblet opp mot LDAP bruker?
    # App som viser hvor man er forventet å møte når?

    groups = relationship('Group', secondary=person_group_map, backref='people')
    scans = relationship('Scan', back_populates='person')

class Group(db.Model):
    __tablename__ = 'group'
    id = Column(UUIDType, primary_key=True, unique=True, nullable=False)
    name = Column(String, nullable=False) # "Teknologi"
    #people =

class Location(db.Model):
    __tablename__ = 'location'
    id = Column(UUIDType, primary_key=True, unique=True, nullable=False)
    name = Column(String, nullable=False) # "Teknologi"
    #uuid = "3452345-542-234-52344-5-45"
    #key = "FBSADF==" # public key
    #name = "Konferanserommet"
    events = relationship('Event', back_populates='location')
    scans = relationship('Scan', back_populates='location')


event_group_map = Table(
    'event_group_map',
    db.Model.metadata,
    Column('group_id', UUIDType, ForeignKey('group.id')),
    Column('event_id', UUIDType, ForeignKey('event.id')),
)

class Event(db.Model):
    __tablename__ = 'event'
    id = Column(UUIDType, primary_key=True, unique=True, nullable=False)
    name = Column(String, nullable=False) # "SKAP Talk"
    start = Column(ArrowType, nullable=False)
    end = Column(ArrowType, nullable=False)

    groups = relationship('Group', secondary=event_group_map, backref='events')

    location_id = Column(UUIDType, ForeignKey('location.id'))
    location = relationship('Location', back_populates='events')

class Scan(db.Model):
    __tablename__ = "scan"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    time = Column(ArrowType, nullable=False)

    person_id = Column(UUIDType, ForeignKey('person.id'))
    person = relationship('Person', back_populates='scans')

    location_id = Column(UUIDType, ForeignKey('location.id'))
    location = relationship('Location', back_populates='scans')



db.create_all()
