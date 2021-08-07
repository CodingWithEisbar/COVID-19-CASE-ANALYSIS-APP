import socket
import threading
import sys
import time
import tkinter
from tkinter.constants import NS
from tkinter.ttk import  Label
from tkinter import Scrollbar, messagebox
import web_scarping

import datetime


def updateData(file_name, data):
    file = open(file_name, "a", encoding="utf8");
    file.write(str(data) + "\n")
    file.close()


user_list = web_scarping.getDictionatyData("user_list.txt")

date_list = web_scarping.getListData("data_date.txt")

def check(inform):
    for i in user_list:
        if i["username"] == inform["username"]:
            return 1
    return 0

def check1(inform):
    for i in date_list:
        if i == inform:
            return 1
    return 0

def already_joined(inform):
    for i in joined_list:
        if i == inform["username"]:
            return 1
    return 0

def findAndDel(inform):
    for i in range(len(joined_list)):
        if joined_list[i] == inform:
            joined_list.pop(i)
            return


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        try:
            client, client_address = server.accept()
        except socket.error:
            return
        #print("%s:%s has connected." % client_address)
        list1.insert(tkinter.END, str(client_address) + " has connected")
        joined = False 
        username = ""
        while True: #use loop for reconection
            tag = client.recv(1024).decode("utf8")
            #handle exit client
            if (tag == "out"):
                client.send(bytes("out", "utf8"))
                #print("%s:%s has disconnected." % client_address)
                list1.insert(tkinter.END, str(client_address) + " has disconnected")
                client.close()
                break
            inform = client.recv(1024).decode("utf8")
            getinform = web_scarping.parse(inform)
            #login client
            if (tag == "log" and check(getinform) == 1):
                #already joined check
                if (already_joined(getinform) == 1): 
                    client.send(bytes("-cancel-", "utf8"))
                    continue
                #send sucessfull log
                client.send(bytes("-ok-", "utf8"))
                client.send(bytes("sign in successful!!", "utf8"))
                username = getinform["username"]
                joined = True
                break
            #register client
            if (tag == "reg"):
                #already signed in check
                if (check(getinform) == 1):
                    client.send(bytes("-cancel-", "utf8"))
                    continue
                #send sucessfull reg
                client.send(bytes("-ok-", "utf8"))
                client.send(bytes("sign up successful!!", "utf8"))
                #new member
                user_list.append(getinform)
                updateData("user_list.txt", getinform)
                #----------
                username = getinform["username"]
                joined = True
                break
            #other case
            client.send(bytes("-denied-", "utf8"))
        #handle joined user
        if joined:
            address[client] = client_address
            client_data_buffer[client] = ""
            client_name[client] = username
            joined_list.append(username)
            updateUserBox()
            
            #print("%s:%s join with account:" % client_address, username + '.') 
            list1.insert(tkinter.END, str(client_address) + " joined with account: " + username + ".")
            handle = threading.Thread(target=handle_client_send, args=(client, ))
            currentThread.append(handle)
            handle.start()
            
def sendData(client, date):
    client.send(bytes("data1", "utf8"))
    data = web_scarping.getDictionatyData(date + "_vietnam.txt")
    for i in data:
        #print(i)
        client.sendall(bytes(str(i), "utf8"))
        time.sleep(1e-12)
    client.send(bytes("end", "utf8"))
    time.sleep(1e-12)
    client.send(bytes("data2", "utf8"))
    data = web_scarping.getDictionatyData(date+"_world.txt")
    for i in data:
        client.sendall(bytes(str(i), "utf8"))
        time.sleep(1e-12)
    client.send(bytes("end", "utf8"))         


def handle_client_send(client):
    while True:
        cmd = client.recv(1024).decode("utf8")
        if (cmd == "out"):
            client.send(bytes("out", "utf8"))
            client.close()
            #print("%s:%s has disconnected." % address[client])
            list1.insert(tkinter.END, str(address[client]) + " has disconnected")
            findAndDel(client_name[client])
            del client_name[client]
            del address[client]
            del client_data_buffer[client]
            updateUserBox()
            break

        if (cmd == "all"):
            list1.insert(tkinter.END, str(address[client]) + " requesting data for set up")
            client.send(bytes("date", "utf8"))
            for i in date_list:
                client.send(bytes(str(i), "utf8"))
                time.sleep(1e-12)
            client.send(bytes("end", "utf8"))
            time.sleep(1e-12)
            sendData(client, datetime.datetime.now().strftime("%d-%m-%Y"))
            client_data_buffer[client] = datetime.datetime.now().strftime("%d-%m-%Y")

        if (check1(cmd) == 1):
            list1.insert(tkinter.END, str(address[client]) + " requesting data")
            if client_data_buffer[client] == cmd: continue
            sendData(client, cmd)
            client_data_buffer[client] = cmd


def Data_update():
    today = datetime.datetime.now().strftime("%d-%m-%Y")
    if check1(today) == 0: 
        updateData("data_date.txt",today) 
        date_list.append(today)
        boardcast2()
    file1 = datetime.datetime.now().strftime("%d-%m-%Y_world.txt")
    file2 = datetime.datetime.now().strftime("%d-%m-%Y_vietnam.txt")
    web_scarping.update_Data2(file1)
    web_scarping.update_Data1(file2)
    list2.insert(tkinter.END, "data has been updated")
    boardcast1()

def Auto_Data_update():
    t = 0
    while UPDATE:
        time.sleep(1)
        t+=1
        if (t == 60 * 60):
            Data_update()
            t = 0

def boardcast1():
    for i in client_data_buffer:
        sendData(i, client_data_buffer[i])

def boardcast2():
    for i in client_name:
        i.send(bytes("date", "utf8"))
        for j in date_list:
            i.send(bytes(str(j), "utf8"))
            time.sleep(0.000000001)
        i.send(bytes("end", "utf8"))
        


def disconecting():
    for i in client_data_buffer:
        i.sendall(bytes("shutdown", "utf8"))

    list2.insert(tkinter.END, "all clients has disconected")

UPDATE = True

def on_closing(event=None):
    """This function is to be called when the window is closed."""
    if  len(joined_list) != 0:
        messagebox.showerror("can not shutdown", message='require all client to be disconected (press "REQUEST SHUTDOWN")')
        pass 
        return
    global UPDATE
    UPDATE = False
    top.destroy()
    server.close()
    
client_name = {}
client_data_buffer = {}
address ={}
joined_list = []

currentThread =[]

def updateUserBox():
    box.delete(0, 'end')
    for i in joined_list:
        box.insert(tkinter.END, str(i))

#tkinter
top = tkinter.Tk()
top.title("server test")
top.geometry("500x600")
top.protocol("WM_DELETE_WINDOW", on_closing)

Label(top, text="COVID-19'S CASE SERVER MANAGEMENT",  font=30).grid(row=1, column=1, columnspan=2)

Label(top, text="joined user").grid(row=2, column=1)
scrollbar0 = Scrollbar(top)
box = tkinter.Listbox(top, height=10, width = 25, yscrollcommand=scrollbar0)
box.grid(row=3, column=1)

Label(top, text="activity log").grid(row=2, column=2)
scrollbar =  tkinter.Scrollbar(top)
list1 = tkinter.Listbox(top, height=15, width=50, yscrollcommand=scrollbar)
list1.grid(row=3, column=2 ,rowspan=3)
scrollbar.grid(row=3, column=3, rowspan=3, sticky=NS)

button = tkinter.Button(top, text="REQUEST SHUTDOWN", height=2,width=20, command=disconecting)
button.grid(row=4, column=1)
button2 = tkinter.Button(top, text="UPDATE DATA BASE", height=2, width=20, command=Data_update)
button2.grid(row=5, column=1)


frame = tkinter.Frame(top)
Label(frame, text="server log").pack()
scrollbar2 =  tkinter.Scrollbar(frame)
list2 = tkinter.Listbox(frame, width=75, height=8, yscrollcommand=scrollbar2)
list2.pack(side=tkinter.LEFT)
scrollbar2.pack(side=tkinter.LEFT,fill=tkinter.Y)
frame.grid(row=6, column=1, columnspan=2)


#----------------------------------------------------    
PORT = 8080
HOST_NAME = socket.gethostname()
HOST = socket.gethostbyname(HOST_NAME)


try:
    server = socket.socket()
except socket.error as err:
    print ("failed, error no %s\n" % err)
    sys.exit()
finally:
    server.bind((HOST, PORT)); server.listen(5);
    # print("bind with %s at port %s\n" % (HOST, PORT))
    # print("listening....")
    list2.insert(tkinter.END, "bind with " + str(HOST) + " at port " + str(PORT))
    list2.insert(tkinter.END, "listening...")
    



    
if __name__ == "__main__":
    Data_update()
    thread1 = threading.Thread(target=accept_incoming_connections)
    thread2 = threading.Thread(target=Auto_Data_update)
    thread2.start()
    thread1.start()
    top.mainloop()    