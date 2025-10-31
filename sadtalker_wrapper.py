import os
import subprocess
import sys
import uuid
from pathlib import Path

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

def generate_educational_video(
    audio_path: str,
    image_path: str,
    output_dir: str = "results",
    enhancer="none",
    still_mode: bool = False,
    verbose: bool = True
) -> str:
    """
    Minimal animation wrapper for SadTalker.
    Produces a talking-head video with subtle motion and lip-sync only.

    Parameters
    ----------
    audio_path : str
    image_path : str
    output_dir : str
    enhancer : str
        Optional: [none, lip, face, gfpgan].
    still_mode : bool
        If True, keeps the head mostly still.
    verbose : bool

    Returns
    -------
    str
        Path to the generated video
    """

    # Resolve paths
    sadtalker_dir = os.path.dirname(__file__)
    inference_script = os.path.join(os.path.dirname(sadtalker_dir), "inference.py")
    
    if not os.path.isfile(inference_script):
        inference_script = os.path.join(sadtalker_dir, "inference.py")

    if not os.path.isfile(inference_script):
        inference_script = "/Users/ayashahal/Desktop/ai-edu-video/sadtalker/inference.py"
        if not os.path.isfile(inference_script):
            raise FileNotFoundError(f"inference.py not found. Tried multiple paths.")

    if not os.path.isfile(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Source image not found: {image_path}")

    os.makedirs(output_dir, exist_ok=True)
    job_id = uuid.uuid4().hex[:8]
    job_dir = os.path.join(output_dir, f"sadtalker_{job_id}")
    os.makedirs(job_dir, exist_ok=True)

    # Build command
    cmd = [
        sys.executable,
        inference_script,
        "--driven_audio", audio_path,
        "--source_image", image_path,
        "--result_dir", job_dir,
        "--preprocess", "crop",
    ]

    # Include enhancer only if not 'none'
    current_enhancer = enhancer.lower().strip()
    if current_enhancer and current_enhancer != "none":
        cmd.extend(["--enhancer", current_enhancer])
        
    if still_mode:
        cmd.append("--still")  # keeps head still

    print(f"⚡ Running SadTalker (minimal animation):\n{' '.join(cmd)}\n")

    try:
        if verbose:
            subprocess.run(cmd, check=True, text=True, encoding='utf-8', errors='ignore')
        else:
            subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')

    except subprocess.CalledProcessError as e:
        print("❌ SadTalker failed!")
        stdout = e.stdout if hasattr(e, 'stdout') and e.stdout else ""
        stderr = e.stderr if hasattr(e, 'stderr') and e.stderr else ""
        if stdout:
            print(f"SadTalker STDOUT:\n{stdout}")
        if stderr:
            print(f"SadTalker STDERR:\n{stderr}")
        raise RuntimeError("SadTalker failed during video generation.")
    except Exception as e:
        print(f"❌ Unexpected error during SadTalker run: {e}")
        raise

    # Locate output video
    video_files = list(Path(job_dir).rglob("*.mp4"))
    if video_files:
        video_path = str(video_files[0])
        print(f"✅ Video generated: {video_path}")
        return video_path

    print("⚠️ No video found in result directory")
    return None
