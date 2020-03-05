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
import pymongo
import hashlib
 
ip = "http://192.168.43.168:5000"
page = "/ul"
login_p = '/logi'
logout_p = '/logout'
data = {
    'num' : '1'
}
 
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["blockchain"]

sport = 0
ssockets = []
 
lap = [12340,12341,12342,12344,12345,12346,12347]
 
user_count = len(lap)

transactionPool = Pool()
purePool = Pool()
blockPool = Pool()

poet=[]

node_state=0
listen_for_transactions_done=0

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
    global poet
    poet.append(msg['random-number'])
    print('handlenum')

def handle_block(block_received):
    if(validate_block(block_received)):
        mydb.blockchain.insert_one(block_received)
    else:
        # Hash comparison wrong

def validate_block(block_received):
    last_block = mydb.blockchain.find().sort([('timestamp', -1)]).limit(1)
    if(last_block['parent_hash']==block_received['parent_hash']):
        return True
    return False

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

def f1():
    pass

def sink():
    r=requests.get(url=ip+'/curd')
    print(r.text)
    s1=r.text
    d1=datetime.datetime(int(s1[:4]),int(s1[5:7]),int(s1[8:10]),int(s1[11:13]),int(s1[14:16]),int(s1[17:19]),int(s1[20:26]))
    print(str(d1))
    peri=10-int(d1.strftime('%S'))%10
    peri=float(peri)-1.0+(1000000.0-float(d1.strftime('%f')))/1000000.0
    print(peri)
    time.sleep(peri)

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
        blockchain.new_transaction(nt['sender'],nt['receiver'],nt['message'])
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
        

def create_genesis_block():
    genesis = {
        'sender':'aaa',
        'receiver':'bbb',
        'timestamp':'1234',
        'random_num':'0.123456',
        'transaction_hash':'0000000000000000',
        'parent_hash':'0000000000000000',
        'msg-type':'block',
        'message':'Genesis block',
    }
    mydb.blockchain.insert_one(genesis)


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
    t = threading.Thread(target=dl)
    t.start()

    create_genesis_block()
    t1 = threading.Thread(target=mine)
    t1.start()
    
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

    def new_transaction(self, sender, receiver, message):
        ts = str(datetime.datetime.now())
        tr={
                'sender': sender,
                'receiver': receiver,
                'message': message,
                'msg-type': 'transaction',
                'timestamp': ts,
        }
        purePool.add(tr)

def wait_for():
    global listen_for_transactions_done,node_state
    if(node_state==0):
        time.sleep(0.5)
    elif(node_state==1):
        time.sleep(0.2)
    else:
        time.sleep(0.3)
    listen_for_transactions_done=1

def listen_for_transactions():
    global listen_for_transactions_done,node_state
    node_state=0
    listen_for_transactions_done=0
    tl=threading.Thread(target=wait_for)
    tl.start()
    while(True):
        # print('dbug\n')
        if(listen_for_transactions_done==1):
            break
        transaction1=purePool.remove()
        if(transaction1==None):
            continue
        transactionPool.add(transaction1)
        print('sending')
        print(transaction1)
        send_all(transaction1)
    print('listening for transactions')

def complete_listen():
    global listen_for_transactions_done,node_state
    node_state=1
    listen_for_transactions_done=0
    t=threading.Thread(target=wait_for)
    t.start()
    while listen_for_transactions_done==0:
        pass
    
    print('Buffer period')

def consensus():
    global listen_for_transactions_done,node_state,poet
    node_state=2
    listen_for_transactions_done=0
    t=threading.Thread(target=wait_for)
    t.start()
    while(True):
        poet=[]
        if listen_for_transactions_done==1:
            break
        if transactionPool.is_empty():
            continue
        random_num = random.random()
        print('my random num '+str(random_num))
        cons = {
            'msg-type': 'random_number',
            'random-number': random_num,
        }
        send_all(cons)
        nou=get_active_users()
        poet.append(random_num)
        while len(poet)!=len(nou):
            # print(poet)
            pass
        print('done')
        win_num = min(poet)
        
        t = threading.Thread(target=if_I_am_winner)
        t.start()

        transaction_mined = transactionPool.remove()
        
    print('Consensus period')

def if_I_am_winner():
    if(win_num==random_num):
        print('I win')
        block={
            'sender':str(transaction_mined['sender']),
            'receiver':str(transaction_mined['receiver']),
            'timestamp':str(transaction_mined['timestamp']),
            'random_num':str(cons['random_number']),
            'message':str(transaction_mined['message']),
            'msg-type':'block',
        }
        blockPool.add(block)

def mine():
    while(blockPool.is_empty()):
        continue
    
    block = blockPool.remove()
    transaction_hash = hashlib.sha256(block['message'].encode())
    parent_block_cursor = mydb.blockchain.find().sort([('timestamp', -1)]).limit(1)
    parent_block_string = parent_block_cursor[0]['sender']+parent_block_cursor[0]['receiver']+parent_block_cursor[0]['timestamp']+parent_block_cursor[0]['random_num']+parent_block_cursor[0]['transaction_hash']+parent_block_cursor[0]['parent_hash']+parent_block_cursor[0]['msg-type']+parent_block_cursor[0]['message']
    print(parent_block_string)
    parent_hash = hashlib.sha256(parent_block_string.encode())
    print(parent_hash.hexdigest())
    block['transaction_hash'] = transaction_hash
    block['parent_hash'] = parent_hash
    mydb.blockchain.insert_one(block)
    send_all(block)

def repeatedly():
    while(True):
        listen_for_transactions()
        complete_listen()
        consensus()

init()
sink()
print(datetime.datetime.now())
repeatedly()