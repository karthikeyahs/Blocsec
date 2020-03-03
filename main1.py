# run on your system
# new file
#test

import socket
import requests
import threading
import json
import datetime
import time
from trpool import Pool
import netifaces as ni
import random
 
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

transactionPool = Pool()
purePool = Pool()

node_state=0
listen_for_transactions_done=0

poet = []

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
    if(node_state==0 or node_state==1):
        transactionPool.add(msg)

def handle_randnum(msg):
    poet.append(msg['random-number'])

def handle_msg(msg):
    try:
        if(msg['msg-type']=='transaction'):
            handle_transaction(msg)
        elif(msg['msg-type']=='random_number'):
            handle_randnum(msg)
    except Exception as e:
        print(e)

def f1():
    pass

def sink():
    r=requests.get(url=ip+'/curd')
    print(r.text)
    s1=r.text
    d1=datetime.datetime(int(s1[:4]),int(s1[5:7]),int(s1[8:10]),int(s1[11:13]),int(s1[14:16]),int(s1[17:19]))
    print(str(d1))
    peri=10-int(d1.strftime('%S'))%10
    print(peri)
    # threading.Timer(peri,f1).start()
    time.sleep(peri)

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
        t = threading.Thread(target = socket_listen,args = (soc, lap[c1]))
        t.start()
    
    global blockchain
    blockchain = Blockchain()
    
 
def send_msg(msg,sip):
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

class Blockchain:
    def __init__(self):
        self.transactions = []
        self.state = 0
        self.chain = []

    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            # Check that the hash of the block is correct
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False
            last_block = block
            current_index += 1

        return True

    def new_transaction(self, sender, recipient, message):
        ts = str(datetime.datetime.now())
        tr={
                'sender': sender,
                'recipient': recipient,
                'message': message,
                'msg-type': 'transaction',
                'timestamp': ts,
        }
        purePool.add(tr)

def wait_for():
    if(node_state==0):
        time.sleep(5)
        listen_for_transactions_done=1
    elif(node_state==1):
        time.sleep(2)
    else:
        time.sleep(3)

def listen_for_transactions():
    node_state=0
    listen_for_transactions_done=0
    t=threading.Thread(target=wait_for)
    t.start()
    while(True):
        transaction1=purePool.remove()
        if(listen_for_transactions_done==1):
            break
        elif(transaction1==None):
            continue
        transactionPool.add(transaction1)
        send_all(transaction1)
    print('listening for transactions')

def complete_listen():
    node_state=1
    t=threading.Thread(target=wait_for)
    t.start()
    print('Buffer period')

def consensus():
    node_state=2
    # I think the below thread is not required. Here, i generate a random number and send it to all and 
    # wait for 3 seconds to receive all numbers.
    t=threading.Thread(target=wait_for)
    t.start()
    random_num = random.random()
    poet.append(random_num)
    cons = {
        'msg-type': 'random_number',
        'random-number': random_num,
    }
    send_all(cons)
    # After sending your number, wait for 3 seconds to receive a random number from every other node as 
    # mentioned in the previous comment
    # t1=threading.Thread(target=wait_for)
    # t1.start()
    win_num = min(poet)
    if(win_num==random_num):
        # Mining comes here
        print('I win')
    print('Consensus period')

def repeatedly():
    while(True):
        listen_for_transactions()
        complete_listen()
        consensus()

init()
sink()
print(datetime.datetime.now())
# repeatedly()