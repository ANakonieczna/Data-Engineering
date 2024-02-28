# Import libraries required for connecting to MySQL
import mysql.connector
# Import libraries required for connecting to PostgreSQL
import psycopg2

# Connect to MySQL
connection = mysql.connector.connect(user='root', password='***************',host='127.0.0.1',database='sales')
cursorMySQL = connection.cursor()

# Connect to PostgreSQL
dsn_hostname = '127.0.0.1'
dsn_user='postgres'
dsn_pwd ='***************'
dsn_port ="5432"
dsn_database ="postgres"
conn = psycopg2.connect(
   database=dsn_database,
   user=dsn_user,
   password=dsn_pwd,
   host=dsn_hostname,
   port= dsn_port
)
cursorPostgreSQL = conn.cursor()

# Find the last 'rowid' from the PostgreSQL data warehouse
# The function get_last_rowid must return the last 'rowid' of the table 'sales_data'

def get_last_rowid():
    SQL = "SELECT MAX(rowid) FROM sales_data"
    cursorPostgreSQL.execute(SQL)
    conn.commit()
    return [int(record[0]) for record in cursorPostgreSQL.fetchall()]

last_row_id = get_last_rowid()
print("Last row id on production datawarehouse = ", last_row_id)

# List all records in the MySQL database with 'rowid' greater than the one on the PostgreSQL data warehouse
# The function get_latest_records must return a list of all records 
# that have a 'rowid' greater than the last_row_id in the 'sales_data' table in the 'sales' database 
# on the MySQL staging data warehouse.

def get_latest_records(rowid):
    SQL = "SELECT * FROM sales_data"
    cursorMySQL.execute(SQL)
    new_rows = []
    for row in cursorMySQL.fetchall():
        if row[0] > int(rowid[0]):
            new_rows.append(row)
    return new_rows

new_records = get_latest_records(last_row_id)
print("New rows on staging datawarehouse = ", len(new_records))

# Insert the additional records from the MySQL database into the PostgreSQL data warehouse
# The function insert_records must insert all the records pass it into the 'sales_data' table in the PostgreSQL data warehouse

def insert_records(records):
    for row in records:
        SQL="INSERT INTO sales_data(rowid,product_id,customer_id,quantity) values(%s,%s,%s,%s)"
        cursorPostgreSQL.execute(SQL,row);
        conn.commit()

insert_records(new_records)
print("New rows inserted into production datawarehouse = ", len(new_records))

# Disconnect from the MySQL warehouse
connection.close()
# Disconnect from the PostgreSQL data warehouse 
conn.close()
# End of program