from keras_preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM

from pandas import read_csv, concat

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, roc_auc_score, log_loss

import tldextract
import numpy as np
import tensorflow as tf
import sys
import time
import os

validChars = {chr(i+45): i for i in range(0, 78)}
maxlen = 127

def do_evaluate(y, probs, round, filename, label):
    f = open("log/char_based_20_round", "a")
    #f.write("---------------------Round" + str(round) + "\n")
    num_sample = len(y)
    count = 0
    for i in range(0, num_sample):
        if label == 1 and probs[i] >= 0.001:
            count += 1
        if label == 0 and probs[i] < 0.001:
            count += 1
    rate = count / num_sample
    #f.write(f"Detection rate for {filename}: {rate}\n")
    y2 = y.to_numpy(dtype='float64')
    y2 = y2.reshape(y2.shape[0], 1)
    probs = probs.astype('float64')
    cross_entropy = log_loss(y2, probs, labels=[1,0])
    f.write(f"{cross_entropy}, ")
    f.close()

if __name__ == "__main__":
    dga_file = os.getcwd() + "/../attacks/attack_char_based_300_each.txt"
    non_dga = os.getcwd() + "/../attacks/benign_01.txt"
    dga_domain = read_csv(dga_file, names=['domain'])
    legit_domain = read_csv(non_dga, names=['domain'])
    dga_domain['tld'] = [tldextract.extract(d).domain for d in dga_domain['domain']]
    legit_domain['tld'] = [tldextract.extract(d).domain for d in legit_domain['domain']]
    dga_domain = dga_domain[~dga_domain['tld'].str.contains('\`|-\.')]
    legit_domain = legit_domain[~legit_domain['tld'].str.contains('\`|-\.')]
    dga_domain = dga_domain.drop_duplicates()
    legit_domain = legit_domain.drop_duplicates()
    dga_domain['label'] = 1
    legit_domain['label'] = 0
    all_domains = concat([legit_domain, dga_domain], ignore_index=True)
    all_domains = all_domains.sample(frac=1).reset_index(drop=True)
    X, y = all_domains['tld'], all_domains['label']
    '''validChars = {x : idx +1 for idx, x in enumerate(set(''.join(X)))}
    #maxFeatures = len(validChars+1)
    maxlen = np.max([len(x) for x in X])'''
    X = [[validChars[y] for y in x] for x in X]
    X = pad_sequences(X, maxlen=maxlen)
    for i in range(1, 11):
        file_model = "save_models/model_after_avg_round" + str(i)
        print(f"Loading model {file_model}")
        current_model = tf.keras.models.load_model(file_model)
        current_model.summary()
        probs = current_model.predict(X)
        do_evaluate(y, probs, i, file_model, 1)
    '''i = 7
    file_model = "save_models/model_after_avg_round" + str(i)
    print(f"Loading model {file_model}")
    current_model = tf.keras.models.load_model(file_model)
    #current_model.summary()
    probs = current_model.predict(X)
    do_evaluate(y, probs, i, file_model, 1)'''