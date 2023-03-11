import sklearn.metrics
from keras_preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers.core import Dense,Dropout,Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from matplotlib import pyplot as plt

from pandas import read_csv,concat
from sklearn.ensemble import RandomForestClassifier
import sklearn.utils.multiclass
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve, auc, classification_report, accuracy_score

import tldextract
import numpy as np
import os

from sklearn.preprocessing import LabelBinarizer

validChars = {chr(i+45):i for i in range(0,78)}
# maxlen = 63
maxlen = 127

'''def plot_roc_curve(true_y, y_prob):
    """
    plots the roc curve based of the probabilities
    """

    fpr, tpr, thresholds = roc_curve(true_y, y_prob)
    plt.plot(fpr, tpr)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.savefig("mygraph.png")
    #plt.show()'''


def do_train_model(current_model, dga_file, non_dga):
    print(f"train with file {dga_file}, {non_dga}")
    current_model.summary()
    dga_file = os.getcwd() + "/train_file/" + dga_file
    non_dga = os.getcwd() + "/non_dga/" + non_dga
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
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    '''model = Sequential()
    model.add(Embedding(maxFeatures, 128, input_length=maxlen))
    model.add(LSTM(128))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='rmsprop')'''
    #for i in range(5):
    current_model.fit(X_train, y_train, batch_size=16, epochs=10)
    # if necessary, evaluate the model here
    probs = current_model.predict(X)

    '''Confusion matrix _______________________________________________'''
    tn, fp, fn, tp = confusion_matrix(y, probs > 0.5).ravel()
    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    if(tp == 0):
        recall = 1
        precision = 0 if fp > 0 else 1
    f1score = (2*precision*recall)/(precision+recall)
    print("TRAINING RESULT:------------------------------------------")
    print("TP: {}\nTN: {}\nFP: {}\nFN: {}\n".format(tp, tn, fp, fn))
    print("FP rate: {}%\nFN rate: {}%\n".format(fp/(fp+tp)*100, fn/(fn+tn)*100))
    print("Accuracy: {}".format((tp+tn)/(tp+tn+fp+fn)))
    print(f"Precision: {precision}")
    print(f"Recal: {recall}")
    print(f"F1-score: {f1score}")

    '''_________________________________________________________________'''
    num_sample = len(y)
    count = 0
    for i in range(0, num_sample):
        if (probs[i] >= 0.5):
            count += 1
    rate = count / num_sample
    print("DECTECTION RATE:", rate)

    return current_model.get_weights(),  current_model