#!/bin/bash

# Waveサーバ上にアップされたデータの削除
rm -rf $HOME/wave-0.17.0-linux-amd64/data/f/*

# Waveサーバの起動
cd wave-0.17.0-linux-amd64
nohup ./waved &
echo "Wave server UP!!"

# アプリの起動
cd ~/wave_app
nohup wave0130/bin/python sys_monitoring2.py &
nohup wave0130/bin/wave run app.py &

echo "App is running!!"

