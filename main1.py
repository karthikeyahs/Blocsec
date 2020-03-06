# run on your system
# new file
#test

import socket
import requests
import threading
import json
import datetime
import time
import netifaces as ni
import random
import pymongo
import hashlib
from blockchain import Blockchain
 
ip = "http://192.168.43.168:5000"

page = "/ul"
login_p = '/logi'
logout_p = '/logout'
data = {
    'num' : '1'
}


sport = 0
ssockets = []
 
lap = [12340,12341,12342,12344,12345,12346,12347]
 
user_count = len(lap)

message_queue=[]

# Login
def login(user):
    d = {
        'uname' : user
    }
    r = requests.post(url = ip+login_p, data = d)
 
def logout():
    r = requests.post(url = ip+logout_p,data={'luname':myuname})
 
 
def get_active_users():
    r = requests.post(url = ip+page, data = data)
    user_list = r.text.split()
    return user_list
 
def handle_transaction(msg):
    send_all(blockchain.new_transaction(msg['sender'],msg['receiver'],msg['message'])[1])

def handle_randnum(msg):
    blockchain.update_transactions(msg)

def handle_block(block_received):
    pass


def handle_msg(msg):
    try:
        if(msg['msg-type']=='transaction'):
            handle_transaction(msg)
        elif(msg['msg-type']=='random_number'):
            handle_randnum(msg)
        elif(msg['msg-type']=='block'):
            handle_block(msg)
    except Exception as e:
        print(e)

def dl():
    print('dl is created')
    port=5001
    sdl = socket.socket()
    sdl.bind(('',port))
    sdl.listen(5)
    while(True):
        c,addr = sdl.accept()
        hval='hey'
        hval=json.dumps(hval).encode('utf-8')
        c.send(hval)
        nt = json.loads(c.recv(1024).decode('utf-8'))
        print('received transaction from html')
        temp=blockchain.new_transaction(nt['sender'],nt['receiver'],nt['message'])
        send_all(temp[0])
        send_all(temp[1])        
        c.close()


def socket_listen(soc, port):
    print(port)
    soc.bind(('', port))
    soc.listen()
 
    while True:
        c, addr = soc.accept()
        val='connected'
        val=json.dumps(val).encode('utf-8')
        c.send(val)
        msg = c.recv(1024)
        msg=json.loads(msg.decode('utf-8'))
        val='received'
        val=json.dumps(val).encode('utf-8')
        c.send(val)
        handle_msg(msg)
        print(msg)
        c.close()


def init():
    global sport,me,myuname
    myuname=str(input("Enter username : "))
    login(myuname)
    global ssockets
    ssockets = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in range(user_count)]
 
    sport = lap[len(get_active_users())-1]
    me = str(ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr'])
    print(me)
    print(sport)
    
    c1 = -1
    for soc in ssockets:
        c1 += 1
        if(lap[c1] == sport): 
            continue
        threading.Thread(target = socket_listen,args = (soc, lap[c1])).start()

    threading.Thread(target=dl).start()
    threading.Thread(target=b_send_msg).start()
    global blockchain
    blockchain = Blockchain()
    
def send_msg(msg,sip):
    global message_queue
    message_queue.append([msg,sip])

def b_send_msg():
    global message_queue
    while(True):
        if(len(message_queue)!=0):
            m1=message_queue.remove()
            a_send_msg(m1[0],m1[1])


def a_send_msg(msg,sip):
    if(msg=='close'):
        cclose()
 
    if(msg == 'logout'):
        logout()
    
    soc = socket.socket()
    print('portszz')
    print(sip)
    print(sport)
    soc.connect((sip,sport))

    print(json.loads(soc.recv(1024).decode('utf-8')))
    msg=json.dumps(msg).encode('utf-8')
    soc.send(msg)
    rs=json.loads(soc.recv(1024).decode('utf-8'))
    print(rs)
    soc.close()
    return rs

def send_all(msg):
    ul1=get_active_users()
    rsl=[]
    for us in ul1:
        if(us != me):
            print(us,me)
            rsl.append(send_msg(msg,us))
    return rsl

def cclose():
    for s in ssockets:
        s.close()



init()