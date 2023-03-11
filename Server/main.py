# import socket programming library

from server_utils import *
from glob_inc.print_log import print_log
from glob_inc.utils import *

from tkinter import *
import tkinter as tk
from tkinter import messagebox

import time
import sys
import math
import os
from sklearn.neural_network import MLPClassifier
import numpy as np

sys.path.insert(0, os.getcwd() + "/../")

from server_utils import *
from glob_inc.print_log import print_log
from glob_inc.utils import *


def remain_to_fl(start_time, duration):
    cur_time = time.time()
    remain_time = duration * 60 - (cur_time - start_time)
    remain_time = math.floor(remain_time)
    if remain_time < 0:
        return 0
    else:
        return remain_time


def handle_hello_msg(conn, addr):
    global id_ip_map_list

    for i in range(len(id_ip_map_list)):
        if id_ip_map_list[i] == 'none':
            id_ip_map_list[i] = addr
            print_log(f"allocate id = {i} for client {addr}", "yellow")
            conn.send(int_to_ubyte(i) + int_to_Nubyte(remain_to_fl(start_wait_time, WAIT_TIME), 32))
            return i


def handle_goodbye_msg(conn, client_id):
    global id_ip_map_list

    client_id = int(client_id)
    id_ip_map_list[client_id] = 'none'
    print_log(f"removed client {client_id}", "red")


def raise_signal(client_id):
    global raise_signal_list

    raise_signal_list[client_id] = 1


def handle_fl_request(conn, client_id):
    global updated_weight_list
    global num_clients_upt_this_round
    client_id = int(client_id)
    send_flearn_population(conn, cur_model_info)
    requirement = recv_model_requirement(conn)
    if requirement == 1:
        print_log(f"Client {client_id} need model version {cur_model_info[2]}")
        send_gmodel(conn, gmodel_path)
    elif requirement == 0:
        pass
    send_training_cmd(conn, client_id)
    updated_weight_list[client_id] = recv_updated_weight(conn)
    num_clients_upt_this_round += 1
    raise_signal(client_id)

    while 1:
        if avg_weight_ready == 1:
            send_weight(conn, avg_weight, client_id)
            break
    print_log(f"finish flearn round for client {client_id}")
    conn.close()


def handle_client(conn, addr):
    global num_clients_this_round

    raw_msg = conn.recv(3)

    if raw_msg[0:2] == b'hl':
        print_log(f"Connected to {addr[0]}, {addr[1]} --- hello message", "green")
        handle_hello_msg(conn, addr)
    elif raw_msg[0:2] == b'gb':
        print_log(f"Connected to {addr[0]}, {addr[1]} --- goodbye message", "green")
        handle_goodbye_msg(conn, raw_msg[2])
    elif raw_msg[0:2] == b'fl':
        print_log(f"Connected to {addr[0]}, {addr[1]} --- flearn request message", "green")
        if is_flearn_time == True:
            num_clients_this_round += 1
            handle_fl_request(conn, raw_msg[2])
        else:
            ref = b'fl_ref' + int_to_Nubyte(remain_to_fl(start_wait_time, WAIT_TIME), 32)
            conn.send(ref)


def print_weight(updated_weight_list):
    for i in range(len(updated_weight_list)):
        print_log(f"UPDATED WEIGHT RECV FROM CLIENT {i}", "yellow", False)
        print_log(updated_weight_list[i], show_time=False)


def cal_avg():
    global avg_weight
    global avg_weight_ready
    global id_ip_map_list
    global updated_weight_list
    global raise_signal_list
    list_of_weight = []
    for i in range(MAX_CLIENT):
        if updated_weight_list[i] != -1:
            list_of_weight.append(updated_weight_list[i])
    # for i in range(len(list_of_weight[0])):
    #     for j in range(1, len(list_of_weight) - 1):
    #         list_of_weight[0][i] += list_of_weight[j][i]
    #     list_of_weight[0][i] /= num_clients_this_round
    # avg_weight = list_of_weight[0]
    # print_log(f"avg_weight for this round is:")
    # print(avg_weight)
    avg_weight = np.mean(list_of_weight, axis=0)
    avg_weight_ready = 1


def is_time_to_avg():
    for i in range(MAX_CLIENT):
        if id_ip_map_list[i] != 'none' and raise_signal_list[i] == 1:
            pass
        else:
            return 0
    return 1


def do_federated_avg():
    global avg_weight_ready
    global id_ip_map_list
    global updated_weight_list
    global raise_signal_list

    num_client_this_round = 0
    list_of_weight = []

    while 1:
        if is_time_to_avg() == 1:
            for i in range(MAX_CLIENT):
                if raise_signal_list[i] == 1:
                    num_client_this_round += 1
                    list_of_weight.append(updated_weight_list[i])
            cal_avg(list_of_weight, num_client_this_round)
            avg_weight_ready = 1
            raise_signal_list = [-1] * MAX_CLIENT


def stop_federated_learning():
    global is_flearn_time
    global num_clients_this_round
    global num_clients_upt_this_round
    global start_wait_time
    if num_clients_this_round > 0:
        print(f"{num_clients_this_round}, {num_clients_upt_this_round}")
        if num_clients_this_round == num_clients_upt_this_round:
            cal_avg()
    start_wait_time = time.time()
    num_clients_this_round = 0
    num_clients_upt_this_round = 0
    is_flearn_time = False
    print("STOP FEDERATED LEARNING ROUND")
    t = threading.Timer(WAIT_TIME * 60, start_federated_learning)
    t.start()


def start_federated_learning():
    global is_flearn_time
    global start_wait_time
    global avg_weight_ready
    global avg_weight
    avg_weight = []
    avg_weight_ready = 0
    is_flearn_time = True
    print("START FEDERATED LEARNING ROUND")
    t = threading.Timer(FL_DUR * 60, stop_federated_learning)
    t.start()


LARGE_FONT = ("verdana", 13, "bold")
HOST = "10.0.2.15"
PORT = 12345
HEADER = 64
FORMAT = "utf8"
DISCONNECT = "x"
SERVER_DATA_PATH = "global_model"

# option
SIGNUP = "signup"
LOGIN = "login"
LOGOUT = "logout"
LIST = "listall"
RUN = "runserver"

Live_Account = []
ID = []
Ad = []


def Check_LiveAccount(username):
    for row in Live_Account:
        parse = row.find("-")
        parse_check = row[(parse + 1):]
        if parse_check == username:
            return False
    return True


def Remove_LiveAccount(conn, addr):
    for row in Live_Account:
        parse = row.find("-")
        parse_check = row[:parse]
        if parse_check == str(addr):
            parse = row.find("-")
            Ad.remove(parse_check)
            username = row[(parse + 1):]
            ID.remove(username)
            Live_Account.remove(row)
            conn.sendall("True".encode(FORMAT))


def check_clientLogIn(username, password):
    if username == "admin" and password == "client":
        return 1

    return 0


def clientLogIn(sck):
    user = sck.recv(1024).decode(FORMAT)
    print("username:--" + user + "--")

    sck.sendall(user.encode(FORMAT))

    pswd = sck.recv(1024).decode(FORMAT)
    print("password:--" + pswd + "--")

    accepted = check_clientLogIn(user, pswd)
    if accepted == 1:
        ID.append(user)
        account = str(Ad[Ad.__len__() - 1]) + "-" + str(ID[ID.__len__() - 1])
        Live_Account.append(account)

    print("accept:", accepted)
    sck.sendall(str(accepted).encode(FORMAT))
    print("end-logIn()")
    print("")


def getFiles():
    files = os.listdir(SERVER_DATA_PATH)
    send_data = ""
    if len(files) == 0:
        send_data += "The server directory is emty"
    else:
        send_data += "\n".join(f for f in files)
    return send_data





# defind GUI-app class
class Server(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("DETECT DGA")
        self.geometry("750x750")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(width=False, height=False)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, HomePage):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame(StartPage)

    def showFrame(self, container):

        frame = self.frames[container]
        if container == HomePage:
            self.geometry("700x750")
        else:
            self.geometry("500x200")
        frame.tkraise()

    # close-programe function
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

    def logIn(self, curFrame):

        user = curFrame.entry_user.get()
        pswd = curFrame.entry_pswd.get()

        if pswd == "":
            curFrame.label_notice["text"] = "password cannot be empty"
            return

        if user == "server" and pswd == "1":
            self.showFrame(HomePage)
            curFrame.label_notice["text"] = ""
        else:
            curFrame.label_notice["text"] = "invalid username or password"


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="bisque2")

        label_title = tk.Label(self, text="\nLOG IN FOR SEVER\n", font=LARGE_FONT, fg='#20639b', bg="bisque2").grid(row=0, column=1)
        label_user = tk.Label(self, text="\tUSERNAME ", fg='#20639b', bg="bisque2", font='verdana 10 bold').grid(row=1, column=0)
        label_pswd = tk.Label(self, text="\tPASSWORD ", fg='#20639b', bg="bisque2", font='verdana 10 bold').grid(row=2, column=0)

        self.label_notice = tk.Label(self, text="", bg="bisque2", fg='red')
        self.entry_user = tk.Entry(self, width=30, bg='light yellow')
        self.entry_pswd = tk.Entry(self, width=30, bg='light yellow', show="*")

        button_log = tk.Button(self, text="LOG IN", bg="#20639b", fg='floral white',
                               command=lambda: controller.logIn(self))

        button_log.grid(row=4, column=1)
        button_log.configure(width=10)
        self.label_notice.grid(row=3, column=1)
        self.entry_pswd.grid(row=2, column=1)
        self.entry_user.grid(row=1, column=1)


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="bisque2")

        label_IP_server = tk.Label(self, text="IP Server:", fg="#20639b", bg="bisque2")
        label_port = tk.Label(self, text="Port:", fg="#20639b", bg="bisque2")
        label_filename = tk.Label(self, text="AVAILABLE MODEL ON SEVER", font=LARGE_FONT, fg='#20639b', bg="bisque2")

        entry_ipServer = tk.Entry(self)
        entry_port = tk.Entry(self)

        frame_fileinfo = tk.Text(self, width=80, height=5, bg="white")

        btn_logout = tk.Button(self, text="Logout", bg="#20639b", fg='floral white', bd=3, width=10,
                               font=("verdana", 9, "bold"), command=lambda: controller.showFrame(StartPage))
        btn_list = tk.Button(self, text="List", bg="#20639b", fg='floral white', bd=3, width=10,
                             font=("verdana", 9, "bold"),
                             command=lambda: frame_fileinfo.insert(tk.END, str(getFiles())))
        btn_refresh = tk.Button(self, text="Run", bg="#20639b", fg='floral white', bd=3, width=10,
                                font=("verdana", 9, "bold"), command=self.run_server)

        self.text_status = tk.Text(self, bg="white", width=80, height=20)

        label_IP_server.place(x=30, y=10)
        label_port.place(x=280, y=10)
        label_filename.place(x=200, y=50)

        entry_ipServer.place(x=100, y=10)
        entry_ipServer.insert(0, str(HOST))
        entry_port.place(x=320, y=10)
        entry_port.insert(0, str(PORT))

        btn_list.place(x=150, y=205)
        btn_refresh.place(x=250, y=205)
        btn_logout.place(x=350, y=205)

        frame_fileinfo.place(x=23, y=85)
        self.text_status.place(x=23, y=250)
        # self.text_status.insert(tk.END,"Waiting for the connection...")

    def Update_Client(self):
        self.text_status.delete('1.0', END)
        if len(Live_Account) == 0:
            self.text_status.insert(tk.END, "Waiting for the connection...")
        else:
            for i in range(len(Live_Account)):
                self.text_status.insert(tk.END, "connected {}".format(Live_Account[i]))
                self.text_status.insert(tk.END, "\n")

    def run_server(self):

        try:
            # avg_thread = threading.Thread(target=do_federated_avg, args=())
            # avg_thread.daemon = True
            # thread_list.append(avg_thread)
            # avg_thread.start()

            host = "10.0.2.15"
            port = 12345
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((host, port))
            print_log(f"SOCKET BINDED TO PORT {port}", show_time=False)

            t = threading.Timer(WAIT_TIME * 60, start_federated_learning)
            t.start()

            # put the socket into listening mode
            s.listen(5)
            print_log("SERVER IS LISTENING . . .")
            # a forever loop until client wants to exit

            while True:
                # establish connection with client
                conn, addr = s.accept()
                # Start a new thread and return its identifier
                new_thread = threading.Thread(target=handle_client, args=(conn, addr))
                new_thread.daemon = True
                thread_list.append(new_thread)
                new_thread.start()

        except KeyboardInterrupt:
            for t in thread_list:
                t.join()
            s.close()
            # print_weight(updated_weight_list)

if __name__ == '__main__':
    MAX_CLIENT = 20
    WAIT_TIME = 1
    FL_DUR = 1
    gmodel_path = os.getcwd() + "/global_model/my_model_new"
    cur_model_info = [0, 0, b'0.0']
    avg_weight_ready = 0
    num_clients_this_round = 0
    num_clients_upt_this_round = 0
    updated_weight_list = [-1] * MAX_CLIENT
    id_ip_map_list = ['none'] * MAX_CLIENT
    raise_signal_list = [-1] * MAX_CLIENT
    thread_list = []
    avg_weight = []
    is_flearn_time = False
    start_wait_time = time.time()

    app = Server()
    app.mainloop()

