#
# Simple Portscanner TCP in Python using sockets
# Rodrigo march 2, 2021
#
import socket
import sys

if len(sys.argv) <= 3:
    print("Wrong syntax!")
    print("Syntax: portscan.py HOST PORT RANGE")
    print("Example: portscan.py www.nasa.gov 1 80")
    sys.exit(1)

host=sys.argv[1]
ports=(int(sys.argv[2]),int(sys.argv[3]))

socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def solveDns(self):
    try:
        self=socket.gethostbyname(self)
    except:
        print("Unable to resolve",host)
        sys.exit(1)
    return self

def checkPort(self):
    global solved
    solved=solveDns(host)
    fulladress=(solved,self)
    isalive=socket1.connect_ex(fulladress)
    if isalive == 0:
        return "open"
    else:
        return "closed"

def scan():
    global num
    num=0
    print("Portscan TCP by solariscodes\nScanning",host,"\nThis may take a while...")
    for i in range(ports[0],ports[-1]):
        a = checkPort(i)
        print("Port", i, "is", a)
        if a == 'open':
            num=num+1
    print("Scan finished.")
    print("Total ports opened: ", num)

scan()
