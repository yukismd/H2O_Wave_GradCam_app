#!/bin/bash

# Waveサーバ上にアップされたデータの削除
rm -rf $HOME/wave-0.13.0-linux-amd64/data/f/*

# Waveサーバの起動
cd wave-0.13.0-linux-amd64
nohup ./waved &
echo "Wave server UP!!"

# アプリの起動
cd ~/app_CreditCardScoring_v2
#nohup wave0130/bin/wave run sys_monitoring.py &
nohup wave0130/bin/python sys_monitoring2.py &
nohup wave0130/bin/wave run credit_scoring3.py &
#source wave0130/bin/activate
#nohup wave run sys_monitoring.py &
#nohup wave run credit_scoring3.py &
echo "App is running!!"

