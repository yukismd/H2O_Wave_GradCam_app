print('<< Start: run_gradcam.py >>')

import os
import sys
import inspect
import time
from importlib import import_module
import numpy as np
import pandas as pd


model_path = sys.argv[1]
data_path_input_folder = sys.argv[2]   # スコアリング用データのパス
data_path_output_folder = sys.argv[3]   # 結果保存先
data_path_output_folder_gradcam = sys.argv[4]   # 結果保存先（GradCAM）
print(model_path)
print(data_path_input_folder)
print(data_path_output_folder)
print(data_path_output_folder_gradcam)

# モデル名
for f in os.listdir(os.path.join(model_path, 'scoring-pipeline')):
    if 'scoring_h2oai_experiment_' in f:
        model_file_name = f
        break
model_name = model_file_name.split('-')[0]
print('model name >>>>> ', model_name)

# Python Scoring Modelのimport
my_model = import_module(model_name)
#print(my_model)
#print(my_model.Scorer)
#print(my_model.scorer._load_pickle_gz)

from gradcam_inference import apply_gradcam_model


class GradCAMScorer(my_model.Scorer):
    def score_gradcam(self, row, gradcam_dir, **kwargs):
        try:
            model_dir = os.path.dirname(inspect.getfile(my_model.Scorer))
            model = my_model.scorer._load_pickle_gz(d=model_dir, p="fitted_model.pickle")
            apply_gradcam_model(test_images=row, gradcam_dir=gradcam_dir, model=model)
        except Exception as e:
            print(e)

        return self.score(row, **kwargs)

    def score_gradcam_batch(self, input_frame, gradcam_dir, **kwargs):
        try:
            test_images = input_frame.to_numpy().flatten()
            model_dir = os.path.dirname(inspect.getfile(my_model.Scorer))
            model = my_model.scorer._load_pickle_gz(d=model_dir, p="fitted_model.pickle")
            apply_gradcam_model(
                test_images=test_images,
                gradcam_dir=gradcam_dir,
                model=model,
            )
        except Exception as e:
            print(e)

        return self.score_batch(input_frame, **kwargs)

gc_scorer = GradCAMScorer()

col_name = gc_scorer.get_column_names()[0]   # 学習データで利用していた画像パスのカラム名
print(gc_scorer.get_column_names())

images = os.listdir(data_path_input_folder)
image_list = [os.path.join(data_path_input_folder, img) for img in images]

print('---------- Score Batch ----------')
columns = [
    pd.Series(image_list, name=col_name, dtype='object'),
        ]
df = pd.concat(columns, axis=1)

start_time = time.time()
res = gc_scorer.score_gradcam_batch(df, data_path_output_folder_gradcam, apply_data_recipes=False)
end_time = time.time()
print('------> Time spent for scoring: {}'.format(end_time - start_time))

df_image = pd.DataFrame({'image_name':images})
res = pd.concat([df_image, res], axis=1)

print(res)   # pd.DataFrame

res.to_csv(os.path.join(data_path_output_folder, 'result.csv'), index=False)

print('<< End: run_gradcam.py >>')