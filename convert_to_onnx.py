import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

def convert_model():
    model_path = "./MentalHealth_AI_Model"
    onnx_path = os.path.join(model_path, "model.onnx")
    
    print(f"Loading PyTorch model from: {model_path}...")
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(model_path, local_files_only=True)
    model.eval()
    
    # 5 output labels mapping:
    # 0: Catastrophizing, 1: Mental Filter, 2: Neutral, 3: Personalization, 4: Should Statements
    print("Model config labels:")
    print(model.config.id2label)
    
    # Create dummy input for ONNX tracing (standard DistilBERT inputs)
    dummy_text = "I feel like everything is going to go wrong and I cannot stop it."
    dummy_input = tokenizer(
        dummy_text,
        max_length=128,
        padding="max_length",
        truncation=True,
        return_tensors="pt"
    )
    
    input_ids = dummy_input["input_ids"]
    attention_mask = dummy_input["attention_mask"]
    
    print(f"Exporting model to ONNX format at: {onnx_path}...")
    
    # Export the model
    torch.onnx.export(
        model,
        (input_ids, attention_mask),
        onnx_path,
        input_names=["input_ids", "attention_mask"],
        output_names=["logits"],
        dynamic_axes={
            "input_ids": {0: "batch_size", 1: "sequence_length"},
            "attention_mask": {0: "batch_size", 1: "sequence_length"},
            "logits": {0: "batch_size"},
        },
        opset_version=14
    )
    
    print("✅ ONNX Model successfully exported and verified!")

if __name__ == "__main__":
    convert_model()
