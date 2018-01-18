#import csv to database. csv can only contain columns from one table.
# importCSV function is a solution assumes that csv contains columns w/ headers FieldName
#  header format corresponds to name of the table field that column data should be imported to.
#  you will pass table name into the importCSV function.

#connect to SQLite DB w/ SQLAlchemy ORM:
from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo = False)

#NOW DEFINE DB SCHEMA (THIS DOESN'T WRITE SCHEMA TO DB, JUST TO SQLALCHEMY CLASSES AND OBJECTS)
#define an SQLAlchemy base class to maintain catalog of classes and tables relative to this base
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

#use the base class to define mapped classes in terms of it:
#as an initial example, define a table called 'users' by defining a class called 'User'. Field names corresponds to csv file header names
from sqlalchemy import Column, Integer, String
# from sqlalchemy import Sequence
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship #http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#relationship-patterns    

from sqlalchemy import update

class People(Base):
    __tablename__ = 'people'
    id = Column(Integer,  primary_key=True)
    name = Column(String(50))
    ssn = Column(String(50))
    age = Column(Integer)

    def __repr__(self):
        return "<People(name='%s', ssn='%s', age='%s')>" % (
                                self.name, self.ssn, self.age)

#NOW WRITE SCHEMA TO DB (THIS WRITES TO SQLITE DB):
Base.metadata.create_all(engine) #build DB schema from Base objects

#NOW WRITE DATA TO DB. YOU NEED A SESSION OBJECT TO DO SO:
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine) #define Session class, which is a factory for making session objects (poor naming choice, in my opinion - why the do it this way??!)
session = Session() #make a session

def importCSV(csvPath, import2Table):
    import csv
    myTable = Base.metadata.tables[import2Table] #get table
    with open(csvPath, 'rt', encoding='utf-8-sig') as csvfile:
        csvreader = csv.reader(csvfile,dialect='excel')
            #also assume all header names match table field names
        headers = next(csvreader) #read csv headers to list
        #for each row, make a dictionary object of each column header:value pair (list comprehension of a dictionary comprehension)
        myRecDictLS = [{aheader:avalue for aheader, avalue in zip(headers,row)} for row in csvreader]
        print (myRecDictLS)
    session.execute(myTable.insert(),myRecDictLS)    #insert records into table
    session.commit()


importCSV('1_table_input.csv', 'people')

for rec in session.query(People):
    print (rec)
