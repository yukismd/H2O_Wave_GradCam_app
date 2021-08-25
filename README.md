# H2O Driverless AI Grad-CAM App

### About
Driverless AIで作成したImage ModelのPython Scoring Pipelineを利用した、Grad-CAMの実行  
画像ファイル一式をzip形式でアップし、スコアリングとGrad-CAMを実施  
![Grad-CAM-App](img/Grad-CAM-App.png)

### 実行環境
AWS EC2(Ubuntu Server 18.04 LTS, t2.large)

### 初期設定
1. [Wave SDK](https://github.com/h2oai/wave/releases/tag/v0.17.0)のダウンロードし、Homeディレクトリ上に解凍
2. 以下「実行に必要なディレクトリとファイル」のmodelsディレクトリとその下に任意のモデル名ディレクトリ（model1やmodel2）を作成
    - 複数のモデルの配置が可能
3. 2で作成したモデル名ディレクトリ下に、Driverless AIで実行済みのExperimentからダウンロードしたPython Scoring Pipelineを配置、解凍（解凍後のフォルダ名はscoring-pipelineとなっている）
4. Python Scoring Pipeline環境の構築。[ドキュメント](https://docs.h2o.ai/driverless-ai/latest-stable/docs/userguide/scoring-standalone-python.html)に従い、scoring-pipelineディレクトリにて作業を実施
    - 本アプリでは、[Running the Python Scoring Pipeline - Alternative Method](https://docs.h2o.ai/driverless-ai/latest-stable/docs/userguide/scoring-standalone-python.html#quick-start-alternative-method)でのインストールを実施し、環境変数（DRIVERLESS_AI_LICENSE_KEY）にDriverless AIライセンスキーを登録
    - インストール方法によって、'do_py_scoring.sh'を修正
5. Wave環境の構築
    - `$ cd $HOME/H2O_Wave_GradCam_app/wave_app/`
    - env_wave0170でPython仮想環境を作成：`$ sudo python3 -m venv env_wave0170`
    - 作成した仮想環境をアクティベート：`$ source env_wave0170/bin/activate`
    - 必要パッケージのインストール：`$ pip install -r requirements.txt `
#### 実行に必要なディレクトリとファイル
```
$HOME/ --- wave-0.17.0-darwin-amd64/ (Wave SDK、Wave実行パス)
        |- H2O_Wave_GradCam_app --- wave_app/ --- app.py
                                               |- custom_utils.py
                                               |- sys_monitoring2.py
                                               |- requirements.txt
                                               |- env_wave0170 (Wave実行用Python仮想環境)
                                               |- dai_py_scoring --- do_py_scoring.sh
                                                                  |- run_gradcam.py
                                                                  |- run_gradcam.py
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

