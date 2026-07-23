import os
import sys
import time

# Ensure current directory is on path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import gradio as gr
from fastapi import FastAPI
from app.main import app as fastapi_app
from app.predictor import CognitiveDistortionPredictor
from app.distortions_db import DISTORTIONS_MAP

# ZeroGPU compatibility mock
try:
    import spaces
except ImportError:
    class spaces:
        @staticmethod
        def GPU(fn=None, duration=None):
            if fn is None:
                return lambda f: f
            return fn


# 1. Custom premium CSS for Gradio
custom_css = """
body, .gradio-container {
    background: radial-gradient(circle at 10% 20%, #0f172a 0%, #0a0f1d 90%) !important;
    color: #f1f5f9 !important;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}
.glass-hero {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.65) 0%, rgba(15, 23, 42, 0.75) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 24px;
    padding: 2.5rem;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
    margin-bottom: 2rem;
    text-align: center;
}
.hero-title {
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #38bdf8 0%, #a855f7 50%, #f43f5e 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}
.hero-subtitle {
    color: #94a3b8;
    font-size: 1.1rem;
    line-height: 1.6;
}
.endpoint-badge {
    background: rgba(56, 189, 248, 0.15);
    color: #38bdf8;
    border: 1px solid rgba(56, 189, 248, 0.3);
    border-radius: 6px;
    padding: 0.2rem 0.5rem;
    font-family: monospace;
    font-size: 0.9rem;
}
.output-card {
    background: rgba(30, 41, 59, 0.45);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}
"""

# 2. Gradio Web Interface
with gr.Blocks() as demo:


    # Hero Banner
    gr.HTML("""
    <div class="glass-hero">
        <h1 class="hero-title">🧠 Mindful Cognitive Distortion AI</h1>
        <p class="hero-subtitle">
            An enterprise-grade, real-time cognitive distortion detection system. 
            Powered by fine-tuned <strong>DistilBERT</strong> & optimized with <strong>ONNX Runtime</strong> for ultra-low latency CBT analysis.
        </p>
    </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=3):
            gr.Markdown("### ✍️ Input Thought Analysis")
            input_text = gr.Textbox(
                label="Enter your stressful or recurring negative thought:",
                placeholder="E.g., If I fail this presentation, I'm a complete failure and everybody will laugh at me.",
                lines=4,
                max_lines=8
            )
            
            # Preset Examples
            gr.Markdown("**💡 Try Sample Thoughts:**")
            with gr.Row():
                ex_catastrophizing = gr.Button("🌋 Exam failure panic", size="sm")
                ex_filter = gr.Button("🔍 Text reply delay", size="sm")
                ex_should = gr.Button("📏 Rigid perfection rule", size="sm")
            
            submit_btn = gr.Button("⚡ Run Neural Prediction", variant="primary", size="lg")
            
        with gr.Column(scale=2):
            gr.Markdown("### 📊 Analysis Dashboard")
            
            with gr.Group():
                prediction_out = gr.HTML("""
                <div style="background: rgba(30, 41, 59, 0.45); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 1.5rem; text-align: center; color: #94a3b8;">
                    Run prediction to see results
                </div>
                """)
                
                confidence_bar = gr.Label(label="Distortion Softmax Probabilities", num_top_classes=5)

    gr.HTML("""<div style="height: 30px;"></div>""")
    
    gr.Markdown("""
    ## 🔌 Consuming the REST API in Your Product
    
    This space runs a **fully active FastAPI backend**. You can query it programmatically from your portfolio, website, or app:
    
    *   **Base URL:** `https://<your-username>-<your-space-name>.hf.space`
    *   **Health Check Endpoint:** <span class="endpoint-badge">GET /health</span>
    *   **Prediction Endpoint:** <span class="endpoint-badge">POST /predict</span>
    *   **API Docs:** [Interactive Swagger Documentation](docs)
    
    ### API Request Example (JavaScript / Fetch):
    ```javascript
    fetch("https://your-username-your-space-name.hf.space/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: "Your thought here..." })
    })
    .then(res => res.json())
    .then(data => console.log(data));
    ```
    """)
    
    # Example button callback mappings
    ex_catastrophizing.click(
        fn=lambda: "If I fail this exam, my entire life will be ruined and I will never get a job.",
        outputs=input_text
    )
    ex_filter.click(
        fn=lambda: "My friend didn't reply to my text for three hours. They definitely hate me.",
        outputs=input_text
    )
    ex_should.click(
        fn=lambda: "I should never make mistakes at work. If I make a mistake, I am useless.",
        outputs=input_text
    )
    
    # Model execution helper
    @spaces.GPU
    def analyze_thought(text):

        if not text or not text.strip():
            return "Please type or select a thought to analyze.", {}
            
        try:
            model_dir = os.environ.get("MODEL_DIR", "./MentalHealth_AI_Model")
            predictor = CognitiveDistortionPredictor.get_instance(model_dir)
            res = predictor.predict(text)
            
            label_id = res["label_id"]
            confidence = res["confidence"]
            latency_ms = res["latency_ms"]
            probs = res["probabilities"]
            
            details = DISTORTIONS_MAP.get(label_id)
            if details is None:
                return f"Error: Label ID {label_id} not found.", {}
                
            all_probs_named = {
                DISTORTIONS_MAP[idx]["name"]: float(prob) for idx, prob in probs.items()
            }
            
            # Format custom HTML result
            emoji_map = {
                "Catastrophizing": "🌋",
                "Mental Filter": "🔍",
                "Neutral": "⚖️",
                "Personalization": "🪞",
                "Should Statements": "📏"
            }
            emoji = emoji_map.get(details['name'], "🧠")
            
            reframing_questions_html = "".join([
                f'<div style="background: rgba(15,23,42,0.6); margin: 0.5rem 0; padding: 0.75rem 1rem; border-left: 3px solid #38bdf8; border-radius: 8px; font-weight: 500; font-size: 0.95rem;">Q{i}: {q}</div>'
                for i, q in enumerate(details["reframing_questions"], 1)
            ])
            
            html_result = f"""
            <div style="background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 20px; padding: 1.5rem; text-align: left; box-shadow: 0 10px 25px rgba(56,189,248,0.08);">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 0.75rem; margin-bottom: 1rem;">
                    <div>
                        <span style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 9999px; padding: 0.25rem 0.75rem; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">{details['name']}</span>
                        <h3 style="margin: 0.5rem 0 0 0; font-size: 1.4rem; color: #f8fafc; font-weight: 700;">{emoji} {details['name']}</h3>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 0.75rem; color: #94a3b8; font-weight: 600; display: block; text-transform: uppercase;">Confidence</span>
                        <strong style="color: #38bdf8; font-size: 1.3rem; font-weight: 800;">{confidence:.1%}</strong>
                    </div>
                </div>
                
                <p style="color: #cbd5e1; font-size: 0.95rem; margin: 0 0 1rem 0; line-height: 1.5;">{details['description']}</p>
            """
            
            if details['name'] != "Neutral":
                html_result += f"""
                <div style="margin-top: 1.25rem;">
                    <h4 style="margin: 0 0 0.5rem 0; color: #38bdf8; font-size: 0.95rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">💬 CBT Reframing Questions</h4>
                    {reframing_questions_html}
                </div>
                
                <div style="margin-top: 1.25rem; background: linear-gradient(135deg, rgba(14, 165, 233, 0.12), rgba(99, 102, 241, 0.12)); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 12px; padding: 1rem; color: #e2e8f0; font-size: 0.95rem; line-height: 1.5;">
                    <strong style="color: #38bdf8; display: block; margin-bottom: 0.25rem; font-size: 0.9rem;">💡 Clinical Advice:</strong>
                    {details['reframing_advice']}
                </div>
                """
            else:
                html_result += f"""
                <div style="margin-top: 1.25rem; background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.25); border-radius: 12px; padding: 1rem; color: #aade80; font-size: 0.95rem; line-height: 1.5; text-align: center;">
                    <strong>⚖️ Balanced Thought Detected</strong><br/>
                    Your thought process is grounded in objective reality. No cognitive distortions were found!
                </div>
                """
                
            html_result += f"""
                <div style="margin-top: 1rem; text-align: right; font-size: 0.75rem; color: #64748b;">
                    Inference latency: {latency_ms:.2f}ms
                </div>
            </div>
            """
            
            return html_result, all_probs_named
        except Exception as e:
            return f'<div style="color: #ef4444; padding: 1rem; border: 1px solid #ef4444; border-radius: 12px;">Error: {str(e)}</div>', {}

    submit_btn.click(fn=analyze_thought, inputs=input_text, outputs=[prediction_out, confidence_bar])

# 3. Mount Gradio interface to FastAPI app at the root "/" path with custom styling
app = gr.mount_gradio_app(
    fastapi_app, 
    demo, 
    path="/", 
    css=custom_css, 
    theme=gr.themes.Soft(primary_hue="sky")
)


if __name__ == "__main__":
    import uvicorn
    # Hugging Face Spaces runs on port 7860
    uvicorn.run("run:app", host="0.0.0.0", port=7860, reload=False)
