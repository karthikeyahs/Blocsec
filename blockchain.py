import hashlib
import pymongo
import random
from trpool import Pool
import datetime
 
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["blockchain"]


class Blockchain:
    def __init__(self,me):
        self.state = 0
        self.chain = []
        self.create_genesis_block()
        self.transactions=Pool()
        self.me=me
        print(self.transactions)
    
    def create_genesis_block(self):
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
                'id': ts,
        }
        self.transactions.add(tr)
        rnummsg={
            'tid':tr['id'],
            'rnum':random.random(),
            'msg-type':'random_number',
            'me':me,
        }
        self.update_transactions(rnummsg)
        return([tr,rnummsg])

    

    def validate_block(self,block_received):
        last_block = mydb.blockchain.find().sort([('timestamp', -1)]).limit(1)
        if(last_block['parent_hash']==block_received['parent_hash']):
            return True
        return False

    def mine(self):
        transaction_hash = hashlib.sha256(block['message'].encode())
        parent_block_cursor = mydb.blockchain.find().sort([('timestamp', -1)]).limit(1)
        parent_block_string = parent_block_cursor[0]['sender']+parent_block_cursor[0]['receiver']+parent_block_cursor[0]['timestamp']+parent_block_cursor[0]['random_num']+parent_block_cursor[0]['transaction_hash']+parent_block_cursor[0]['parent_hash']+parent_block_cursor[0]['msg-type']+parent_block_cursor[0]['message']
        print(parent_block_string)
        parent_hash = hashlib.sha256(parent_block_string.encode())
        print(parent_hash.hexdigest())
        block['transaction_hash'] = transaction_hash
        block['parent_hash'] = parent_hash
        mydb.blockchain.insert_one(block)

    def update_transactions(self,msg):
        for el in self.transactions.q:
            if(el['tid']==msg['tid']):
                el['rlist'].append(msg['rnum'])
                return
        msg['id']=msg['tid']
        self.transactions.add(msg)
        self.update_transactions(msg)
        
    