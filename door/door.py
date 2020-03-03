from flask import Flask,session,render_template,request
import socket
import json
import netifaces as ni

app = Flask(__name__)
app.secret_key='secret'

s = socket.socket()	
port = 5001
s.connect((str(ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']),port))

@app.route('/')
def h1():
	return render_template('transaction.html')

@app.route('/generate_new_transaction', methods=['POST'])
def h2():
    global s
    tr={
        'sender':request.form.get('sender'),
        'receiver':request.form.get('receiver'),
        'message':request.form.get('message'),
    }
    print(json.loads(s.recv(1024).decode('utf-8'))) 
    tr = json.dumps(tr).encode('utf-8')
    s.send(tr)
    return render_template('transaction.html')


if __name__=='__main__':
    app.run()
