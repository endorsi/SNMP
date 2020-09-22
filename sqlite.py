import sqlite3

conn = sqlite3.connect("snmp.db")
c = conn.cursor()


conn.execute('''CREATE TABLE RESPONDS
         (
          NUM           integer PRIMARY KEY, 
          ID            TEXT, 
          OID           TEXT  ,
          IP            TEXT  ,
          RESPOND       TEXT    
          )''')


with conn:
    c.execute("INSERT INTO RESPONDS VALUES (1,'valencia123','.1.2.3.4.5.6','10.20.40.60','676-utf8')")
conn.close()
