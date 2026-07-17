import os
import sys
import torch

# Ensure we can import from app.py in the same folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from inference import (
        LipReadingModel, 
        extract_lips, 
        transform, 
        decode_prediction, 
        refine_text_with_llm,
        MODEL_PATH,
        device
    )
except ImportError as e:
    print(f"Error: Could not import inference modules. Make sure you run this script from the project folder. Detail: {e}")
    sys.exit(1)

def test_video(video_path, use_llm=True):
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at '{video_path}'")
        return

    print("=" * 60)
    print(f"[*] Testing Lip2Speech on video: {os.path.basename(video_path)}")
    print("=" * 60)

    # 1. Load model
    print("[1] Loading model weights...")
    try:
        model = LipReadingModel()
        model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
        model.to(device)
        model.eval()
        print("[OK] Model loaded successfully!")
    except Exception as e:
        print(f"[ERROR] Failed to load model weights: {e}")
        return

    # 2. Extract lips
    print("[2] Extracting lip features from video...")
    try:
        lips = extract_lips(video_path)
        print(f"[OK] Extracted {len(lips)} frames successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to extract lips: {e}")
        return

    # 3. Preprocess
    print("[3] Preprocessing lip frames...")
    try:
        transformed_frames = []
        for f in lips:
            transformed_frames.append(transform(f))
        tensor = torch.stack(transformed_frames).unsqueeze(0).to(device)
    except Exception as e:
        print(f"[ERROR] Preprocessing failed: {e}")
        return

    # 4. Model Inference
    print("[4] Running model inference...")
    try:
        with torch.no_grad():
            logits = model(tensor)
        raw_prediction = decode_prediction(logits)
        print("[OK] Inference complete!")
    except Exception as e:
        print(f"[ERROR] Model inference failed: {e}")
        return

    # 5. Optional LLM Refinement
    refined_prediction = raw_prediction
    if use_llm:
        print("[5] Refining text using local T5 LLM...")
        try:
            refined_prediction = refine_text_with_llm(raw_prediction)
        except Exception as e:
            print(f"[WARN] T5 Refinement failed: {e}")

    # Display results
    print("\n" + "=" * 50)
    print(f"RAW PREDICTION:     {raw_prediction if raw_prediction else '(no speech detected)'}")
    if use_llm:
        print(f"REFINED PREDICTION: {refined_prediction if refined_prediction else '(no speech detected)'}")
    print("=" * 50 + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_video.py <path_to_video.mp4>")
        sys.exit(1)

    video_arg = sys.argv[1]
    test_video(video_arg)
