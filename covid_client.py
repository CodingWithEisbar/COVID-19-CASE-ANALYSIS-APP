import tkinter as tk
import threading
import sys
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import socket
from time import sleep
from datetime import date

# get tkinter child
def all_children(window):
    _list = window.winfo_children()
    for item in _list:
        if item.winfo_children():
            _list.extend(item.winfo_children())
    return _list

def parse(d): #read indivitual dictionary
    dictionary = dict()
    # Removes curly braces and splits the pairs into a list
    pairs = d.strip('{}').split(', ')
    for i in pairs:
        pair = i.split(': ')
        # Other symbols from the key-value pair should be stripped.
        dictionary[pair[0].strip('\'\'\"\"')] = pair[1].strip('\'\'\"\"')
    return dictionary

join_message = ""



def request_join(tag):
    if str(password.get()) == "" and str(username.get()) == "":
        messagebox.showinfo("Thông báo", "Vui lòng nhập thông tin của bạn")
        return
    elif str(username.get()) == "":
        messagebox.showinfo("Thông báo", "Vui lòng nhập tên người dùng")
        return
    elif str(password.get()) == "":
        messagebox.showinfo("Thông báo", "Vui lòng nhập mật khẩu")
        return

    data = {"username": str(username.get()), "password": str(password.get())}
    client.send(bytes(str(tag), "utf8"))
    client.send(bytes(str(data), "utf8"))
    msg = client.recv(1024).decode("utf8")
    if (msg == "-ok-"):
        if (tag == "reg"):
            messagebox.showinfo("Thông báo", "Đăng ký thành công")
            
        else:
            messagebox.showinfo("Thông báo", "Đăng nhập thành công")
            
        joinIn()
        threading.Thread(target=received_handle).start()
        client.send(bytes("all", "utf8"))
        return
    if(msg == "-cancel-"):
        messagebox.showinfo("Thông báo", "Tài khoản đã tồn tại")
        
        return
    else:
        messagebox.showinfo("Thông báo", "Tên người dùng hoặc mật khẩu sai")
        

# handle user input and output
def received_handle():
    while True:
        msg = client.recv(1024).decode("utf8", errors='ignore')
        if msg == "out":
            break
        if msg == "shutdown": 
            messagebox.showinfo(title="server request", message="server đã yêu cầu ngừng kết nối")
            threading.Thread(target=on_closing).start()
            continue
        if msg == "data1":
             Vie_but['state'] = 'disabled'
             world_but['state'] = 'disabled'
             button4['state'] = 'disabled'
             global data1
             j = 0
             msg2 = client.recv(1024).decode("utf8", errors='ignore')
             while (msg2 != "end"):
                 temp = parse(msg2)
                 data1.insert(j, temp)
                 msg2 = client.recv(1024).decode("utf8", errors='ignore')
             updateProvinceBox()
             Vie_but['state'] = 'normal'
             world_but['state'] = 'normal'
             button4['state'] = 'normal'

        if msg == "data2":
             Vie_but['state'] = 'disabled'
             world_but['state'] = 'disabled'
             button4['state'] = 'disabled'
             global data2
             j =0
             msg2 = client.recv(1024).decode("utf8", errors='ignore')
             while (msg2 != "end"):
                 temp = parse(msg2)
                 data2.insert(j, temp)
                 msg2 = client.recv(1024).decode("utf8", errors='ignore')
             updateRegionBox()
             Vie_but['state'] = 'normal'
             world_but['state'] = 'normal'
             button4['state'] = 'normal'
        if msg == "date":
            if date_list[0] == "": del date_list[0]
            j= 0
            msg2 = client.recv(1024).decode("utf8", errors='ignore')
            while (msg2 != "end"):
                date_list.insert(j, msg2)
                msg2 = client.recv(1024).decode("utf8", errors='ignore')
            date_box['value'] = date_list
            date_box.current(0)
            global current_day_box
            current_day_box = date_box.get()

def send_handle(cmd):
    client.send(bytes(str(cmd), "utf8"))

def sendDate(event):
    global current_day_box
    if date_box.get() == current_day_box: 
        return
    server_log.insert(END, "đang lấy dữ liệu ngày " + date_box.get() + "\n")
    client.send(bytes(str(date_box.get()), "utf8"))
    current_day_box = date_box.get()


# handle user quit
def on_closing(event=None):
    try:
        """This function is to be called when the window is closed."""
        client.send(bytes("out", "utf8"))
        msg = client.recv(1024).decode("utf8")

        if (msg == "out"):
            client.close()

        top.quit()
    except socket.error:
        sys.exit()


# change frame
def requestBox():
    if not conecting():
        messagebox.showerror(title="failed to connect", message="given server address is not available or actively refuse to connect")
        pass
        return
    frame1.pack_forget()
    frame2.pack()
    InFrom.pack()
    joinFrame.pack()


def joinIn():
    frame2.pack_forget()
    InFrom.pack_forget()
    joinFrame.pack_forget()
    top.geometry("1280x900")
    QuotesnButton.pack()
    frameText_box.pack()
    #server_frame.pack()
    server_log.insert(END,"Chào mừng "+ str(username.get()) + "\n")
    server_log.insert(END,"Hãy giữ gìn sức khoẻ bạn nhé!!\n")

def pack_frame_VietNam():
    send_handle("data1")
    msg_list4.delete('1.0', END)
    Combobox_world.pack_forget()
    frameText_box.pack_forget()
    Combobox_vietnam.pack()
    frameText_box.pack()


def pack_frame_world():
    send_handle("data2")
    msg_list4.delete('1.0', END)
    Combobox_vietnam.pack_forget()
    frameText_box.pack_forget()
    Combobox_world.pack()
    frameText_box.pack()
    

def findnShow_vietnam(event):
    #data1 = getDictionatyData("vietnam.txt")
    #msg_list4.delete('1.0', END)
    for i in data1:
        if(provinceChosen.get() == i['Tỉnh thành[a]']):
            msg_list4.insert(INSERT, "Tỉnh thành: " + i['Tỉnh thành[a]']+"\n")
            msg_list4.insert(INSERT, "Ca nhiễm: " + i['Ca nhiễm']+"\n")
            msg_list4.insert(INSERT, "Đang điều trị: " + i['Đang điều trị']+"\n")
            msg_list4.insert(INSERT, "Hồi phục: " + i['Hồi phục']+"\n")
            msg_list4.insert(INSERT, "Tử vong: " + i['Tử vong[b]']+"\n")
            msg_list4.insert(INSERT, "---------------------------------------------------"+"\n")
            break     

def findnShow_world(event):
    #data2 = getDictionatyData("world.txt")
    for i in data2:
        if(regionChosen.get() == i['country']):
            msg_list4.insert(INSERT, "Quốc gia: " + i['country']+"\n")
            msg_list4.insert(INSERT, "Ca nhiễm: " + i['cases']+"\n")
            msg_list4.insert(INSERT, "Hồi phục: " + i['recovered']+"\n")
            msg_list4.insert(INSERT, "Tử vong: " + i['deaths']+"\n")
            msg_list4.insert(INSERT, "---------------------------------------------------"+"\n")
            break     


def clearScreen():
    msg_list4.delete('1.0', END)

'''def logOut():
    client.send(bytes("out", "utf8"))
    msg = client.recv(1024).decode("utf8")
    if (msg == "out"):
         client.close()
    top.geometry("1280x900")
    #Màn hình kết quả
    QuotesnButton.pack_forget()
    frameText_box.pack_forget()
    Combobox_world.pack_forget()
    Combobox_vietnam.pack_forget()

    #Màn hình đăng nhập
    frame2.pack()
    InFrom.pack()
    joinFrame.pack()'''

province =[""]
region = [""]
date_list = [""]
data1 = []
data2 = []


def updateRegionBox():
    if region[0] == "": del region[0]
    j=0
    for i in data2:
        region.insert(j, i['country'])
        j+=1
    regionChosen['value'] = region
    regionChosen.current(0)
    server_log.insert(END,"Dữ liệu về thế giới đã được cập nhật!\n")

def updateProvinceBox():
    if province[0] == "": del province[0]
    j=0
    for i in data1:
        province.insert(j, i['Tỉnh thành[a]'])
        j+=1
    provinceChosen['value'] = province
    provinceChosen.current(0)
    server_log.insert(END,"Dữ liệu về Việt Nam đã được cập nhật\n")

# # socket create
# HOST_NAME = socket.gethostname()
# HOST = socket.gethostbyname(HOST_NAME)
# PORT = 8080  # input("port: ")

# try:
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# except socket.error as err:
#     print("failed, error no %s\n" % err)
#     sys.exit()
# finally:
#     client.connect((HOST, int(PORT)))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def conecting():
    try:
        client.connect((HOST.get(), int(PORT.get())))
    except socket.error:
        return False
    return True

current_day_box = ""

# GUI implement
top = Tk()
#window_icon = PhotoImage(file='covid-19.png')
#top.iconphoto(True,window_icon)
top.title("COVID-19 Ở VIỆT NAM VÀ TRÊN THẾ GIỚI")
top.geometry("1280x700")
top.protocol("WM_DELETE_WINDOW", on_closing)


HOST = StringVar()
PORT = StringVar()

# first frame
frame1 = Frame(top)
image1 = PhotoImage(file='app_background.png')
Label(frame1, text="TOÀN DÂN HÃY TUÂN THỦ NGHIÊM TẮC 5K CỦA BỘ Y TẾ", font=("Segoe UI", 16)).grid(row=1, column=1, columnspan=4)
Label(frame1, text="! VIỆT NAM QUYẾT THẮNG ĐẠI DỊCH !",fg="red", font=("Consolas", 16)).grid(row=2, column=1, columnspan=4)
Label(frame1, text="host ip: ").grid(row=3, column=2)
Label(frame1, text="host port: ").grid(row=4, column=2)
Entry(frame1, textvariable=HOST).grid(row=3, column=2, columnspan=2)
Entry(frame1, textvariable=PORT).grid(row=4, column=2, columnspan=2)
joinButton = Button(frame1, height=2, width=10, text="JOIN", command=requestBox)
joinButton.grid(row=5, column=2, columnspan=2)
frame1_background = Label(frame1, image=image1).grid(row=6, column=1, columnspan=4)
frame1.pack()

# login and registation frame
frame2 = Frame(top)
Label(frame2, height=2, width=50, text="LOGIN", font=("Rockstone", 45)).pack()
Label(frame2, height=3, width=30, text="HÃY NHẬP THÔNG TIN CỦA BẠN").pack()

# information frame
InFrom = Frame(top)
Label(InFrom, text='Username').grid(row=2)
Label(InFrom, text='Password').grid(row=3)
username = Entry(InFrom)
password = Entry(InFrom, show='*')
username.grid(row=2, column=1)
password.grid(row=3, column=1)

# sign_up frame
joinFrame = Frame(top)
join1 = Button(joinFrame, text="ĐĂNG NHẬP", command=lambda: request_join("log"))
join2 = Button(joinFrame, text="ĐĂNG KÝ", command=lambda: request_join("reg"))
join1.pack(side=LEFT)
join2.pack(side=RIGHT)


#Biểu ngữ và các nút lựa chọn
homnay = date.today()
dinhdang_homnay = homnay.strftime("%d/%m/%Y")
QuotesnButton = Frame(top)
Label(QuotesnButton,text="HÃY GIỮ AN TOÀN CHO BẠN VÀ CHÚNG TA TRƯỚC ĐẠI DỊCH COVID-19", font = ("Segoe UI", 16, "bold"), fg = "red").grid(row=1, column=1, columnspan=2)
Label(QuotesnButton,text="Hôm nay là: " + dinhdang_homnay, font = ("Segoe UI", 11,), fg = "dark blue").grid(row=2, column=1, columnspan=2)
button_list = Label(QuotesnButton, text="Lựa chọn khu vực", width=27)
button_list.grid(row=3, column=1)


#Thêm button VN và TG
Vie_but = Button(QuotesnButton, width = 27, text = "Việt Nam", command=lambda: pack_frame_VietNam())
Vie_but.grid(row=4, column=1)
world_but = Button(QuotesnButton, width = 27, text = "Thế giới", command=lambda: pack_frame_world())
world_but.grid(row=5, column=1)
button4 = Button(QuotesnButton, text='Thoát', width=27, command=on_closing)
button4.grid(row=6, column=1)
'''log_out = Button(QuotesnButton, width = 28, text = "Đăng xuất", command=lambda: logOut())
log_out.pack(side = RIGHT)'''
Label(QuotesnButton ,text="ngày đang tra cứu").grid(row=3, column=2)
date_box = ttk.Combobox(QuotesnButton, width=27, values=date_list, state= 'readonly')
date_box.grid(row=4, column=2)
date_box.current(0)
date_box.bind("<<ComboboxSelected>>", sendDate)
clear_Screen = Button(QuotesnButton, width = 28, text = "Xoá", command=lambda: clearScreen())
clear_Screen.grid(row=6, column=2)
#Combobox
#World
Combobox_world = Frame(top)
Label(Combobox_world, text='Lựa chọn quốc gia: ').pack(side = LEFT)
regionChosen = ttk.Combobox(Combobox_world, width = 27, value = region, state = 'readonly')
regionChosen.pack(side = RIGHT)
regionChosen.current(0)
regionChosen.bind("<<ComboboxSelected>>", findnShow_world)

#VietNam
Combobox_vietnam = Frame(top)
Label(Combobox_vietnam, text='Lựa chọn tỉnh thành: ').pack(side = LEFT)
provinceChosen = ttk.Combobox(Combobox_vietnam, width = 27, value = province, state = 'readonly')
provinceChosen.pack(side = RIGHT)
provinceChosen.current(0)
provinceChosen.bind("<<ComboboxSelected>>", findnShow_vietnam)

#Information Textbox 
frameText_box  = Frame(top)
scrollbar4 = Scrollbar(frameText_box)
Label(frameText_box, text="kết quả tra cứu").grid(row=1, column=1)
msg_list4 = Text(frameText_box, height=20, width=65,yscrollcommand=scrollbar4.set)
msg_list4.grid(row = 2,column = 1,rowspan = 7)
scrollbar4.grid(row = 2,column = 2, sticky = NS,rowspan = 2)

#Server log
#server_frame =Frame(top)
server_log = Text(frameText_box, height=20, width=45)
Label(frameText_box,text='thông báo từ server').grid(row = 1, column=3)
server_log.grid(row = 2, column=3, rowspan=2)

top.mainloop()
