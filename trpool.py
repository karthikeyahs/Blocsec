class Pool:
    q = []
    def __init__(self):
        self.q = []
    def add(self,transaction):
        tid=transaction['id']
        self.q.append({
            'tid':tid,
            'rlist':[],
            'traction':transaction
        })
        sorted(self.q,key=lambda i:i['tid'],receive=True)
    def remove(self):
        if len(self.q)==0:
            return None
        temp=self.q.remove()
        sorted(self.q,key=lambda i:i['tid'],receive=True)
        return temp
    def see(self):
        if len(self.q)==0:
            return None
        return self.q[0]
    def is_empty(self):
        return len(self.q)==0
    def __str__(self):
        s=''
        for el in self.q:
            s+=str(el['tid'])+'\n'
            for e1 in el['rlist']:
                s+=str(e1)+'\n'
        return s