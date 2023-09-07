import subprocess
import sys


def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])


# Example
if __name__ == '__main__':

    try:
        import paho.mqtt.client as mqtt

        print('Pass! Take a break and drink something :)')


    except:
        install('paho-mqtt')
        print('Failed! Check "paho" package installation!')
import paho.mqtt.client as mqtt
import time
import random
import sqlite3
global click
global button_click
button_click = 1
def get_status_server_by_number(serverNumber):
    c.execute("SELECT * FROM serversData WHERE serverNumber=:serverNumber", {'serverNumber': serverNumber})
    return c.fetchone()

def update_serverData(serverNumber, open_close):
    with conn:
        c.execute("""UPDATE serversData SET open_close = :open_close WHERE serverNumber =:serverNumber""",{'serverNumber':serverNumber, 'open_close':open_close})

def get_status_sys_by_number(sysNumber):
    c2.execute("SELECT * FROM dryIceData WHERE sysNumber=:sysNumber", {'sysNumber': sysNumber})
    return c2.fetchone()

def update_sys(sysNumber, open_close):
    with conn2:
        c2.execute("""UPDATE dryIceData SET open_close = :open_close WHERE sysNumber =:sysNumber""",{'sysNumber':sysNumber, 'open_close':open_close})

# broker list
brokers=["iot.eclipse.org","broker.hivemq.com",\
         "test.mosquitto.org"]

broker=brokers[1]


def on_log(client, userdata, level, buf):
        print("log: "+buf)
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)
def on_disconnect(client, userdata, flags, rc=0):
        print("DisConnected result code "+str(rc))
def on_message(client,userdata,msg):
        topic=msg.topic
        m_decode=str(msg.payload.decode("utf-8","ignore"))
        print("message received: ",m_decode)
        msg_parse(m_decode)

def msg_parse(m_decode):
        print(m_decode) 
        global button_click
        global click
        subString="Temperature:" 
        if subString in m_decode:    
            rez=float(m_decode.split('Temperature: ')[1].split(' Humidity:')[0])
            print(rez) 
            if rez >= 21 :
                client.publish(pub_topic,"Servers are too hot - turn on cooling system")
                client.publish('IOT_PROJECT_Relay',"Dry-ice system turned on turbo-mode")
                conn2 = sqlite3.connect('serversData.db')
                c2=conn2.cursor()
                for serverNumber in range(20):
                    c2.execute("""UPDATE serversData SET open_close = :open_close WHERE serverNumber =:serverNumber""",{'serverNumber':serverNumber+1, 'open_close':'open'})
                    conn2.commit()
                time.sleep(3)
        elif "open" in m_decode:
            conn = sqlite3.connect('dryIceData.db')
            c=conn.cursor()
            c.execute("""UPDATE dryIceData SET open_close = :open_close WHERE sysNumber =:sysNumber""",{'sysNumber':21, 'open_close':'open'})
            conn.commit()
        elif "close" in m_decode:
            conn = sqlite3.connect('dryIceData.db')
            c=conn.cursor()
            c.execute("""UPDATE dryIceData SET open_close = :open_close WHERE sysNumber =:sysNumber""",{'sysNumber':21, 'open_close':'close'})
            conn.commit()
            
client = mqtt.Client("IOT_project", clean_session=True) # create new client instance

client.on_connect=on_connect  #bind call back function
client.on_disconnect=on_disconnect
client.on_log=on_log
client.on_message=on_message
print("Connecting to broker ",broker)
port=1883
client.connect(broker,port)     #connect to broker
pub_topic= 'IOT_PROJECT'



conn = sqlite3.connect('serversData.db')
conn2 = sqlite3.connect('dryIceData.db')
c=conn.cursor()
c2=conn2.cursor()
for serverNumber in range(12):
    if (get_status_server_by_number(serverNumber+1)[1] == "open"):
        client.publish(pub_topic," There is a open cooling system on server " + str(serverNumber+1)+" The system will close the cooling system")
        update_serverData(serverNumber+1, 'close')
        time.sleep(1.5)
        client.publish(pub_topic," The system closed the cooling system")
    else:
        client.publish(pub_topic, "The cooling system is currently offline on server " + str(serverNumber+1))
    time.sleep(1.5)
for sysNumber in range(4):
    
    if (get_status_sys_by_number(sysNumber+1)[1] == "open"):
        client.publish(pub_topic," Dry-ice machine " + str(sysNumber+1)+" is ON")
        update_sys(sysNumber+1, 'close')
        time.sleep(1.5)
        client.publish(pub_topic," The system closed the Dry-ice machine")
    else:
        client.publish(pub_topic, " Dry-ice machine " + str(sysNumber+1) + " is OFF")

    time.sleep(1.5)
client.publish(pub_topic, "The scan is finished and all the cooling systems and Dry-ice machines are closed ")
client.loop_start()
client.subscribe("IOT_PROJECT")
time.sleep(300)
client.loop_stop()

client.disconnect() # disconnect
print("End publish_client run script")






