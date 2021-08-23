import uuid

import cv2
import numpy as np
import os
import pandas as pd
from h2oaicore.h2oai_images.h2oai_image_classification.automodel import (
    ClassificationAutoModel,
)
from h2oaicore.h2oai_images.h2oai_image_classification.utils import read_img
from h2oaicore.systemutils import (
    config,
    get_num_gpus_per_experiment,
    user_dir,
    call_subprocess_onetask,
    remove,
)
from numpy import nan
from scipy.special._ufuncs import expit
import tensorflow as tf
from tensorflow.errors import ResourceExhaustedError
from tensorflow.keras import backend as K


def _grad_cam_batch(model, images, classes, layer_name, input_shape):
    """
    GradCAM method for visualizing input saliency.
    Same as grad_cam but processes multiple images in one run.
    """

    import cv2

    cv2.ocl.setUseOpenCL(False)
    cv2.setNumThreads(0)

    loss = tf.gather_nd(model.output, np.dstack([range(images.shape[0]), classes])[0])
    layer_output = model.get_layer(layer_name).output
    grads = K.gradients(loss, layer_output)[0]
    gradient_fn = K.function([model.input, K.learning_phase()], [layer_output, grads])

    conv_output, grads_val = gradient_fn([images, 0])
    weights = np.mean(grads_val, axis=(1, 2))
    cams = np.einsum("ijkl,il->ijk", conv_output, weights)

    # Process CAMs
    new_cams = np.empty((images.shape[0], input_shape[0], input_shape[1]))

    for i in range(new_cams.shape[0]):
        cam_i = cams[i] - cams[i].mean()
        cam_i = (cam_i + 1e-10) / (np.linalg.norm(cam_i, 2) + 1e-10)
        new_cams[i] = cv2.resize(
            cam_i, (input_shape[1], input_shape[0]), cv2.INTER_LINEAR
        )
        new_cams[i] = np.maximum(new_cams[i], 0)
        new_cams[i] = new_cams[i] / new_cams[i].max()

    return new_cams


def _predict_single_model(
    sh, test_images, params, stage, model_path, model_weights, gradcam_dir
):
    #     sh.gpu_lock_and_session(logger=None)

    from h2oaicore.models import TensorFlowModel

    tf_model = TensorFlowModel(experiment_id=str(uuid.uuid4()))
    tf_model.params_base = sh.params_base
    sh.tf_config = tf_model.set_tf_config({}, train_shape=(1, 1), valid_shape=(1, 1))
    tf_model.create_new_sess()
    sh.gpus_to_use = sh.tf_config.gpu_options.visible_device_list
    sh.gpu_list = [int(x) for x in sh.gpus_to_use.split(",") if x != ""]
    sh.n_gpus = len(sh.gpu_list)

    kwargs_for_model_type = {
        "pretrained_architecture_name": params["architecture"],
        "n_classes": len(sh.idx2cls),
        "weights": "imagenet",
        "freeze_encoder": False,
        "dropout": params["dropout"],
        "concatenate_poolings": False,
    }

    single_model = ClassificationAutoModel(
        model_type="finetune",
        input_shape=params[f"input_shape_stage_{stage}"],
        multilabel=sh.multilabel,
        kwargs_for_model_type=kwargs_for_model_type,
        crop_strategy=params["crop_strategy"],
        kwargs_for_crop_strategy={},
        workers=sh.num_workers,
        log_dir=params["log_dir"],
        custom_read_func=sh.custom_read_func,
        verbose=sh.verbose,
        params_base=sh.params_base,
    )

    with open(model_path, "wb") as f:
        f.write(model_weights)

    single_model.load_weights(model_path)
    remove(model_path)

    single_model.compile("sgd")

    if single_model.batch_size is not None:
        batch_size = single_model.batch_size
    else:
        batch_size = 32

    batch_size_grid = single_model._get_batch_grid(batch_size)

    for bs in [max(1, x) for x in batch_size_grid]:

        try:
            test_iter = single_model.data_iterator(
                images=test_images,
                labels=None,
                preprocess_function=single_model.preprocess_input,
                batch_size=bs,
                crop_function=single_model.tta_non_crop,
                kwargs_for_crop_strategy=single_model.kwargs_for_crop_strategy,
                augmentations=None,
                shuffle=False,
                input_channels=single_model.input_shape[2],
            )

            for i in range(len(test_iter)):
                start = i * bs
                end = min((i + 1) * bs, len(test_iter.images))
                batch_idx = np.array(range(start, end))
                img_batch = test_iter._get_batches_of_transformed_samples(batch_idx)

                probs = single_model.model.predict_on_batch(img_batch)
                preds = np.argmax(probs, axis=1)
                
                if single_model.template_model is not None:
                    single_model.model = single_model.template_model

                gradcams = _grad_cam_batch(
                    model=single_model.model,
                    images=img_batch,
                    classes=preds,
                    layer_name="grad_cam_layer",
                    input_shape=single_model.input_shape,
                )

                for gradcam_idx, gradcam in enumerate(gradcams):
                    img_path = test_iter.images[start + gradcam_idx]

                    img = test_iter.crop_function(
                        data={"image": read_img(img_path)},
                        **single_model.kwargs_for_crop_strategy,
                    )["image"]

                    jetcam = cv2.applyColorMap(
                        np.uint8(255 * gradcam), cv2.COLORMAP_RAINBOW
                    )
                    jetcam = (np.float32(jetcam) * 0.8 + img * 1.2) / 2

                    jetcam = cv2.cvtColor(np.uint8(jetcam), cv2.COLOR_BGR2RGB)
                    cv2.imwrite(
                        os.path.join(gradcam_dir, os.path.split(img_path)[-1]), jetcam
                    )

            break

        except ResourceExhaustedError as e:
            if bs == 1:
                raise e
            continue


def apply_gradcam_model(test_images, gradcam_dir, model):
    os.makedirs(gradcam_dir, exist_ok=True)
    (search_space, model_bytes), _, _, _ = model.get_model_properties()

    # Initialize the model
    model.params_base["n_gpus"] = get_num_gpus_per_experiment()
    sh = model._initialize_model()
    sh._set_validation_search_space(search_space)

    if getattr(model, "context", None):
        base_path = model.context.experiment_tmp_dir
    else:
        base_path = user_dir()

    for model_name, model_weights in model_bytes.items():
        model_id, stage = [int(x) for x in model_name.split("_")]
        model_path = os.path.join(base_path, str(uuid.uuid4())[:10] + "_keras.model")

        params = sh.search_space[model_id]

        call_subprocess_onetask(
            _predict_single_model,
            args=(),
            kwargs={
                "sh": sh,
                "test_images": test_images,
                "params": params,
                "stage": stage,
                "model_path": model_path,
                "model_weights": model_weights,
                "gradcam_dir": gradcam_dir,
            },
            max_payload_size=1 << 32,
            trials_override=1,
        )

        break
