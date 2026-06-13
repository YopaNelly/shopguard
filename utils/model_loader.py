"""
Model loader for ShopGuard AI.
Loads the trained CNN-BiLSTM from the real path first, then falls back to demo mode.

Python 3.12 + TensorFlow 2.16+ compatible.
"""
import streamlit as st
import numpy as np
import os

# ── Constants matching training ──────────────────────────────────────────────
SEQUENCE_LENGTH = 32
IMG_SIZE        = 64

# Real model path - trained model on this machine
_MODEL_PATHS = [
    "/home/ngadou/Documents/best_cnn_bilstm_v2",
    "/home/ngadou/Documents/best_cnn_bilstm_v2.keras",
    "/home/ngadou/Documents/best_cnn_bilstm_v2/saved_model.pb",
    "models/best_model.keras",
    "models/best_cnn_bilstm_v2.keras",
]


def focal_loss(gamma=2.0, alpha=0.25):
    """
    Focal Loss - must match the function used during training.
    Registered as a custom object when loading the .keras file.
    Compatible with TensorFlow 2.16+ and Python 3.12.
    """
    import tensorflow as tf

    def focal_loss_fixed(y_true, y_pred):
        y_true  = tf.cast(y_true, tf.float32)
        pt      = tf.where(tf.equal(y_true, 1), y_pred, 1.0 - y_pred)
        alpha_t = tf.where(tf.equal(y_true, 1), alpha, 1.0 - alpha)
        eps     = 1e-7
        loss    = -alpha_t * tf.pow(1.0 - pt, gamma) * tf.math.log(pt + eps)
        return tf.reduce_mean(loss)

    focal_loss_fixed.__name__ = "focal_loss_fixed"
    return focal_loss_fixed


@st.cache_resource
def load_surveillance_model():
    """
    Load the trained CNN-BiLSTM model.

    Search order:
      1.  /home/ngadou/Documents/best_cnn_bilstm_v2   (real trained model)
      2.  models/best_model.keras                      (local fallback)
      3.  Demo mode                                    (no model file found)

    Returns a model object (real or DemoModel).
    """
    # Try to find and load the real model
    for path in _MODEL_PATHS:
        if not os.path.exists(path):
            continue

        try:
            import tensorflow as tf
            from tensorflow.keras.models import load_model

            st.info(f"Loading model from: {path}")

            custom_objects = {"focal_loss_fixed": focal_loss()}

            model = load_model(
                path,
                custom_objects=custom_objects,
                compile=False,          # avoid optimizer-state issues on load
            )

            # Recompile for inference (metrics only, no training needed)
            model.compile(
                optimizer="adam",
                loss=focal_loss(gamma=2.0, alpha=0.25),
                metrics=["accuracy"],
            )

            st.success(f"CNN-BiLSTM model loaded successfully from {path}")
            st.info(f"Model input shape: {model.input_shape}")
            return model

        except Exception as exc:
            st.warning(f"Could not load model from {path}: {exc}")
            continue

    # ── Demo mode fallback ────────────────────────────────────────────────────
    st.info("Running in DEMO MODE - no trained model file found at expected paths.")
    st.caption(
        "Expected path: /home/ngadou/Documents/best_cnn_bilstm_v2  "
        "Place the .keras file there and restart the app to use the real model."
    )

    class DemoModel:
        """
        Simulates CNN-BiLSTM predictions using frame motion intensity.
        Produces realistic probability distributions for demonstration.
        """
        input_shape = (None, SEQUENCE_LENGTH, IMG_SIZE, IMG_SIZE, 3)

        def predict(self, sequences, verbose=0):
            rng = np.random.default_rng(seed=42)
            results = []
            for seq in sequences:
                motion = float(np.std(seq)) * 10.0
                base   = min(0.88, max(0.08, motion * 0.28))
                noise  = rng.uniform(-0.12, 0.12)
                prob   = float(np.clip(base + noise, 0.04, 0.96))
                results.append([prob])
            return np.array(results, dtype=np.float32)

    return DemoModel()


def predict_single(model, batch_tensor):
    """
    Run inference on a single prepared batch tensor.

    Parameters
    ----------
    model        : loaded model or DemoModel
    batch_tensor : np.ndarray  shape (1, 32, 64, 64, 3)

    Returns
    -------
    float  probability in [0, 1]
    """
    try:
        result = model.predict(batch_tensor, verbose=0)
        # result shape: (1, 1) or (1,)
        return float(result.flatten()[0])
    except Exception as exc:
        st.error(f"Inference error: {exc}")
        return 0.5   # neutral fallback
