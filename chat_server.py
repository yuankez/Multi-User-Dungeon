# =========================================================================
# File:                      chat_server.py
#
# Title:                     Multi User Dungeon World server
#
# Instruction:
#
# Author:                    Yuanke Zhang
#
# Description:               This file is the Contain the server.
#
# Notes:                     None
#
#===========================================================================

import socket
import threading


def clientThreadIn(conn, nick):
    global data
    global count
    while True:
        #try:
        temp = conn.recv(1024)
        if temp.decode().split(':')[1] == 'exit':
            print(temp.decode())
            #     self.Stop = True
            #     #threading.Event()
            NotifyAll(nick + 'leaves the room')
            count -= 1
            print("There are " +  str(count) + "users in the room")
            print("assas",data)
            return
        if not temp:
            conn.close()
            return
        NotifyAll(temp)
        print(data)
       # except:
    NotifyAll(nick + 'leaves the room')
    count -= 1
    print("There are "+ str(count) + "users in the room")
    print(data)
    return


def clientThreadOut(conn, nick):
    global data
    while True:
        if con.acquire():
            con.wait()
            if data:
                try:
                    conn.send(data)
                    con.release()
                except:
                    con.release
                    return


def NotifyAll(ss):
    global data
    if con.acquire():  # acquire lock
        data = ss
        con.notifyAll()
        con.release()


con = threading.Condition()  # 条件
Host = input('input the server ip address:')  # ip address
port = 1111
data = ''
count = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')
s.bind((Host.encode(), port))
s.listen(5)
print('Socket now listening')

while True:

    conn, addr = s.accept()
    print('Connected with' + '' + addr[0] + ':' + str(addr[1]))
    nick = conn.recv(1024) # get the user name
    count += 1
    NotifyAll(nick.decode() + ' Joined the room chat !! There are ' + str(count) + 'user in the room')
    print(data)
    print(str((threading.activeCount() + 1) / 2) + 'person(s)')
    conn.sendall(data.encode())
    threading.Thread(target=clientThreadIn, args=(conn, nick.decode())) .start()
    threading.Thread(target=clientThreadOut, args=(conn, nick.decode())).start()
