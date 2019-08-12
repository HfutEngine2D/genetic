import sqlite3

class DbHandler():
  __data_name = ''

  def __init__(self, name):
    self.__data_name = name
    self.open()

  def open(self):
    self.__conn = sqlite3.connect(self.__data_name)
    self.__c = self.__conn.cursor()

  def close(self):
    self.__conn.commit()
    self.__conn.close()

  def Create(self):
    print(self.__data_name)
    self.__c.execute('create table Chromosome (Vkey varchar(20) primary key, Vvalue varchar(20), paramStr varchar(50))')

  def list_chromosome(self):
    list_return = []
    cursor = self.__c.execute('select * from Chromosome')
    for row in cursor:
      list_return.append(row)
    return list_return

  def insert(self, Vkey, Vvalue, changStr):
    self.__c.execute('insert into Chromosome (Vkey, Vvalue, paramStr) values (\'{}\', \'{}\', \'{}\')'
          .format(Vkey,Vvalue,changStr))
