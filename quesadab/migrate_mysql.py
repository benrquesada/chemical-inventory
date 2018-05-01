import argparse
from application import app
from application.models.buildingsModel import *
from application.models.chemicalsModel import *
from application.models.containersModel import *
from application.models.floorsModel import *
from application.models.historiesModel import *
from application.models.rolesModel import *
from application.models.roomsModel import *
from application.models.usersModel import *
from application.models.storagesModel import *
from application.models.wasteContainersModel import *
from application.models.wasteChemicalsModel import *
from application.models.wasteContentsModel import *

def create_tables(db, tables):
    for table in tables:
        db.create_table(table)

def clone_entries(db, tables):
    for table in tables:
        print("-------------%s----------" % (str(table)))
        entries = table.select()
        entries = list(entries)
	old_db = table._meta.database
        table._meta.database = db
        for entry in entries:
            try:
                table.create(**entry._data)
            except Exception as e:
                print(e)
                print(entry._data)
        table._meta.database = old_db

def migrate(user, password, db, host):
    tables = [Buildings, Chemicals, Floors,Rooms,Users,Storages,Containers, Histories, Wastecontainers, Wastechemicals, Wastecontents]
    mysql = MySQLDatabase(db, host=host,password=password,user=user)
    create_tables(mysql, tables)
    clone_entries(mysql, tables)





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Move Sqlite Data to MySQL DB')
    parser.add_argument('--user',required=True, help='Username for MySQL')
    parser.add_argument('--password', required=True, help="Password for MySQL")
    parser.add_argument('--db',required=True, help='Database for MySQL')
    parser.add_argument('--host', required=True, help="host for MySQL")
    args = parser.parse_args()

    migrate(args.user, args.password, args.db, args.host)

    #python migrate_mysql.py --user cas --password CasIsThePassword123! --host localhost --db cas >>log.txt
