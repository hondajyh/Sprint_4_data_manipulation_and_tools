#DEMONSTRATE A MANY TO MANY RELATIONSHIP BETWEEN 2 TABLES:
#run thru sqlalchemy.org's tutorial: http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
#connect to SQLite DB w/ SQLAlchemy ORM:
from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo = False)


#NOW DEFINE DB SCHEMA (THIS DOESN'T WRITE SCHEMA TO DB, JUST TO SQLALCHEMY CLASSES AND OBJECTS)
#define an SQLAlchemy base class to maintain catalog of classes and tables relative to this base
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

#use the base class to define mapped classes in terms of it:
#as an initial example, define a table called 'users' by defining a class called 'User'
from sqlalchemy import Column, Integer, String
# from sqlalchemy import Sequence
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship #http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#relationship-patterns

# Column(Integer, Sequence('user_id_seq'), primary_key=True)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,  primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))
    #sets up 1 to many relationship between 1 user and many addresses
    #define relationship in both tables so that elements added in one direction automatically become visible in the other direction. This behavior occurs based on attribute on-change events and is evaluated in Python, without using any SQL:
    addresses = relationship("Address", back_populates = "user") #addresses is a collection that holds related Address class objects

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
                                self.name, self.fullname, self.password)

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    #sets up many to 1 relationship between 1 user and many addresses
    #define relationship in both tables so that elements added in one direction automatically become visible in the other direction. This behavior occurs based on attribute on-change events and is evaluated in Python, without using any SQL:
    user = relationship("User", back_populates="addresses") #stores the related user class object

    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address


#NOW WRITE SCHEMA TO DB (THIS WRITES TO SQLITE DB):
Base.metadata.create_all(engine) #build DB schema from Base objects

#NOW WRITE DATA TO DB. YOU NEED A SESSION OBJECT TO DO SO:
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine) #define Session class, which is a factory for making session objects (poor naming choice, in my opinion - why the do it this way??!)
session = Session() #make a session
ed_user = User(name='ed', fullname='Ed Jones', password='edspassword') #make a record
session.add(ed_user) # add  record held in object to the DB - but only as a temp. item (it's not yet comitted)
session.add_all([
    User(name='wendy', fullname='Wendy Williams', password='foobar'),
    User(name='mary', fullname='Mary Contrary', password='xxg527'),
    User(name='fred', fullname='Fred Flinstone', password='blah')])
session.commit() #commit all pending transactions to DB


#NOW DO SOME QUERYING:
for name, in session.query(User.name).filter(User.fullname=='Ed Jones'):
    print(name)

for instance in session.query(User).order_by(User.id): #session.query() <--a SQLAlchemy Query object!
    print(instance.name, instance.fullname)

#PLAYING W/ RELATIONSHIPS:
jack = User(name='jack', fullname='Jack Bean', password='gjffdd')
jack.addresses #no associated addresses yet. so addresses relationship collection returnes empty

jack.addresses = [#insert some addresses
    Address(email_address='jack@google.com'),
    Address(email_address='j25@yahoo.com')]

jack.addresses #now that we added addresses associated w/ jack, relationship collectdion returns non-empty
#write jack to DB:
session.add(jack)
session.commit()

#do a join type query:
for rec in session.query(User.fullname, Address.email_address).filter(User.name == 'jack'):
    print (rec)
