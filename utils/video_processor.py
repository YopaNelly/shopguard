"""
Video processing utilities for ShopGuard AI.
Extracts and preprocesses frames for CNN-BiLSTM inference.
Also extracts preview frames at a larger display size for on-screen viewing.
"""
import cv2
import numpy as np

# Must match training constants exactly
SEQUENCE_LENGTH  = 32
IMG_SIZE         = 64    # model input size
PREVIEW_SIZE     = 224   # display size for on-screen frame previews (larger = visible)


def extract_uniform_frames(
    video_path: str,
    num_frames: int = SEQUENCE_LENGTH,
    img_size:   int = IMG_SIZE,
):
    """
    Extract exactly `num_frames` frames uniformly sampled from the video.
    Preprocesses for model input: BGR→RGB, resize to img_size×img_size, normalise to [0,1].

    Returns
    -------
    sequence : np.ndarray  shape (num_frames, img_size, img_size, 3)  float32
    error    : str or None
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None, "Could not open video file."

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames < num_frames:
        cap.release()
        return None, (
            f"Video too short: {total_frames} frames found, "
            f"minimum {num_frames} required."
        )

    indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
    frames  = []

    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(idx))
        ret, frame = cap.read()
        if not ret:
            break
        rgb     = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(rgb, (img_size, img_size), interpolation=cv2.INTER_AREA)
        normed  = resized.astype(np.float32) / 255.0
        frames.append(normed)

    cap.release()

    if len(frames) != num_frames:
        return None, f"Only extracted {len(frames)} of {num_frames} required frames."

    return np.stack(frames, axis=0), None


def extract_preview_frames(
    video_path:  str,
    num_frames:  int = 8,
    display_size: int = PREVIEW_SIZE,
):
    """
    Extract a small set of evenly-spaced frames at display resolution for on-screen viewing.
    These are NOT used for model inference (they are too large for the model input).

    Returns
    -------
    frames : list of np.ndarray  each shape (display_size, display_size, 3)  uint8 RGB
    error  : str or None
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return [], "Could not open video file."

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames < 1:
        cap.release()
        return [], "Video contains no frames."

    indices = np.linspace(0, total_frames - 1, min(num_frames, total_frames), dtype=int)
    frames  = []

    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(idx))
        ret, frame = cap.read()
        if not ret:
            continue
        rgb     = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Resize maintaining aspect ratio, then centre-crop to square
        h, w    = rgb.shape[:2]
        scale   = display_size / min(h, w)
        nh, nw  = int(h * scale), int(w * scale)
        rgb     = cv2.resize(rgb, (nw, nh), interpolation=cv2.INTER_AREA)
        # Centre crop
        y0 = (nh - display_size) // 2
        x0 = (nw - display_size) // 2
        rgb = rgb[y0: y0 + display_size, x0: x0 + display_size]
        frames.append(rgb)

    cap.release()
    return frames, None


def process_video_for_inference(video_path: str):
    """
    Full pipeline: extract model-ready frames and add batch dimension.

    Returns
    -------
    batch_tensor : np.ndarray  shape (1, SEQUENCE_LENGTH, IMG_SIZE, IMG_SIZE, 3)
    error        : str or None
    """
    sequence, error = extract_uniform_frames(video_path)
    if error:
        return None, error
    return np.expand_dims(sequence, axis=0), None


def get_video_metadata(video_path: str) -> dict:
    """Read basic video metadata without loading frames."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {}
    meta = {
        "fps":          cap.get(cv2.CAP_PROP_FPS),
        "frame_count":  int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        "width":        int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height":       int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    }
    meta["duration"] = meta["frame_count"] / meta["fps"] if meta["fps"] > 0 else 0
    cap.release()
    return meta
