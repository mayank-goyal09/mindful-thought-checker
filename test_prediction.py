import os
import time
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from app.predictor import CognitiveDistortionPredictor
from app.distortions_db import DISTORTIONS_MAP

def verify_predictions():
    test_text = "If I don't get this job, I'll never find a career and my life will be a total failure."
    print(f"Test Sentence: '{test_text}'\n")
    
    # 1. Run inference using original PyTorch model
    print("--- Running PyTorch Model ---")
    model_path = "./MentalHealth_AI_Model"
    start_pt = time.perf_counter()
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    pt_model = AutoModelForSequenceClassification.from_pretrained(model_path, local_files_only=True)
    pt_model.eval()
    
    inputs = tokenizer(test_text, max_length=128, padding="max_length", truncation=True, return_tensors="pt")
    with torch.no_grad():
        outputs = pt_model(**inputs)
        pt_logits = outputs.logits.numpy()
    
    # Apply softmax
    pt_probs = np.exp(pt_logits - np.max(pt_logits, axis=-1, keepdims=True))
    pt_probs = pt_probs / np.sum(pt_probs, axis=-1, keepdims=True)
    pt_probs = pt_probs[0]
    
    pt_class = int(np.argmax(pt_probs))
    pt_conf = pt_probs[pt_class]
    pt_latency = (time.perf_counter() - start_pt) * 1000
    
    print(f"PyTorch Prediction: {DISTORTIONS_MAP[pt_class]['name']} ({pt_conf:.2%})")
    print(f"PyTorch Loading + Inference Latency: {pt_latency:.2f} ms")
    
    # 2. Run inference using ONNX Runtime
    print("\n--- Running Optimized ONNX Runtime ---")
    start_onnx_load = time.perf_counter()
    predictor = CognitiveDistortionPredictor.get_instance(model_path)
    onnx_load_latency = (time.perf_counter() - start_onnx_load) * 1000
    
    # Measure inference only
    start_onnx_inf = time.perf_counter()
    onnx_res = predictor.predict(test_text)
    onnx_inf_latency = (time.perf_counter() - start_onnx_inf) * 1000
    
    onnx_class = onnx_res["label_id"]
    onnx_conf = onnx_res["confidence"]
    
    print(f"ONNX Prediction: {DISTORTIONS_MAP[onnx_class]['name']} ({onnx_conf:.2%})")
    print(f"ONNX Model Initialization Latency: {onnx_load_latency:.2f} ms")
    print(f"ONNX Inference Latency (Single Sentence): {onnx_inf_latency:.2f} ms")
    
    # 3. Verify parity
    print("\n--- Parity Verification ---")
    print(f"Predictions Match: {pt_class == onnx_class}")
    diff = np.abs(pt_probs - np.array(list(onnx_res["probabilities"].values())))
    print(f"Max Probability Difference: {np.max(diff):.6f}")
    
    # 4. Latency analysis
    speedup = pt_latency / onnx_inf_latency
    print(f"Speedup Factor (PyTorch Loading + Inference vs ONNX Inference): {speedup:.1f}x")

if __name__ == "__main__":
    verify_predictions()
