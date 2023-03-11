import tensorflow as tf
from tensorflow.python.tools import freeze_graph

from model import *
from keras.models import load_model
from tensorflow.python.platform import gfile

from tkinter import *
import tkinter as tk
from tkinter import messagebox

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

class TestDGA(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("DETECT DGA")
        self.geometry("750x750")

        frame_fileinfo = tk.Text(self, width=85, height=5, bg="white")
        btnFrame = Frame(self, bd=2, relief=RIDGE, bg="white")
        btnFrame.place(x=150, y=205, width=350, height=35)

        btnTest = Button(btnFrame, text="Test", command=self.run_test, width=17, font=("times new roman", 13, "bold"),
                         bg="blue", fg="white")
        btn_list = tk.Button(btnFrame, text="List", command=lambda: frame_fileinfo.insert(tk.END, str(getFiles())), width=17, font=("times new roman", 13, "bold"),
                         bg="blue", fg="white")
        btnTest.grid(row=0, column=0)
        btn_list.grid(row=0, column=1)
        frame_fileinfo.place(x=23, y=85)

        self.text_status = tk.Text(self, bg="white", width=85, height=25)
        self.text_status.place(x=23, y=250)

    def run_test(self):
        test_file = os.getcwd() + "/train_file/bigviktor_200_11_.txt"
        test_file2 = os.getcwd() + "/../Client3/train_file/qakbot_200_21_.txt"
        dga_file = os.getcwd() + "/../attacks/matsnu.txt"
        non_dga = os.getcwd() + "/../attacks/benign_1000_01.txt"
        test_domain = read_csv(dga_file, names=['domain'])
        test_domain['tld'] = [tldextract.extract(d).domain for d in test_domain['domain']]
        test_domain = test_domain[~test_domain['tld'].str.contains('\`|-\.')]
        test_domain = test_domain.drop_duplicates()
        test_domain['label'] = 1
        train_domain = test_domain.sample(frac=1).reset_index(drop=True)
        X, y = train_domain['tld'], train_domain['label']
        X = [[validChars[y] for y in x] for x in X]
        domain = pad_sequences(X, maxlen=maxlen)

        model = tf.keras.models.load_model(cur_model_file)
        res = np.array(model.predict(domain))
        dga_number = 0
        legal_number = 0
        for i in np.nditer(res):
            if i > 0.001:
                # print("DGA")
                dga_number += 1
            else:
                # print("legal doamain")
                legal_number += 1
        # result = np.where(res < 0.01)
        # print(np.array(domain))
        # print(result)
        print(f"DGA number = {dga_number}")
        print(f"Legal domain number = {legal_number}")
if __name__ == "__main__":
    cur_model_file = os.getcwd() + "/save_models/model_after_avg_round10"
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

    app = TestDGA()
    app.mainloop()

