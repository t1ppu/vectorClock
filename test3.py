import socket
import numpy as np
from threading import Thread
import time
import logging
import traceback

ip= "127.0.0.1"
port1= 8003
port2= 8006
sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock2=  socket.socket(socket.AF_INET, socket.SOCK_STREAM)

i=2
v= [0,0,0]

def send_msg():
    global v
    print("-----Press any key to send a message----")
    while True:
        x=input()
        if x:
            sock2=  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock2.bind((ip,port2))
            while True:
                no=input("Enter machine number (1 or 2): ")
                if no not in ('1','2'):
                    print("Please enter correct number.")
                else:
                    fport= 8000+int(no)
                    v[i]+=1
                    msg=''.join(str(x)+' ' for x in v) + ' '
                    inp=input("Enter the message to send:")
                    print(v,end='')
                    msg+=inp
                    try:
                        try:
                            sock2.sendto(msg.encode(),(ip,fport))
                        except:
                            sock2=  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock2.connect((ip,fport))
                            sock2.sendto(msg.encode(),(ip,fport))
                            #sock2.close()
                    except Exception as e:
                        logging.error(traceback.format_exc())
                        print("Couldn't send msg!")
                        v[i]-=1
                    print(v)
                    break
            sock2.shutdown(socket.SHUT_RDWR)
        time.sleep(3)

def rec_msg(sock,addr):
    global v
    #print('Got a msg from', addr)
    try:
        msg = sock.recv(1024)
        print(v,end='')
        v[i]+=1
        #print(msg.decode().split('  ')[1])
        l= [int(x) for x in list(msg.decode().split('  ')[0]) if x.isdigit()]
        v=np.maximum(v,l)
        print(v,end='')
        print(msg.decode().split('  ')[1])
        #print(msg.decode())
    except Exception as e:
        logging.error(traceback.format_exc())

if __name__ == "__main__":
    print("Waiting for msgs")
    sock.bind((ip, port1))
    sock.listen(3)
    #sock2.bind((ip,port2))
    print(sock)
    t1=None
    t2=None
    t1= Thread(target=send_msg,args=(),daemon=True)
    t1.start()
    while True:
        try:
            conn, addr= sock.accept()
            #print(conn)
            if conn:
                t2= Thread(target=rec_msg,args=(conn,addr,), daemon=True)
                t2.start()
            time.sleep(1)
        except Exception as e:
            logging.error(traceback.format_exc())
    print("xx")
    t1.join()
    #s.close()
