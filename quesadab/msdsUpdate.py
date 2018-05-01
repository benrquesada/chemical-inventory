#!/usr/bin/python
 
import sqlite3
from sqlite3 import Error
 
 
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None
        
def update_chemicals(conn, task):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE chemicals
              SET sdsLink = ? 
              WHERE chemId = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)
    
def getSearchTerm(conn, chemId):
    """
    Query row in table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM chemicals WHERE chemId = ?", [chemId])
 
    rows = cur.fetchall()
    cas = rows[0]
    cas = cas[3]
    if isCas(cas) == False:
        return False
    else:
        cas = cas.strip()
        return cas

def isCas(cas):
    if type(cas) == unicode:
        cas = cas.strip()
        if len(cas) == 0:
            return False
        for i in cas:
            if i.isdigit() == True or i == "-":
                pass
            else:
                return False
        return True
    else:
        return False
 
def main():
    #Dev
    #database = "/home/ubuntu/workspace/new_workspace/ChemicalInventory/chemical-inventory-new/data/inventory.sqlite"
    
    #production
    database = "/var/www/html/chemical-inventory-new/data/inventory.sqlite"
    conn = create_connection(database)
    with conn:
        cId = 1
        while True:
            try:
                term = getSearchTerm(conn, cId)
                if term == False:
                    cId=cId+1
                else:
                    sdsLink = "https://msdsmanagement.msdsonline.com/af807f3c-b6be-4bd0-873b-f464c8378daa/ebinder/?SearchTerm="+term
                    print ("updated chemId "+str(cId)+" sdslink with "+sdsLink)
                    update_chemicals(conn, (sdsLink,cId))
                    cId=cId+1
            except IndexError:
                break
             
        
        
 
if __name__ == '__main__':
    main()