"""
各モデルは、App実行の前に、models内に配置したPythonScoringディレクトリ上で環境構築（run_example.shが実行できる状態）しておかなくてはならない

[2021/8/xx] version 1
"""

import os
import glob
import subprocess
import zipfile
import shutil
from h2o_wave import Q, main, app, ui, handle_on, on, data
import pandas as pd
import numpy as np
import custom_utils

proj_folder = 'H2O_Wave_GradCam_app'

"""
q.client.model_selected
q.client.selected_model
q.client.model_path : '/home/ubuntu/H2O_Wave_GradCam_app/models/art_age'
q.client.data_path_input : '/home/ubuntu/H2O_Wave_GradCam_app/models/art_age/data/input_data'
q.client.data_path_input_folder : zipから展開したフォルダ名 '/home/ubuntu/H2O_Wave_GradCam_app/models/art_age/data/input_data/sample_image_art_age'
q.client.data_path_output : '/home/ubuntu/H2O_Wave_GradCam_app/models/art_age/data/output_data'
q.client.data_path_output_folder : 結果の保存先 '/home/ubuntu/H2O_Wave_GradCam_app/models/art_age/data/output_data/sample_image_art_age'
q.client.data_path_output_folder_gradcam : 結果の保存先(GradCAM) '/home/ubuntu/H2O_Wave_GradCam_app/models/art_age/data/output_data/sample_image_art_age/grad_cam'
"""

def run_python_scoring_pipeline(model_path, data_path_input_folder, data_path_output_folder, data_path_output_folder_gradcam):
    """ model_path上のPythonScoringPipelineを実行
    """
    # data_path_input_folder内の写真をスコアリング
    # data_path_output_folder上に結果csv, data_path_output_folder_gradcam上にgradcam結果写真が保存される
    subprocess.run(['bash', 'dai_py_scoring/do_py_scoring.sh', model_path, data_path_input_folder, data_path_output_folder, data_path_output_folder_gradcam])
    return 'Scoring Done!!!'


@app('/app')
async def serve(q: Q):

    q.page['header'] = ui.header_card(
        box='1 1 6 1',    # x座標 y座標 幅 高さ
        title='Grad-CAM Scoring',
        subtitle='Image Model (Python Scoring) of Driverless AI',
    )

    if not q.client.model_selected:    # 初期画面。モデル選択前
        list_model_path = os.listdir(os.path.join(os.environ['HOME'], proj_folder, 'models'))    # modelsディレクトリのモデル一覧
        choices = [ui.choice(mod, mod) for mod in list_model_path]
        q.page['card_model_select'] = ui.form_card(
            box='1 2 2 10',    # x座標 y座標 幅 高さ
            items=[
                ui.text_xl('Select a model'),
                ui.dropdown(name='button_selected_model', label='Which model?', required=True, choices=choices),
                ui.button(name='button_model_selected', label='Select This Model', primary=True),
            ]
        )
    
    await handle_on(q)     # 各ボタンが押された場合、ここでハンドリング

    print("q.args --> ", q.args)
    print("q.client --> ", q.client)
    await q.page.save()


@on('button_model_selected')
async def model_selected(q: Q):
    """ モデル選択後、ファイルのアップ画面
    """
    #(todo) 以下の場合(モデルが選択されていない)、中止
    # if q.args.button_selected_model=='':

    del q.page['card_model_select'], q.page['card_result']
    q.client.model_selected = True
    q.client.selected_model = q.args.button_selected_model
    q.client.model_path = os.path.join(os.environ['HOME'], proj_folder, 'models', q.client.selected_model)
    q.client.data_path_input = os.path.join(q.client.model_path, 'data', 'input_data')
    os.makedirs(q.client.data_path_input, exist_ok=True)
    q.client.data_path_output = os.path.join(q.client.model_path, 'data', 'output_data')
    os.makedirs(q.client.data_path_output, exist_ok=True)

    q.page['card_data_upload'] = ui.form_card(
        box='1 2 2 10',    # x座標 y座標 幅 高さ
        items=[
            ui.text_xl('Selected model: {}'.format(q.client.selected_model)),
            ui.text_l('Upload the data'),
            ui.file_upload(name='button_file_uploaded', 
                        label='Upload this file & Do scoring', 
                        multiple=True,
                        file_extensions=['zip'],   # 許可するファイル形式
                        max_file_size=10, 
                        max_size=15
            )
        ]
    )


@on('button_file_uploaded')
async def do_scoring(q: Q):
    """ 結果の表示
    """
    del q.page['card_model_select']
    print('Uploaded zip on wave server: {}'.format(q.args.button_file_uploaded))

    local_path_zip = await q.site.download(q.args.button_file_uploaded[0], path=q.client.data_path_input)  # Waveサーバ上のデータをApp実行パス上にロード、そのパスの取得
    print(local_path_zip)
    print(os.path.splitext(os.path.basename(local_path_zip)))
    with zipfile.ZipFile(local_path_zip) as existing_zip:
        existing_zip.extractall(q.client.data_path_input)

    q.client.data_path_input_folder = os.path.join(q.client.data_path_input, os.path.splitext(os.path.basename(local_path_zip))[0])    # zip解凍後フォルダのパス（写真が入っているフォルダ）
    q.client.data_path_output_folder = os.path.join(q.client.data_path_output, os.path.splitext(os.path.basename(local_path_zip))[0])  # 結果保存用（上と同じフォルダ名で作成）
    os.makedirs(q.client.data_path_output_folder, exist_ok=True)
    q.client.data_path_output_folder_gradcam = os.path.join(q.client.data_path_output_folder, 'grad_cam')  # data_path_output_folder下のGradCAM結果保存用
    os.makedirs(q.client.data_path_output_folder_gradcam, exist_ok=True)

    res = run_python_scoring_pipeline(q.client.model_path, q.client.data_path_input_folder, q.client.data_path_output_folder, q.client.data_path_output_folder_gradcam)   # PyScoringの実行
    print(res)

    df_res = pd.read_csv(os.path.join(q.client.data_path_output_folder, 'result.csv'))   # 予測結果

    list_gradcam_img = os.listdir(q.client.data_path_output_folder_gradcam)    # gradcam結果画像一覧
    choices_gc=[ui.choice(img, img) for img in list_gradcam_img]

    #(todo) 結果のzip q.client.data_path_output_folder_gradcam 
    # data_path_output_folder_gradcamフォルダをその名前のまま（grad_cam）、同ディレクトリ上（data_path_output_folder）の保存
    shutil.make_archive(q.client.data_path_output_folder_gradcam, 'zip', root_dir=q.client.data_path_output_folder_gradcam)
    server_file_path = await q.site.upload([q.client.data_path_output_folder_gradcam+'.zip'])   # サーバへアップし、サーバ上パスを取得

    q.page['card_result'] = ui.form_card(
        box='3 2 4 10',    # x座標 y座標 幅 高さ
        items=[
            ui.text_xl('Scoring Result'),
            custom_utils.ui_table_from_df(df=df_res, name='Scoring Result', downloadable=True, height='250px'),
            #ui.text_m(''),
            ui.link(label='Download Grad-CAM Images', download=True, path=server_file_path[0]),
            ui.dropdown(name='gradcam_img', label='Show Grad-CAM image.', trigger=True, choices=choices_gc),
            #ui.text_m(q.args.gradcam_img),
            #(todo) GradCAM結果の表示
        ]
    )
