import os

import numpy as np
import streamlit as st
import tensorflow as tf
from huggingface_hub import hf_hub_download
from PIL import Image
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import load_model

from src.config import HF_MODEL_FILENAME, HF_REPO_ID, IMG_SIZE, MODEL_PATH

# Layer konvolusi terakhir ResNet-50, dipakai sebagai sumber peta aktivasi Grad-CAM.
LAST_CONV_LAYER = "conv5_block3_out"

# Model disimpan dengan versi Keras yang lebih baru (config Dense menyertakan
# 'quantization_config'), sedangkan Keras yang terpasang belum mengenal kwarg
# tersebut. Patch from_config agar kwarg tak dikenal diabaikan saat memuat model.
_original_dense_from_config = Dense.from_config.__func__


@classmethod
def _patched_dense_from_config(cls, config):
    config = dict(config)
    config.pop("quantization_config", None)
    return _original_dense_from_config(cls, config)


Dense.from_config = _patched_dense_from_config


def _resolve_model_path() -> str:
    """Pakai model lokal jika ada; jika tidak, unduh dari Hugging Face Hub."""
    if os.path.exists(MODEL_PATH):
        return MODEL_PATH
    return hf_hub_download(repo_id=HF_REPO_ID, filename=HF_MODEL_FILENAME)


@st.cache_resource
def get_model():
    return load_model(_resolve_model_path())


def preprocess_image(image: Image.Image):
    img = image.convert("RGB").resize(IMG_SIZE)
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


def predict(image: Image.Image):
    model = get_model()
    img_array = preprocess_image(image)
    prob = float(model.predict(img_array, verbose=0)[0][0])

    if prob <= 0.5:
        label = "AI Generated"
        confidence = (1 - prob) * 100
    else:
        label = "Human Made"
        confidence = prob * 100

    prob_ai = (1 - prob) * 100
    prob_human = prob * 100

    return {
        "label": label,
        "confidence": confidence,
        "prob_ai": prob_ai,
        "prob_human": prob_human,
        "raw_prob": prob,
    }


@st.cache_resource
def get_gradcam_model():
    model = get_model()
    return tf.keras.models.Model(
        model.inputs,
        [model.get_layer(LAST_CONV_LAYER).output, model.output],
    )


def _apply_jet_colormap(heatmap: np.ndarray) -> np.ndarray:
    # Aproksimasi colormap "jet" (biru -> hijau -> kuning -> merah) tanpa matplotlib.
    h = np.clip(heatmap, 0.0, 1.0)
    r = np.clip(1.5 - np.abs(4.0 * h - 3.0), 0.0, 1.0)
    g = np.clip(1.5 - np.abs(4.0 * h - 2.0), 0.0, 1.0)
    b = np.clip(1.5 - np.abs(4.0 * h - 1.0), 0.0, 1.0)
    return (np.stack([r, g, b], axis=-1) * 255).astype("uint8")


def compute_gradcam(image: Image.Image, raw_prob: float) -> Image.Image:
    """Menghasilkan overlay Grad-CAM untuk kelas yang diprediksi model.

    Heatmap dihitung terhadap kelas hasil prediksi: jika raw_prob <= 0.5
    (prediksi AI), skor yang diturunkan gradiennya adalah 1 - sigmoid agar
    area yang disorot merupakan bukti ke arah kelas AI.
    """
    grad_model = get_gradcam_model()
    img_tensor = tf.convert_to_tensor(preprocess_image(image), dtype=tf.float32)

    with tf.GradientTape() as tape:
        conv_output, preds = grad_model(img_tensor)
        score = preds[:, 0]
        if raw_prob <= 0.5:
            score = 1.0 - score

    grads = tape.gradient(score, conv_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    heatmap = tf.reduce_sum(conv_output[0] * pooled_grads, axis=-1)
    heatmap = tf.maximum(heatmap, 0.0)
    max_val = float(tf.reduce_max(heatmap))
    if max_val > 0:
        heatmap = heatmap / max_val

    heatmap_rgb = _apply_jet_colormap(heatmap.numpy())
    base = image.convert("RGB")
    heatmap_img = Image.fromarray(heatmap_rgb).resize(base.size, Image.BILINEAR)
    return Image.blend(base, heatmap_img, alpha=0.45)
