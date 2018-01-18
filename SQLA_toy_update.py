#toy example to work with SQLAlchemy updates
from sqlalchemy import update
#connect to SQLite DB w/ SQLAlchemy ORM:
from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo = False)

#NOW DEFINE DB SCHEMA (THIS DOESN'T WRITE SCHEMA TO DB, JUST TO SQLALCHEMY CLASSES AND OBJECTS)
#define an SQLAlchemy base class to maintain catalog of classes and tables relative to this base
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

#use the base class to define mapped classes in terms of it:
from sqlalchemy import Column, Integer, String
# from sqlalchemy import Sequence
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship #http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#relationship-pattern
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,  primary_key=True)
    firstname = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))

    def __repr__(self): #used in query function to return values of queried fields
        return "<User(id='%s', firstname='%s', fullname='%s', password='%s')>" % (
                                self.id, self.firstname, self.fullname, self.password)

#NOW WRITE SCHEMA TO DB (THIS WRITES TO SQLITE DB):
Base.metadata.create_all(engine) #build DB schema from Base objects

#NOW WRITE DATA TO DB. YOU NEED A SESSION OBJECT TO DO SO:
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine) #define Session class, which is a factory for making session objects (poor naming choice, in my opinion - why the do it this way??!)
session = Session() #make a session
#now insert data using various insert methods:
ed_user = User(firstname='ed', fullname='Ed Jones', password='edspassword') #single insert to User table. pass the record to object ed_user
session.add(ed_user) # add record held in object to the DB - but only as a temp. item (it's not yet comitted)
session.add_all([ #insert multiple records to User table
    User(firstname='wendy', fullname='Wendy Williams', password='foobar'),
    User(firstname='mary', fullname='Mary Contrary', password='xxg527'),
    User(firstname='fred', fullname='Fred Thompson', password='blah')])
#insert to User table using dictionary object
mydict = {'firstname':'jake', 'fullname':'jake tonda', 'password': 'jagd'}
session.add(User(**mydict))
session.commit() #commit all pending transactions to DB

#update wendy's fullname:
#setup table and column objects we'll need:
myTable = Base.metadata.tables['users'] #get User table from SQLAlchemy metadata handler
myCol =  myTable.c['firstname'] #get the column called 'name'

#print results before update
for rec in session.query(myTable).filter(myCol == 'wendy'): #query using column object. get record: WHERE firstname == 'wendy'
    print (rec)

u=update(myTable) #build a SQLAlchemy updater object
u=u.values({'fullname': 'Wendy Aldddmon'}) #define updater w/ values to update
u=u.where(myCol == 'wendy') #define updater w/ the update where clause (updete where firstname == 'wendy')
session.execute(u)
session.commit()
#print wendy's updated result:
for rec in session.query(myTable).filter(myCol == 'wendy'):
    print (rec)
