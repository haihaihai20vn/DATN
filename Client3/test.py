import tensorflow as tf
import tldextract
from tensorflow.python.tools import freeze_graph

from model import *
from keras.models import load_model
from tensorflow.python.platform import gfile

from tkinter import *
import tkinter as tk
from tkinter import messagebox

from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import os

validChars = {chr(i+45):i for i in range(0,78)}
# maxlen = 63
maxlen = 127

CLIENT_DATA_PATH = "/home/thanhhai/Desktop/DistributedAI/attacks"

def getFiles():
    files = os.listdir(CLIENT_DATA_PATH)
    send_data = ""
    if len(files) == 0:
        send_data += "The server directory is emty"
    else:
        send_data += "\n".join(f for f in files)
    return send_data

class TestDGA:
    def __init__(self, root):
        def run_test():
            data = domainEntry.get()
            print(data)
            domain = [[validChars[ch] for ch in tldextract.extract(data).domain]]
            domain = pad_sequences(domain, maxlen=maxlen)
            model = tf.keras.models.load_model(test_model_file)
            result = model.predict(domain)
            print(result)
            if result > 0.001:
                dga_notice["text"] = ""
                benign_notice["text"] = ""
                dga_notice["text"] = "DGA domain"

                print("DGA called!")
            else:
                dga_notice["text"] = ""
                benign_notice["text"] = ""
                benign_notice["text"] = "Benign domain"
                print("Benign called!")
        self.root = root
        self.root.title("DETECT DGA")
        self.root.geometry("800x750")

        #frame_fileinfo = tk.Text(self.root, width=75, height=5, bg="white", font=("times new roman", 13))
        lbl_domain = Label(self.root, text="Domain:", font=("times new roman", 13, "bold"))
        domainEntry = tk.Entry(self.root, width=75, bg="white", font=("times new roman", 13))
        dga_notice = tk.Label(self.root, text="", fg='red', font=("times new roman", 32, "bold"))
        benign_notice = tk.Label(self.root, text="", fg='green', font=("times new roman", 32, "bold"))
        button_test = tk.Button(self.root, text="Test", width=17, font=("times new roman", 13, "bold"),
                         bg="blue", fg="white", command=run_test)
        button_test .place(x=300, y=205)
        lbl_domain.place(x=23, y=60)
        domainEntry.place(x=100, y=60)
        dga_notice.place(x=250, y=100)
        benign_notice.place(x=250, y=100)

        # bg image
        '''img3 = Image.open("/home/thanhhai/Desktop/DistributedAI/Client3/violet_background.png")
        img3 = img3.resize((500, 400), Image.ANTIALIAS)
        self.photoImage3 = ImageTk.PhotoImage(img3)

        bg_img = Label(self.root, image=self.photoImage3)
        bg_img.place(x=23, y=250, width=85, height=25)

        instruction = LabelFrame(bg_img, bd=2, width=85, height=25, relief=RIDGE, bg="white")
        instruction.place(x=23, y=250)'''
        lbl_instruction = Label(self.root, text="Instruction", fg='black',
                          font=("times new roman", 24, "bold"))
        lbl_step1 = Label(self.root, text="Step 1: Enter the domain name in the entry above", fg='black',
                          font=("times new roman", 18, "bold"))
        lbl_step2 = Label(self.root, text="Step 2: Press the test button", fg='black',
                          font=("times new roman", 18, "bold"))
        lbl_res1a = Label(self.root,
                         text="- If it is an attack domain created by the domain generation algorithm,",
                         fg='black',
                         font=("times new roman", 18, "bold"))
        lbl_res1b = Label(self.root,
                         text="it will display red text: DGA domain",
                         fg='black',
                         font=("times new roman", 18, "bold"))
        lbl_res2 = Label(self.root,
                         text="- If it is a benign domain, it will display blue text: Benign domain",
                         fg='black',
                         font=("times new roman", 18, "bold"))
        lbl_instruction.place(x=300, y=280)
        lbl_step1.place(x=40, y=350)
        lbl_step2.place(x=40, y=400)
        lbl_res1a.place(x=40, y=450)
        lbl_res1b.place(x=50, y=500)
        lbl_res2.place(x=40, y=550)
if __name__ == "__main__":
    test_model_file = os.getcwd() + "/save_models/model_after_avg_round10"
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

    root = tk.Tk()
    obj = TestDGA(root)
    root.mainloop()



