import tensorflow as tf
from tensorflow.python.tools import freeze_graph

from model import *
from keras.models import load_model
from tensorflow.python.platform import gfile

validChars = {chr(i+45):i for i in range(0,78)}
# maxlen = 63
maxlen = 127


if __name__ == "__main__":
    cur_model_file = os.getcwd() + "/save_models/model_after_avg_round8"
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
    test_file = os.getcwd() + "/../generators/necurs/example_domains.txt"
    test_file2 = os.getcwd() + "/non_dga/benign_01.txt"
    dga_file = os.getcwd() + "/../attacks/fobber.txt"
    non_dga = os.getcwd() + "/../attacks/benign_1000_01.txt"
    test_domain = read_csv(dga_file, names=['domain'])
    test_domain['tld'] = [tldextract.extract(d).domain for d in test_domain['domain']]
    test_domain = test_domain[~test_domain['tld'].str.contains('\`|-\.')]
    test_domain = test_domain.drop_duplicates()
    test_domain['label'] = 1
    train_domain = test_domain.sample(frac=1).reset_index(drop=True)
    X, y = train_domain['tld'], train_domain['label']
    X = [[validChars[y] for y in x] for x in X]
    X = pad_sequences(X, maxlen=maxlen)
    domain = [[validChars[ch] for ch in tldextract.extract('lopqmutrecwilhzya.net').domain]]
    domain = pad_sequences(domain, maxlen=maxlen)

    #folder_model = os.getcwd() + "/save_models/model_after_avg_round3"

    model = tf.keras.models.load_model(cur_model_file)
    #model.summary()
    res = model.predict(domain)
    print(res)
    if res > 0.01:
        print("DGA")
    else:
        print("legal domain")

