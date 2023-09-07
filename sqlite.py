import sqlite3
import random


conn = sqlite3.connect('serversData.db')
conn2 = sqlite3.connect('dryIceData.db')
c=conn.cursor()
c2=conn2.cursor()

c.execute("""CREATE TABLE serversData (
          serverNumber integer,
          open_close text
           )""")

c2.execute("""CREATE TABLE dryIceData (
           sysNumber integer,
           open_close text
           )""")
conn.commit()
conn2.commit()


def insert_server(serverNumber, open_close):
    with conn:
        c.execute("INSERT INTO serversData VALUES (:serverNumber, :open_close)",{'serverNumber':serverNumber, 'open_close':open_close})

def get_server_status_by_number(serverNumber):
    c.execute("SELECT * FROM serversData WHERE serverNumber=:serverNumber", {'serverNumber': serverNumber})
    return c.fetchall()

def insertSys(sysNumber, open_close):
    with conn2:
        c2.execute("INSERT INTO dryIceData VALUES (:sysNumber, :open_close)",{'sysNumber':sysNumber, 'open_close':open_close})

def update_window(sysNumber, open_close):
    with conn2:
        c2.execute("""UPDATE from dryIceData SET open_close = :open_close WHERE sysNumber =:sysNumber""",{'sysNumber':sysNumber, 'open_close':open_close})

def get_sys_status_by_number(sysNumber):
    c.execute("SELECT * FROM dryIceData WHERE sysNumber=:sysNumber", {'sysNumber': sysNumber})
    return c.fetchall()

for x in range(21):
    
    mylist1 = ['open', 'close']
    insert_server(x+1,random.choice(mylist1)) 
    insertSys(x+1,random.choice(mylist1)) 
    
conn.close()
conn2.close()