import os
from threading import *
import time
import signal
import sys
from scapy.all import *

sys.path.insert(0, os.getcwd() + "/../")

from detail_proc import *
from glob_inc.print_log import print_log

from tkinter import *
import tkinter as tk
from tkinter import messagebox


def handle_sigint(sig, frame):
    global raw_domain_thread
    global is_exit
    print_log("Main thread received SIGINT")
    # raw_domain_thread.stop()
    is_exit = True


def is_stop():
    return is_exit


def asyn_capture_domain():
    global queue
    global mutex

    t = AsyncSniffer(iface="ens33", prn=handle_packet(queue, mutex), store=0)
    t.start()


def capture_domain():
    global queue
    global mutex

    sniff(iface="ens33", prn=handle_packet(queue, mutex), store=0)


def init_domain_capture_thread():
    print_log("Main thread is creating a thread to capture domain . . .")
    thread = Thread(target=asyn_capture_domain(), args=())
    # print_log("CAPTURE DOMAIN THREAD HAS STARTED")
    return thread


def start_periodic_fed_learn_process():
    global cur_model_info
    global client_id
    global round_counter

    t = Timer(time_to_fl + 4, fed_learn_process, args=(
    host, port, train_file, non_dga, client_id, cur_model_info, cur_model_file, is_exit, WAIT_TIME * 60, round_counter))
    t.start()
    time.sleep(time_to_fl + 5)
    if is_exit == True:
        t.cancel()
        return
    t.cancel()


def main_comm_process_func():
    global client_id
    global time_to_fl
    if is_exit == True:
        return
    if client_id == -1:
        client_id, time_to_fl = do_hello_process(host, port, client_id)
        print(f"Start FL request in {time_to_fl}")

    start_periodic_fed_learn_process()


def init_main_comm_thread():
    print_log("Main thread is creating main communication thread . . .")
    thread = Thread(target=main_comm_process_func, args=())
    # thread.daemon = True
    return thread


def init_dga_detection_thread():
    global cur_model_info
    global cur_model_file
    global queue
    global mutex
    print_log("Main thread is creating dga detection thread . . .")
    thread = Thread(target=dga_detection_func, args=(cur_model_file, cur_model_info, queue, mutex, is_exit))
    return thread


def read_conf_file(filename):
    global port
    global host
    global train_file
    global non_dga

    f_config = open(os.getcwd() + "/../" + filename)
    print_log("Main thread is reading config file . . .")
    for lines in f_config:
        split_line = lines.split("=")
        conf_type = split_line[0].strip()
        conf_value = split_line[1].strip()
        if conf_type == "PORT":
            port = conf_value
            port = int(port)
        elif conf_type == "CAPTURE_DUR":
            nfstream_dur = conf_value
        elif conf_type == "TRAIN_FILE":
            train_file = os.getcwd() + "/" + conf_value
        elif conf_type == "NON_DGA":
            non_dga = os.getcwd() + "/" + conf_value
        elif conf_type == "SERVER_IP":
            host = conf_value
    f_config.close()


LARGE_FONT = ("verdana", 13, "bold")
HOST = "10.0.2.15"
PORT = 12345
HEADER = 64
FORMAT = "utf8"
DISCONNECT = "x"
CLIENT_DATA_PATH = "/home/thanhhai/Desktop/DistributedAI/Client2/client_model"

# option
SIGNUP = "signup"
LOGIN = "login"
LOGOUT = "logout"
LIST = "listall"
RUN = "runclient"

Live_Account = []
ID = []
Ad = []




def getFiles():
    files = os.listdir(CLIENT_DATA_PATH)
    send_data = ""
    if len(files) == 0:
        send_data += "The client directory is emty"
    else:
        send_data += "\n".join(f for f in files)
    return send_data


def clientListFiles(sck):
    files = getFiles()

    sck.sendall(files.encode(FORMAT))
    sck.recv(1024)

    msg = "end"
    sck.sendall(msg.encode(FORMAT))
    sck.recv(1024)




# defind GUI-app class
class Client(tk.Tk):
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

        if user == "client" and pswd == "1":
            self.showFrame(HomePage)
            curFrame.label_notice["text"] = ""
        else:
            curFrame.label_notice["text"] = "invalid username or password"


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="bisque2")

        label_title = tk.Label(self, text="\nLOG IN FOR CLIENT\n", font=LARGE_FONT, fg='#20639b', bg="bisque2").grid(row=0, column=1)
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
        label_filename = tk.Label(self, text="AVAILABLE MODEL ON CLIENT", font=LARGE_FONT, fg='#20639b', bg="bisque2")

        entry_ipServer = tk.Entry(self)
        entry_port = tk.Entry(self)

        frame_fileinfo = tk.Text(self, width=80, height=5, bg="white")

        btn_logout = tk.Button(self, text="Logout", width=17, font=("times new roman", 13, "bold"),
                         bg="blue", fg="white", command=lambda: controller.showFrame(StartPage))
        btn_list = tk.Button(self, text="List", width=17, font=("times new roman", 13, "bold"),
                         bg="blue", fg="white", command=lambda: frame_fileinfo.insert(tk.END, str(getFiles())))
        btn_run = tk.Button(self, text="Run", width=17, font=("times new roman", 13, "bold"),
                         bg="blue", fg="white", command=self.run_client)

        self.text_status = tk.Text(self, bg="white", width=80, height=20)

        label_IP_server.place(x=30, y=10)
        label_port.place(x=280, y=10)
        label_filename.place(x=200, y=50)

        entry_ipServer.place(x=100, y=10)
        entry_ipServer.insert(0, str(HOST))
        entry_port.place(x=320, y=10)
        entry_port.insert(0, str(PORT))

        btn_list.place(x=80, y=205)
        btn_run.place(x=250, y=205)
        btn_logout.place(x=420, y=205)

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

    def run_client(self):
        read_conf_file("distributedai.config")
        signal.signal(signal.SIGINT, handle_sigint)
        sigset = [signal.SIGINT]

        main_comm_thread = init_main_comm_thread()

        main_comm_thread.start()
        print_log(f"Thread control federated learning function has started")
        '''dga_detection_thread.start()
        print_log(f"Thread for dga detection has started")'''
        # raw_domain_thread.start()
        # print_log(f"Thread for capturing domain from network has started")

        signal.sigwait(sigset)

        # raw_domain_thread.join()
        main_comm_thread.join()
        # dga_detection_thread.join()

        do_goodbye_process(host, port, client_id)

        print_log(f"CLIENT {client_id} HAS STOPPED WORKING", "red")

if __name__ == "__main__":
    # cur_model_file  = os.getcwd() + "/models/degas/nyu_model.h5"
    cur_model_file = os.getcwd() + "/client_model/simple_LSTM_model"
    cur_model_info = ["non_exist", 0, -1]
    client_id = -1
    is_exit = False
    time_to_fl = 0
    WAIT_TIME = 1
    round_counter = 0

    port = -1
    train_file = "none"
    non_dga = "none"
    host = "localhost"

    queue = []
    mutex = Lock()

    # raw_domain_thread = AsyncSniffer(iface = "ens33", prn=handle_packet(queue, mutex), store = 0, stop_filter = is_exit)

    dga_detection_thread = init_dga_detection_thread()

    app = Client()
    app.mainloop()
