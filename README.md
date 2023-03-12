# DATN
***INSTALL LIBRARY***
1) install python 3.8
sudo apt-get install python3.8
2) install pip3:
sudo apt-get -y install python3-pip
3) Install tensorflow 2.5
pip3 install tensorflow==2.5
4) Install tldextract
pip3 install tldextract
5) Install sklearn:
pip3 install -U scikit-learn
6) Install scapy:
pip3 install scapy
7) Install pandas
pip3 install pandas

***Run program***
1) Fix file distributedai.config
   SERVER_IP = your IP address
2) Run a server:
   <br/>cd DATN/Server/
   <br/>sudo python3 threaded_server.py
3) Run a first client:
   <br/>cd DATN/Client2/
   <br/>sudo python3 full_feature_client.py
4) Run a second client:
   <br/>cd DATN/Client3/
   <br/>sudo python3 full_feature_client.py
5) Test model:
   <br/>cd DATN/Client2/
   <br/>sudo python3 test.py
