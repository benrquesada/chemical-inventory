from application.config import *
from application.absolutepath import getAbsolutePath
from peewee import *

def getDB (dbName, dbType):
#choose which database to use
  dbtype = "sqlite"

  if dbtype == "mysql":

      #This changes based on what dtabase you set up in MYSQL
      theDB = MySQLDatabase('chemical', user='root', password='root',
                             host='localhost', port=3306)

  else:
      dbPath = config.databases[dbType][dbName].filename
      dbPath = getAbsolutePath(dbPath)
      theDB = SqliteDatabase (dbPath,
                              pragmas = ( ('busy_timeout',  100),
                                          ('journal_mode', 'WAL')
                                      ),
                              threadlocals = True)




  config.databases[dbType][dbName].theDB = theDB
  return theDB
