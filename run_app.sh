#!/bin/bash

# Waveサーバ上にアップされたデータの削除
rm -rf $HOME/wave-0.17.0-linux-amd64/data/f/*

# Waveサーバの起動
cd $HOME/wave-0.17.0-linux-amd64
nohup ./waved &
echo "Wave server UP!!"

# アプリの起動
cd $HOME/H2O_Wave_GradCam_app/wave_app
nohup env_wave0170/bin/python sys_monitoring2.py &
nohup env_wave0170/bin/wave run app.py &

echo "App is running!!"

