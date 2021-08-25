# H2O Driverless AI Grad-CAM App

### About
Driverless AIで作成したImage ModelのPython Scoring Pipelineを利用した、Grad-CAMの実行  
画像ファイル一式をzip形式でアップし、スコアリングとGrad-CAMを実施

### 実行環境
AWS EC2(Ubuntu Server 18.04 LTS, t2.large)

### 初期設定
1. [Wave SDK](https://github.com/h2oai/wave/releases/tag/v0.17.0)のダウンロードし、Homeディレクトリ上に解凍
2. 以下’Directories and Files’のmodelsディレクトリとその下に任意のモデル名ディレクトリ（model1やmodel2）を作成
3. ２で作成したモデル名ディレクトリ下に、Driverless AIで実行済みのExperimentからダウンロードしたPython Scoring Pipelineを配置、解凍（解凍後のフォルダ名はscoring-pipelineとなっている）
4. Python Scoring Pipeline環境の構築
    - あああ
5. いいい



#### Directories and Files
```
$HOME/ --- wave-0.17.0-darwin-amd64/ (Wave SDK、Wave実行パス)
        |- H2O_Wave_GradCam_app --- wave_app/ --- app.py
                                               |- custom_utils.py
                                               |- sys_monitoring2.py
                                               |- requirements.txt
                                               |- env_wave0170 (Wave実行用Python仮想環境)
                                 |- models/ --- model1/ --- scoring-pipeline/ (Driverless AIのPython Scoring Pipeline)
                                             |- model2/
                                             |- ...
                                 |- run_app.sh
```


#### Appの開始
`$ cd ~/H2O_Wave_GradCam_app`  
`$ bash run_app.sh` （アプリ開始用スクリプト）  
"Grad-CAM Scoring"アプリへは、YourIP:10101/app  
"System Monitoring"アプリへは、YourIP:10101/sys

#### モデルの追加
