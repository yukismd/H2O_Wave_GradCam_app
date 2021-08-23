print('<< Start: run_gradcam.py >>')

import os
import sys
import inspect
import time
from importlib import import_module
import numpy as np
import pandas as pd


model_path = sys.argv[1]   # スコアリング用データのパス
data_path_input_folder = sys.argv[2]
data_path_output_folder = sys.argv[3]
print(model_path)
print(data_path_input_folder)
print(data_path_output_folder)

# モデル名
for f in os.listdir(os.path.join(model_path, 'scoring-pipeline')):
    if 'scoring_h2oai_experiment_' in f:
        model_file_name = f
        break
model_name = model_file_name.split('-')[0]
print('model name >>>>> ', model_name)

my_model = import_module(model_name)
print(my_model)
print(my_model.Scorer)
print(my_model.scorer._load_pickle_gz)

#from model_name import Scorer
#from model_name.scorer import (
#    _load_pickle_gz,
#)
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

my_scorer = GradCAMScorer()

score = my_scorer.score_gradcam(
    [
        "xxxxx.jpg"  # image
    ],
    '.',
    apply_data_recipes=False,
)
end_time = time.time()

print(score)

#df = pd.DataFrame({'x1':[1,2,3], 'x2':[6,7,8]})
#df.to_csv(os.path.join(model_path, 'test.csv'))

print('<< End: run_gradcam.py >>')