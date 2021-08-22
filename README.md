# H2O Driverless AI Grad-CAM App

### About
Driverless AIで作成したImage ModelのPython Scoring Pipelineを利用した、Grad-CAMの実行  
画像ファイル一式をzip形式でアップし、スコアリングとGrad-CAMを実施

### Directories and Files
```
$HOME/ --- wave-0.17.0-darwin-amd64/ (Wave SDK、Wave実行パス)
        |- H2O_Wave_GradCam_app --- wave_app/ --- app.py (Grad-CAM APP)
                                               |- env_wave0170 (Wave実行用Python仮想環境)
                                 |- models/ --- model1/ --- scoring-pipeline/ (Driverless AIのPython Scoring Pipeline)
                                                         |- data/ --- input_data/ (アップロードされるスコアリング用データ)
                                                         |- output_data/ (結果データ)
                                             |- model2/
                                             |- ...
                                 |- run_app.sh (Appの開始)
```

### 実行方法

#### 初期設定

#### Appの開始
1. command `$ bash run_app.sh`
2. access "ip:10101/scoring" for Grad-CAM app. "ip:10101/sys" for monitoring app.

#### モデルの追加
