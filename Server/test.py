
'''import sys

from tkinter import *


def TimesTable():
    print("\n")
    result = ""
    print("Hello")
    result = result + "Hello" + "\n"
    print("DGA")
    result = result + "DGA" + "\n"


    # for x in range(1, 13):
    #     m = 1
    #     print('\t\t', (x), ' x ', (m), ' = ', (x * m), )
    #     result = result + '\t\t' + str(x) + ' x ' + str(m) + ' = ' + str(x * m) + "\n"
    result = Label(Multiply, text=result, justify='left').grid(row=9, column=6)


Multiply = Tk()
Multiply.geometry('250x500+700+200')
Multiply.title('Multiplication Table')

EnterTable = StringVar()

label1 = Label(Multiply, text='                                         ').grid(row=4, column=6)

button1 = Button(Multiply, text='Times Table', command=TimesTable).grid(row=5, column=6)
label1 = Label(Multiply, text='                                         ').grid(row=6, column=6)

Multiply.mainloop()'''
import time
import sys
import math
import os
from sklearn.neural_network import MLPClassifier
import numpy as np
import tensorflow as tf
from tensorflow.python.tools import freeze_graph

from keras.models import load_model
from tensorflow.python.platform import gfile

gmodel_path = os.getcwd() + "/global_model/my_model_new"
model = tf.keras.models.load_model(gmodel_path)
model.summary()
