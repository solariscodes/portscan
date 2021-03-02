#
# Simple Portscanner TCP in Python using sockets
# Rodrigo march 2, 2021
#
import socket

host='www.terra.com.br'
ports=(441,444)

socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def solveDns(self):
    self=socket.gethostbyname(self)
    return self

def checkPort(self):
    global solved
    solved=solveDns(host)
    #solved='192.168.1.1'
    fulladress=(solved,self)
    isalive=socket1.connect_ex(fulladress)
    if isalive == 0:
        return "open"
    else:
        return "closed"

def scan():
    global num
    num=0
    print("Portscan TCP by solariscodes.\nScanning",host,"\n")
    for i in range(ports[0],ports[-1]):
        a = checkPort(i)
        print("Port", i, "is", a)
        if a == 'open':
            num=num+1
    print("Scan finished.")
    print("Total ports opened: ", num)

scan()
