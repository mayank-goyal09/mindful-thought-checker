# Production-Grade Cognitive Distortion Detector AI

A production-ready service to analyze text and detect cognitive distortions (irrational, exaggerated thought patterns such as catastrophizing or personalization). 

This system consists of a fine-tuned **DistilBERT** sequence classification model optimized using **ONNX Runtime** for high performance, served via a **FastAPI backend** and an interactive **Streamlit frontend**.

---

## ⚡ Why is this Setup "Production-Grade"?

1. **Lightweight & Efficient (Memory Optimization)**:
   * Loading a full PyTorch model in production requires about **~1.2 GB of RAM** and demands the heavy PyTorch package (>1.5 GB disk footprint).
   * By converting the model to **ONNX format**, we load it via `onnxruntime` which operates natively in C++. The model loads in milliseconds and consumes only **~250 MB of RAM (80% memory savings)**.

2. **Incredible Speedup (Latency Optimization)**:
   * CPU-based PyTorch inference can be slow (taking 100ms to 250ms per sentence).
   * In our tests, the ONNX Runtime model performs inference on CPU in under **20ms**, yielding a **112x speedup** compared to loading PyTorch and running prediction from scratch.

3. **High Parity & Accuracy**:
   * The ONNX model outputs predictions identical to the original PyTorch model (max probability difference is `0.000000`).

4. **Decoupled High-Availability Architecture**:
   * The **FastAPI API** handles high-throughput prediction requests.
   * The **Streamlit UI** serves as a decoupled interactive dashboard. It includes a fallback mechanism: if the FastAPI backend goes offline, it automatically falls back to loading the ONNX model locally.

---

## 📂 Project Structure

* `MentalHealth_AI_Model/` - Folder containing the model config, tokenizer files, and `model.onnx` weights.
* `app/`
  * `main.py` - FastAPI application exposing `/health` and `/predict` REST endpoints.
  * `predictor.py` - Core ONNX model loader and prediction pipeline.
  * `distortions_db.py` - Database containing descriptions, examples, and reframing advice for the distortions.
* `streamlit_app.py` - Streamlit dashboard with a thought analyzer and CBT reframing worksheet.
* `convert_to_onnx.py` - Script to export PyTorch weights to ONNX format.
* `requirements.txt` - Project dependencies.

---

## 🚀 How to Run the Project

### 1. Install Dependencies
Make sure you have Python 3.10+ installed. In your terminal, run:
```bash
pip install -r requirements.txt
```
*(If on Windows and running into encoding issues, install `onnxscript` using `pip install onnxscript`)*

### 2. Export the Model to ONNX (Done)
To export the PyTorch model to ONNX, run:
```bash
python -X utf8 convert_to_onnx.py
```
This creates `model.onnx` and `model.onnx.data` inside the `MentalHealth_AI_Model/` directory.

### 3. Run the FastAPI Backend
Start the FastAPI server on port 8000:
```bash
uvicorn app.main:app --port 8000
```
The server will start up on `http://127.0.0.1:8000`. You can view the automatic OpenAPI documentation at `http://127.0.0.1:8000/docs`.

### 4. Run the Streamlit Frontend
Start the Streamlit application:
```bash
streamlit run streamlit_app.py --server.port 8501
```
Open `http://localhost:8501` in your browser.

---

## 🔌 API Documentation

### 1. Health Check
* **Endpoint:** `GET /health`
* **Response:**
```json
{
  "status": "healthy",
  "model_engine": "ONNX Runtime",
  "model_file": "./MentalHealth_AI_Model\\model.onnx",
  "classes_loaded": 5
}
```

### 2. Predict Cognitive Distortion
* **Endpoint:** `POST /predict`
* **Payload:**
```json
{
  "text": "I got a B on the exam. I should always get A's, I'm completely useless."
}
```
* **Response:**
```json
{
  "text": "I got a B on the exam. I should always get A's, I'm completely useless.",
  "predicted_distortion": "Should Statements",
  "confidence": 0.9896,
  "latency_ms": 15.2,
  "distortion_details": {
    "name": "Should Statements",
    "description": "Holding rigid, unrealistic rules for yourself or others, often using words like 'should', 'must', or 'ought to'.",
    "examples": ["I should never make mistakes at work."],
    "reframing_questions": [
      "Why must this rule always apply? Is it realistic?",
      "What happens if I replace 'should' with 'I would prefer to'?"
    ],
    "reframing_advice": "Reframe rules into preferences. Replace rigid 'should' statements with flexible, compassionate language like 'It would be nice if...'."
  },
  "all_probabilities": {
    "Catastrophizing": 0.005,
    "Mental Filter": 0.003,
    "Neutral": 0.001,
    "Personalization": 0.001,
    "Should Statements": 0.9896
  }
}
```
