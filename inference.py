import os
import cv2
import numpy as np
import torch
import torch.nn as nn
import pyttsx3
from torchvision import models, transforms

# ─── Config ───────────────────────────────────────────────────────────────────
MODEL_PATH     = "lipreading_model.pth"
IMG_SIZE       = 112
MAX_FRAMES     = 25

GRID_VOCAB = ["sil", "bin", "lay", "place", "set", "blue", "green", "red", "white", 
              "at", "by", "in", "with", "a", "b", "c", "d", "e", "f", "g", "h", 
              "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", 
              "v", "x", "y", "z", "zero", "one", "two", "three", "four", "five", 
              "six", "seven", "eight", "nine", "again", "now", "please"]
char_to_ix = {ch: i for i, ch in enumerate(GRID_VOCAB)}
ix_to_char = {i: ch for i, ch in enumerate(GRID_VOCAB)}
NUM_CLASSES = len(GRID_VOCAB)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ─── Model ────────────────────────────────────────────────────────────────────
class LipReadingModel(nn.Module):
    def __init__(self, num_classes=NUM_CLASSES):
        super(LipReadingModel, self).__init__()
        try:
            mobilenet = models.mobilenet_v2(weights=None)
        except (AttributeError, TypeError):
            mobilenet = models.mobilenet_v2(pretrained=False)
        self.feature_extractor = mobilenet.features
        self.pool = nn.AdaptiveAvgPool2d((1, 1))
        
        # FINE-TUNING IMPROVEMENT: Unfreeze the final CNN blocks of MobileNetV2 (from block 14 onwards)
        for name, param in self.feature_extractor.named_parameters():
            block_idx = int(name.split('.')[0]) if name.split('.')[0].isdigit() else 0
            if block_idx >= 14:
                param.requires_grad = True
            else:
                param.requires_grad = False
            
        self.lstm = nn.LSTM(input_size=1280, hidden_size=256, num_layers=2, 
                            batch_first=True, bidirectional=True)
        self.fc = nn.Linear(512, num_classes)

    def forward(self, x):
        batch_size, seq_len, c, h, w = x.size()
        x = x.view(batch_size * seq_len, c, h, w)
        features = self.feature_extractor(x)
        features = self.pool(features)
        features = features.view(batch_size, seq_len, -1)
        
        lstm_out, _ = self.lstm(features)
        out = self.fc(lstm_out)
        return out

# Lazy-load model and Haar Cascade detector
_model = None
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Lazy-load T5 LLM models
_t5_model = None
_t5_tokenizer = None

def get_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model weights not found at '{MODEL_PATH}'. "
                                    "Place your lipreading_model.pth next to inference.py.")
        _model = LipReadingModel(num_classes=NUM_CLASSES).to(device)
        state = torch.load(MODEL_PATH, map_location=device)
        _model.load_state_dict(state)
        _model.eval()
    return _model

def get_t5():
    global _t5_model, _t5_tokenizer
    if _t5_model is None or _t5_tokenizer is None:
        try:
            from transformers import T5ForConditionalGeneration, T5Tokenizer
            model_name = "t5-base"
            _t5_tokenizer = T5Tokenizer.from_pretrained(model_name)
            _t5_model = T5ForConditionalGeneration.from_pretrained(model_name).to(device)
        except Exception as e:
            print("=" * 60)
            print(f"  WARNING: Failed to fetch/load T5 model from Hugging Face: {e}")
            print("  The application will automatically fall back to raw predictions.")
            print("=" * 60)
            _t5_model = "FAILED"
            _t5_tokenizer = "FAILED"
    if _t5_model == "FAILED":
        return None, None
    return _t5_model, _t5_tokenizer

# ─── Inference helpers ─────────────────────────────────────────────────────────
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def extract_lips(video_path, max_frames=MAX_FRAMES):
    cap = cv2.VideoCapture(video_path)
    frames = []
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        mouth_roi = None
        for (x, y, w, h) in faces:
            # Mathematical adjustment targeting lower-half mouth area
            mouth_y = int(y + h * 0.65)
            mouth_h = int(h * 0.25)
            mouth_x = int(x + w * 0.25)
            mouth_w = int(w * 0.5)
            mouth_roi = frame[mouth_y:mouth_y+mouth_h, mouth_x:mouth_x+mouth_w]
            break 
            
        if mouth_roi is not None and mouth_roi.size > 0:
            mouth_roi = cv2.resize(mouth_roi, (IMG_SIZE, IMG_SIZE))
        else:
            # Safe frame-slice fallback if face-tracking slips
            h, w, _ = frame.shape
            mouth_roi = cv2.resize(frame[int(h*0.6):int(h*0.9), int(w*0.3):int(w*0.7)], (IMG_SIZE, IMG_SIZE))
            
        frames.append(mouth_roi)
        if len(frames) >= max_frames:
            break
            
    cap.release()
    
    while len(frames) < max_frames:
        frames.append(np.zeros((IMG_SIZE, IMG_SIZE, 3), dtype=np.uint8))
        
    return np.array(frames)

def decode_prediction(logits):
    pred_idxs = torch.argmax(logits, dim=-1).squeeze(0).cpu().numpy()
    
    decoded_words = []
    prev_word = ""
    for idx in pred_idxs:
        word = ix_to_char[idx]
        if word != "sil" and word != prev_word:
            decoded_words.append(word)
            prev_word = word
    raw_predicted_text = " ".join(decoded_words)
    return raw_predicted_text

def refine_text_with_llm(raw_text):
    if not raw_text or raw_text == "(no speech detected)":
        return raw_text
        
    try:
        model, tokenizer = get_t5()
        llm_prompt = f"Correct the grammar and spelling: {raw_text}"
        inputs = tokenizer(llm_prompt, return_tensors="pt").to(device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_length=32,
                repetition_penalty=2.5,
                no_repeat_ngram_size=2,
                early_stopping=True
            )
            
        refined_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
        cleaned = refined_output.strip()
        
        # Split by periods to look for sentences
        sentences = [s.strip() for s in cleaned.split(".") if s.strip()]
        
        valid_sentences = []
        for s in sentences:
            s_lower = s.lower()
            if "correct grammar" in s_lower or "spelling" in s_lower or "grammar and spelling" in s_lower:
                if ":" in s:
                    after_colon = s.split(":", 1)[1].strip()
                    if after_colon and not ("grammar" in after_colon.lower() or "spelling" in after_colon.lower()):
                        valid_sentences.append(after_colon)
                continue
            valid_sentences.append(s)
            
        if valid_sentences:
            cleaned = " ".join(valid_sentences)
        else:
            cleaned = raw_text
            
        cleaned = cleaned.lstrip(":,. ")
        return cleaned.strip() if cleaned.strip() else raw_text
    except Exception as e:
        print(f"T5 generation error: {e}")
        return raw_text

def text_to_speech(text, out_path):
    """Synthesise speech and save as WAV. Tries offline pyttsx3, falls back to gTTS."""
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        engine.setProperty("volume", 1.0)
        engine.save_to_file(text, out_path)
        engine.runAndWait()
        print("Successfully synthesized audio offline using pyttsx3.")
    except Exception as e:
        print(f"Offline TTS failed: {e}. Falling back to gTTS (online)...")
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang='en')
            tts.save(out_path)
            print("Successfully synthesized audio online using gTTS.")
        except Exception as online_err:
            print(f"Online TTS fallback failed: {online_err}")
            raise e
