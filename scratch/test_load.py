import sys
import os
import torch

# Add parent dir to path so we can import from app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import LipReadingModel, NUM_CLASSES

def test_load():
    model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "lipreading_model.pth"))
    print(f"Model path resolved to: {model_path}")
    print("Initializing model...")
    model = LipReadingModel(num_classes=NUM_CLASSES)
    
    print(f"Loading weights from {model_path}...")
    try:
        state_dict = torch.load(model_path, map_location="cpu")
        model.load_state_dict(state_dict)
        print("Success! Model weights loaded successfully without any key mismatches.")
        
        # Test forward pass with a dummy tensor
        dummy_input = torch.randn(1, 25, 3, 112, 112) # batch_size=1, seq_len=25, c=3, h=112, w=112
        with torch.no_grad():
            output = model(dummy_input)
        print(f"Forward pass output shape: {output.shape}")
        print("Model verification passed!")
    except Exception as e:
        print(f"Error loading model weights: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_load()
