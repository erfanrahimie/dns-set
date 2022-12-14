import subprocess
from tkinter import *
import json

# Color app
BG = "#212529"
LB = "#f1faee"
EN_BG = "#343a40"
EN_FG = "#f1faee"
BT_BG = "#495057"
BT_FG = "#f1faee"
LB_FG = "#4ecdc4"

# Set window
ws = Tk()
ws.title('DNS SET')
ws.geometry('300x295')
ws.config(bg=BG)
ws.eval('tk::PlaceWindow . center')
ws.resizable(False, False)


# To read the json file
def read():
    with open('Server.json', 'r') as file:
        return json.load(file)


# To write the json file
def write(data):
    with open('Server.json', 'w') as file:
        json.dump(data, file, indent=2)


# Get interface names
CONNECTIONS = []
a = str(subprocess.run("powershell.exe Get-NetAdapter -physical", shell=True, capture_output=True))
for con in a.split('\\r\\n')[3:]:
    if 'Up' in con:
        CONNECTIONS.append(con.split(' ')[0])


# Connect to the selected server
def connect_selected():
    itm = None
    try:
        itm = lb.get(lb.curselection())
    except:
        var.set("Select the server!")
        return
    try:
        server = read()
        index1 = server['Servers'][itm][0]
        index2 = server['Servers'][itm][1]
        for interface in CONNECTIONS:
            msg = subprocess.run(f'netsh interface ipv4 set dnsservers {interface} static {index1}',
                                 shell=True, capture_output=True)
            if 'parameter is incorrect' in str(msg):
                raise ValueError
            subprocess.run(f'netsh interface ipv4 add dnsservers {interface} {index2} index=2', shell=True)
            var.set("Set DNS successfully")
    except ValueError:
        var.set("There is a problem with DNS")


# Add Server popup page
def popup():

    # Add server to file
    def add_dns_server():
        server = read()
        server['Servers'].update({e0.get(): [e1.get(), e2.get()]})
        write(server)
        var.set("Added DNS, please refresh the list")

    # Set popup
    info = Toplevel(ws)
    info.title('Add Dns Server')
    info.geometry("250x150+650+400")
    info.resizable(False, False)
    info.config(bg=BG)

    # Page content
    Label(info, text="Name : ", font=("Arial", 10), bg=BG, fg=LB).grid(row=0, padx=20)
    Label(info, text="Index 1 : ", font=("Arial", 10), bg=BG, fg=LB).grid(row=1)
    Label(info, text="Index 2 : ", font=("Arial", 10), bg=BG, fg=LB).grid(row=2)

    e0 = Entry(info, bg=EN_BG, fg=EN_FG, font=("Arial", 10))
    e0.grid(row=0, column=1, pady=5)
    e1 = Entry(info, bg=EN_BG, fg=EN_FG, font=("Arial", 10))
    e1.grid(row=1, column=1, pady=5)
    e2 = Entry(info, bg=EN_BG, fg=EN_FG, font=("Arial", 10))
    e2.grid(row=2, column=1, pady=5)

    Button(info, bg=BT_BG, fg=BT_FG, text="Add Server", font=("Arial", 10), command=add_dns_server).grid(
        row=4, column=1, pady=20)

    info.transient(ws)
    info.grab_set()


# Refresh ListBox
def refresh_list():
    server = read()
    lb.delete(0, END)
    id = 0
    for serv in server['Servers']:
        lb.insert(id, serv)
        id += 1
    var.set("list updated")


# Delete item from ListBox
def delete_list():
    try:
        itm = lb.get(lb.curselection())
        lb.delete(lb.curselection())
        server = read()
        del server['Servers'][itm]
        write(server)
        var.set("Delete DNS successfully")
    except:
        var.set("Clear DNS successfully")
        for interface in CONNECTIONS:
            subprocess.run(f'netsh interface ipv4 set dnsservers {interface} dhcp', shell=True)


# Page content
lb = Listbox(ws, bg=EN_BG, fg=EN_FG, font=("Arial", 11),
             selectbackground=EN_BG, selectforeground=LB_FG, justify=CENTER, width=100)
lb.pack()

var = StringVar()
disp = Label(ws, textvariable=var, bg=BG, fg=LB_FG, font=("Arial", 10))
disp.pack()

Button(ws, text='Set DNS Server', command=connect_selected, bg=BT_BG, fg=BT_FG, font=("Arial", 10)).pack(
    fill=X, pady=10)
Button(ws, text='Add Server', command=popup, bg=BT_BG, fg=BT_FG, font=("Arial", 10)).pack(
    fill=X, expand=True, side=LEFT)
Button(ws, text='Refresh', command=refresh_list, bg=BT_BG, fg=BT_FG, font=("Arial", 10)).pack(
    fill=X, padx=5, expand=True, side=LEFT)
Button(ws, text='Delete', command=delete_list, bg=BT_BG, fg=BT_FG, font=("Arial", 10)).pack(
    fill=X, expand=True, side=LEFT)

# Add item to ListBox
with open('Server.json', 'r') as file:
    data = json.load(file)
    id = 0
    for serv in data['Servers']:
        lb.insert(id, serv)
        id += 1

ws.mainloop()
