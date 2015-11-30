import datetime
import ujson as json

from peewee import *

from app import database

class BaseModel(Model):
    class Meta:
        database = database


class Message(BaseModel):                              
    timestamp = DateTimeField()                        
    epoch_milli = IntegerField()                       
    recv = DateTimeField(default=datetime.datetime.now)
                                                       
    class Meta:                                        
        order_by = ('-recv',)                          
                                                       
class Host(BaseModel):                                 
    name = CharField(unique=True)                      
                                                       
# the user model specifies its fields (or columns) decl
class CPUStats(Message):                               
    hostname = ForeignKeyField(Host)                   
    load_1 = FloatField()                              
    load_5 = FloatField()                              
    load_15 = FloatField()                             
    CPU = TextField()                                  

def create_tables():
    database.connect()
    database.create_tables([Host, CPUStats], safe=False)


