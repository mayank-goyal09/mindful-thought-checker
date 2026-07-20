import os
import time
import numpy as np
from transformers import AutoTokenizer
import onnxruntime as ort

class CognitiveDistortionPredictor:
    _instance = None

    @classmethod
    def get_instance(cls, model_dir="./MentalHealth_AI_Model"):
        if cls._instance is None:
            cls._instance = cls(model_dir)
        return cls._instance

    def __init__(self, model_dir="./MentalHealth_AI_Model"):
        self.model_dir = model_dir
        self.onnx_path = os.path.join(model_dir, "model.onnx")
        
        # Verify the ONNX model exists
        if not os.path.exists(self.onnx_path):
            raise FileNotFoundError(
                f"ONNX model file not found at {self.onnx_path}. "
                "Please run `python convert_to_onnx.py` to generate the ONNX file first."
            )
            
        print(f"Loading tokenizer from: {self.model_dir}...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_dir)
        
        print(f"Creating ONNX Runtime InferenceSession for: {self.onnx_path}...")
        # Load ONNX session with CPU execution provider (default for CPU production)
        self.session = ort.InferenceSession(self.onnx_path, providers=['CPUExecutionProvider'])
        
        # Warmup session
        self.predict("Warmup sentence")

    def _softmax(self, logits):
        exp_logits = np.exp(logits - np.max(logits, axis=-1, keepdims=True))
        return exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)

    def predict(self, text: str):
        start_time = time.perf_counter()
        
        # 1. Tokenize input text
        inputs = self.tokenizer(
            text,
            max_length=128,
            padding="max_length",
            truncation=True,
            return_tensors="np"
        )
        
        # Format inputs for ONNX Runtime (needs matching names from the export)
        ort_inputs = {
            "input_ids": inputs["input_ids"].astype(np.int64),
            "attention_mask": inputs["attention_mask"].astype(np.int64)
        }
        
        # 2. Run ONNX Session
        ort_outputs = self.session.run(None, ort_inputs)
        logits = ort_outputs[0]  # Shape: (batch_size, num_classes)
        
        # 3. Softmax to get probabilities
        probabilities = self._softmax(logits)[0]
        
        # 4. Get top prediction
        predicted_class_id = int(np.argmax(probabilities))
        confidence = float(probabilities[predicted_class_id])
        
        latency_ms = (time.perf_counter() - start_time) * 1000
        
        # Construct all class probabilities mapping
        class_probabilities = {
            int(idx): float(prob) for idx, prob in enumerate(probabilities)
        }
        
        return {
            "label_id": predicted_class_id,
            "confidence": confidence,
            "latency_ms": latency_ms,
            "probabilities": class_probabilities
        }
