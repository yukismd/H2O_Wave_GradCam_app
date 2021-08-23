import inspect
import os

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import time

import numpy as np
import pandas as pd

from scoring_h2oai_experiment_781087ea_f0d6_11eb_85c5_0242ac110002 import Scorer
from scoring_h2oai_experiment_781087ea_f0d6_11eb_85c5_0242ac110002.scorer import (
    _load_pickle_gz,
)
from gradcam_inference import apply_gradcam_model


class GradCAMScorer(Scorer):
    def score_gradcam(self, row, gradcam_dir, **kwargs):
        try:
            model_dir = os.path.dirname(inspect.getfile(Scorer))
            model = _load_pickle_gz(d=model_dir, p="fitted_model.pickle")
            apply_gradcam_model(test_images=row, gradcam_dir=gradcam_dir, model=model)
        except Exception as e:
            print(e)

        return self.score(row, **kwargs)

    def score_gradcam_batch(self, input_frame, gradcam_dir, **kwargs):
        try:
            test_images = input_frame.to_numpy().flatten()
            model_dir = os.path.dirname(inspect.getfile(Scorer))
            model = _load_pickle_gz(d=model_dir, p="fitted_model.pickle")
            apply_gradcam_model(
                test_images=test_images,
                gradcam_dir=gradcam_dir,
                model=model,
            )
        except Exception as e:
            print(e)

        return self.score_batch(input_frame, **kwargs)

scorer = GradCAMScorer()

print('---------- Score Row ----------')
start_time = time.time()

gradcam_dir="gradcam_out/"

score = scorer.score_gradcam(
    [
        "image/0ad489f5869ccfbf76dd.jpg"  # image
    ],
    gradcam_dir,
    apply_data_recipes=False,
)
end_time = time.time()

print(score)
print('------> Time spent: {}'.format(end_time - start_time))


print('---------- Score Batch ----------')
columns = [
    pd.Series(['image/0adf9aa5cc9ed73eb3a9.jpg',
        'image/0af60b45f35cf91e0c5d.jpg',
        'image/0c515020cc274031c263.jpg',
        'image/0c6c88f8163296db363d.jpg',
        'image/0c792460fd93a2ccd1b5.jpg',
        'image/1c863a363fa4bca238f4.jpg',
        'image/1cab368ec3a2b40f51c2.jpg',
        'image/1cc7f4d0bff3f740bd22.jpg',
        'image/1e072aa553fb1f938e6f.jpg',
        'image/1e5e6fda412e961e1be6.jpg',
        'image/1ee84e02f381edf874dd.jpg'], name='image', dtype='object'),
        ]
df = pd.concat(columns, axis=1)

start_time = time.time()
print(scorer.score_gradcam_batch(df, gradcam_dir, apply_data_recipes=False))
end_time = time.time()
print('------> Time spent: {}'.format(end_time - start_time))    
