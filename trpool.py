class Pool:
    q = []
    def __init__(self):
        self.q = []
    def add(self,transaction):
        self.q.append(transaction)
        sorted(self.q,key=lambda i:i['timestamp'],reverse=True)
    def remove(self):
        if len(self.q)==0:
            return None
        return self.q.pop()
    def __str__(self):
        s=''
        for el in self.q:
            s+='Type :'+el['msg-type']+'\n'+'Timestamp : '+el['timestamp']+'\n'+'Message : '+el['message']+'\n'+'Sender : '+el['sender']+'\n'+'Recipient : '+el['recipient']+'\n\n'
        return s