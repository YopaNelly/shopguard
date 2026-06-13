import streamlit as st
import numpy as np
import os

SEQUENCE_LENGTH = 32
IMG_SIZE        = 64

# ── Paste your Google Drive file ID here ─────────────────────────────────────
GDRIVE_FILE_ID  = "1rZ9-OdkpX1iewWRpCQa5K0nkPOFmk76_"
LOCAL_MODEL_PATH = "models/best_cnn_bilstm_v2.keras"


def focal_loss(gamma=2.0, alpha=0.25):
    import tensorflow as tf
    def focal_loss_fixed(y_true, y_pred):
        y_true  = tf.cast(y_true, tf.float32)
        pt      = tf.where(tf.equal(y_true, 1), y_pred, 1.0 - y_pred)
        alpha_t = tf.where(tf.equal(y_true, 1), alpha, 1.0 - alpha)
        loss    = -alpha_t * tf.pow(1.0 - pt, gamma) * tf.math.log(pt + 1e-7)
        return tf.reduce_mean(loss)
    focal_loss_fixed.__name__ = "focal_loss_fixed"
    return focal_loss_fixed


def _download_model():
    """Download model from Google Drive if not already present locally."""
    if os.path.exists(LOCAL_MODEL_PATH):
        return True, None

    os.makedirs("models", exist_ok=True)

    try:
        import gdown
        url = f"https://drive.google.com/uc?id={GDRIVE_FILE_ID}"
        st.info("Downloading model from Google Drive (first run only, may take 1-2 minutes)...")
        gdown.download(url, LOCAL_MODEL_PATH, quiet=False)

        if os.path.exists(LOCAL_MODEL_PATH):
            return True, None
        else:
            return False, "Download completed but file not found."

    except Exception as e:
        return False, str(e)


@st.cache_resource
def load_surveillance_model():
    """
    Load CNN-BiLSTM model.
    Downloads from Google Drive on first run, then caches locally.
    Falls back to Demo Mode if download fails or TensorFlow not available.
    """

    # First try local paths (works when running locally with your trained model)
    local_paths = [
        "/home/ngadou/Documents/best_cnn_bilstm_v2",
        "/home/ngadou/Documents/best_cnn_bilstm_v2.keras",
        LOCAL_MODEL_PATH,
    ]

    # Try to download from Google Drive if not found locally
    if not any(os.path.exists(p) for p in local_paths):
        if GDRIVE_FILE_ID != "PASTE_YOUR_FILE_ID_HERE":
            downloaded, err = _download_model()
            if not downloaded:
                st.warning(f"Could not download model: {err}")
        else:
            st.warning("Google Drive file ID not set in model_loader.py")

    # Try loading from any available path
    all_paths = local_paths + [LOCAL_MODEL_PATH]

    for path in all_paths:
        if not os.path.exists(path):
            continue
        try:
            import tensorflow as tf
            from tensorflow.keras.models import load_model

            model = load_model(
                path,
                custom_objects={"focal_loss_fixed": focal_loss()},
                compile=False,
            )
            model.compile(
                optimizer="adam",
                loss=focal_loss(gamma=2.0, alpha=0.25),
                metrics=["accuracy"],
            )
            st.success(f"CNN-BiLSTM model loaded from {path}")
            st.info(f"Input shape: {model.input_shape}")
            return model

        except Exception as e:
            st.warning(f"Could not load from {path}: {e}")
            continue

    # Demo Mode fallback
    st.info("Running in DEMO MODE - model not available on this environment.")

    class DemoModel:
        input_shape = (None, SEQUENCE_LENGTH, IMG_SIZE, IMG_SIZE, 3)

        def predict(self, sequences, verbose=0):
            rng     = np.random.default_rng(seed=42)
            results = []
            for seq in sequences:
                motion = float(np.std(seq)) * 10.0
                base   = min(0.88, max(0.08, motion * 0.28))
                prob   = float(np.clip(base + rng.uniform(-0.12, 0.12), 0.04, 0.96))
                results.append([prob])
            return np.array(results, dtype=np.float32)

    return DemoModel()


def predict_single(model, batch_tensor):
    try:
        result = model.predict(batch_tensor, verbose=0)
        return float(result.flatten()[0])
    except Exception as e:
        st.error(f"Inference error: {e}")
        return 0.5
        
