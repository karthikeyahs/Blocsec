import socket
import requests
import threading
import json
 
ip = "http://192.168.43.150:5000"
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
        print(msg)
        c.close()
 
def init():
    global sport,me,myuname
    myuname=str(input("Enter username : "))
    login(myuname)
    global ssockets
    ssockets = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in range(user_count)]
 
    sport = lap[len(get_active_users())-1]
    me = socket.gethostbyname(socket.gethostname())
    print(sport)
    
    c1 = -1
    for soc in ssockets:
        c1 += 1
        if(lap[c1] == sport): 
            continue
        t = threading.Thread(target = socket_listen,args = (soc, lap[c1]))
        t.start()
    
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
    msg=json.dumps(msg).encode('utf-8')
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
        tr={
            'sender': sender,
            'recipient': recipient,
            'message': message,
        }
        rsl=send_all(tr)
        if(len(rsl)!=len(get_active_users()-1)):
            cons()

init()
