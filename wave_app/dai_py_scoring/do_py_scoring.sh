#!/bin/bash

echo "****** ****** do_py_scoring.sh START ****** ******"

echo "Model path" $1
echo "Input data path" $2
echo "Output data path" $3
echo "Output data path (grad cam)" $4

# scoring-pipeline内に構築済みのPython仮想環境から実行
$1/scoring-pipeline/env/bin/python $HOME/H2O_Wave_GradCam_app/wave_app/dai_py_scoring/run_gradcam.py $1 $2 $3 $4

echo "****** ****** do_py_scoring.sh END ****** ******"
