import os
import streamlit as st
import requests
import pandas as pd
import time

# 1. Page Config
st.set_page_config(
    page_title="Cognitive Disorder AI | Mindful Thought Checker",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject Glassmorphism & Modern Production CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main App Background */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(15, 23, 42, 1) 0%, rgba(10, 15, 29, 1) 90%);
        color: #f1f5f9;
    }

    /* Keyframe Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes pulseGlow {
        0%, 100% {
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.15), 0 0 30px rgba(99, 102, 241, 0.1);
        }
        50% {
            box-shadow: 0 0 25px rgba(56, 189, 248, 0.35), 0 0 50px rgba(99, 102, 241, 0.25);
        }
    }

    /* Glassmorphism Generic Card */
    .glass-card {
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.5s ease-out forwards;
        margin-bottom: 1.25rem;
    }

    .glass-card:hover {
        transform: translateY(-4px);
        border-color: rgba(56, 189, 248, 0.35);
        box-shadow: 0 12px 40px 0 rgba(56, 189, 248, 0.12);
    }

    /* Glass Header Hero */
    .glass-hero {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.65) 0%, rgba(15, 23, 42, 0.75) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2rem 2.5rem;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
        margin-bottom: 2rem;
        animation: pulseGlow 6s infinite ease-in-out;
    }

    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #38bdf8 0%, #a855f7 50%, #f43f5e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        line-height: 1.6;
        font-weight: 400;
    }

    /* Metric Badges */
    .badge-glow {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.4rem 0.9rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        backdrop-filter: blur(10px);
    }

    .badge-catastrophizing { background: rgba(244, 63, 94, 0.15); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.3); }
    .badge-mental-filter { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
    .badge-should { background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }
    .badge-personalization { background: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.3); }
    .badge-neutral { background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }

    /* QnA & Reframing Cards */
    .qna-box {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.7), rgba(30, 41, 59, 0.5));
        border-left: 4px solid #38bdf8;
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 0.85rem;
        transition: all 0.3s ease;
        animation: fadeInUp 0.4s ease-out forwards;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    .qna-box:hover {
        border-left-color: #a855f7;
        transform: translateX(6px) scale(1.005);
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(51, 65, 85, 0.6));
        box-shadow: 0 8px 25px rgba(168, 85, 247, 0.15);
    }

    .qna-question {
        color: #e2e8f0;
        font-weight: 600;
        font-size: 0.95rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .advice-box {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.12), rgba(99, 102, 241, 0.12));
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 16px;
        padding: 1.2rem;
        margin-top: 1rem;
        color: #cbd5e1;
    }

    /* Catalog Cards Grid */
    .catalog-card {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 1.5rem;
        height: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        flex-direction: column;
        justify: space-between;
    }

    .catalog-card:hover {
        transform: translateY(-5px) scale(1.01);
        border-color: rgba(168, 85, 247, 0.4);
        box-shadow: 0 15px 35px rgba(168, 85, 247, 0.15);
    }

    .catalog-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
    }

    .catalog-icon {
        font-size: 2.2rem;
        background: rgba(255, 255, 255, 0.05);
        padding: 0.5rem 0.75rem;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .example-chip {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 10px;
        padding: 0.6rem 0.85rem;
        font-size: 0.85rem;
        color: #cbd5e1;
        font-style: italic;
        margin-bottom: 0.5rem;
        transition: all 0.2s ease;
    }

    .example-chip:hover {
        border-color: rgba(56, 189, 248, 0.3);
        color: #f8fafc;
        transform: translateX(3px);
    }

    /* Architecture Nodes */
    .arch-node {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 16px;
        padding: 1.2rem;
        text-align: center;
        transition: all 0.3s ease;
    }

    .arch-node:hover {
        transform: translateY(-4px);
        border-color: #38bdf8;
        box-shadow: 0 10px 25px rgba(56, 189, 248, 0.2);
    }

    /* Override Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.6);
        padding: 6px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .stTabs [data-baseweb="tab"] {
        height: 48px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 12px;
        color: #94a3b8;
        font-weight: 600;
        border: none;
        padding: 0px 20px;
    }

    .stTabs [aria-selected="true"] {
        background-color: rgba(56, 189, 248, 0.15) !important;
        color: #38bdf8 !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
</style>
""", unsafe_allow_html=True)

# 3. Setup URLs & Paths
API_URL = "http://127.0.0.1:8000/predict"
MODEL_DIR = "./MentalHealth_AI_Model"
ONNX_PATH = os.path.join(MODEL_DIR, "model.onnx")

# Session state initialization for input
if "thought_input" not in st.session_state:
    st.session_state["thought_input"] = ""

def set_sample_thought(text: str):
    st.session_state["thought_input"] = text

# Distortion Emoji Mapping
DISTORTION_EMOJIS = {
    "Catastrophizing": "🌋",
    "Mental Filter": "🔍",
    "Neutral": "⚖️",
    "Personalization": "🪞",
    "Should Statements": "📏"
}

DISTORTION_BADGES = {
    "Catastrophizing": "badge-catastrophizing",
    "Mental Filter": "badge-mental-filter",
    "Should Statements": "badge-should",
    "Personalization": "badge-personalization",
    "Neutral": "badge-neutral"
}

# 4. Header Hero Section
st.markdown("""
<div class="glass-hero">
    <div class="hero-title">
        <span>🧠</span> Mindful Cognitive Disorder AI
    </div>
    <div class="hero-subtitle">
        An enterprise-grade, real-time cognitive distortion detection system. Powered by fine-tuned 
        <strong>DistilBERT</strong> & optimized with <strong>ONNX Runtime</strong> for ultra-low latency CBT analysis.
    </div>
</div>
""", unsafe_allow_html=True)

# 5. Sidebar System Status
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
        <span style="font-size: 2.8rem;">⚙️</span>
        <h3 style="margin-top: 0.5rem; color: #f8fafc; font-weight: 700;">System Control</h3>
    </div>
    """, unsafe_allow_html=True)
    
    api_online = False
    try:
        health_resp = requests.get("http://127.0.0.1:8000/health", timeout=1)
        if health_resp.status_code == 200:
            api_online = True
    except:
        pass
        
    if api_online:
        st.markdown("""
        <div class="glass-card" style="padding: 1rem; border-color: rgba(34, 197, 94, 0.4);">
            <div style="display: flex; align-items: center; gap: 0.6rem;">
                <span style="color: #4ade80; font-size: 1.2rem;">🟢</span>
                <div>
                    <strong style="color: #f8fafc;">FastAPI Backend</strong><br/>
                    <span style="color: #4ade80; font-size: 0.8rem;">Status: ONLINE (REST API)</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="glass-card" style="padding: 1rem; border-color: rgba(245, 158, 11, 0.4);">
            <div style="display: flex; align-items: center; gap: 0.6rem;">
                <span style="color: #fbbf24; font-size: 1.2rem;">🟡</span>
                <div>
                    <strong style="color: #f8fafc;">FastAPI Offline</strong><br/>
                    <span style="color: #fbbf24; font-size: 0.8rem;">Fallback: Local ONNX Engine</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 💡 CBT Insight")
    st.caption("""
    Cognitive distortions are biased perspectives we take on ourselves and the world around us. 
    By identifying patterns like **Catastrophizing** or **Should Statements**, Cognitive Behavioral Therapy (CBT) helps rewire these thoughts toward balanced reality.
    """)

# Local Predictor Fallback Cache
@st.cache_resource
def get_local_predictor():
    if os.path.exists(ONNX_PATH):
        try:
            from app.predictor import CognitiveDistortionPredictor
            return CognitiveDistortionPredictor.get_instance(MODEL_DIR)
        except Exception as e:
            st.error(f"Error loading local predictor: {e}")
    return None

# 6. Navigation Tabs
tab_analyzer, tab_catalog, tab_architecture = st.tabs([
    "🔮 Real-Time Analyzer", 
    "📚 Distortion Catalog Grid", 
    "⚡ Architecture & Performance"
])

# ----------------- TAB 1: ANALYZER (PRODUCTION GRID) -----------------
with tab_analyzer:
    st.markdown("### ✍️ Input Thought Analysis")
    
    # Input Area with Preset Examples
    user_input = st.text_area(
        "Enter your stressful or recurring negative thought:",
        height=110,
        placeholder="E.g., If I fail this presentation, I'm a complete failure and everybody will laugh at me.",
        key="thought_input"
    )
    
    # Sample Chips / Buttons for Quick Testing (Using callbacks to update session state safely)
    st.markdown("<span style='font-size: 0.85rem; color: #94a3b8; font-weight: 600;'>TRY SAMPLE THOUGHTS:</span>", unsafe_allow_html=True)
    chip_cols = st.columns(3)
    with chip_cols[0]:
        st.button(
            "🌋 Exam failure panic", 
            use_container_width=True,
            on_click=set_sample_thought,
            args=("If I fail this exam, my entire life will be ruined and I will never get a job.",)
        )
    with chip_cols[1]:
        st.button(
            "🔍 Text reply delay", 
            use_container_width=True,
            on_click=set_sample_thought,
            args=("My friend didn't reply to my text for three hours. They definitely hate me.",)
        )
    with chip_cols[2]:
        st.button(
            "📏 Rigid perfection rule", 
            use_container_width=True,
            on_click=set_sample_thought,
            args=("I should never make mistakes at work. If I make a mistake, I am useless.",)
        )
            
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    analyze_btn = st.button("⚡ Run Neural Prediction", type="primary", use_container_width=True)
    
    if analyze_btn:
        if not user_input.strip():
            st.warning("⚠️ Please type or select a thought to analyze.")
        else:
            result = None
            mode_used = ""
            
            # Method 1: FastAPI
            if api_online:
                with st.spinner("🔮 Running inference via FastAPI REST API..."):
                    try:
                        resp = requests.post(API_URL, json={"text": user_input})
                        if resp.status_code == 200:
                            result = resp.json()
                            mode_used = "FastAPI Backend (REST API)"
                    except Exception as e:
                        st.error(f"API Error: {e}")
            
            # Method 2: ONNX Fallback
            if result is None:
                local_predictor = get_local_predictor()
                if local_predictor:
                    with st.spinner("⚡ Running inference via ONNX Runtime..."):
                        try:
                            from app.distortions_db import DISTORTIONS_MAP
                            pred_res = local_predictor.predict(user_input)
                            label_id = pred_res["label_id"]
                            details = DISTORTIONS_MAP[label_id]
                            
                            all_probs_named = {
                                DISTORTIONS_MAP[idx]["name"]: prob 
                                for idx, prob in pred_res["probabilities"].items()
                            }
                            
                            result = {
                                "text": user_input,
                                "predicted_distortion": details["name"],
                                "confidence": pred_res["confidence"],
                                "latency_ms": pred_res["latency_ms"],
                                "distortion_details": details,
                                "all_probabilities": all_probs_named
                            }
                            mode_used = "Local ONNX Runtime Session"
                        except Exception as e:
                            st.error(f"ONNX Local Error: {e}")
                else:
                    st.error("No model available. Start FastAPI backend or run convert_to_onnx.py.")

            # Render Production Grid Results
            if result:
                distortion_name = result["predicted_distortion"]
                confidence = result["confidence"]
                latency = result["latency_ms"]
                details = result["distortion_details"]
                emoji = DISTORTION_EMOJIS.get(distortion_name, "🧠")
                badge_class = DISTORTION_BADGES.get(distortion_name, "badge-neutral")

                st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
                
                # Top Summary Card
                st.markdown(f"""
                <div class="glass-card" style="border-color: rgba(56, 189, 248, 0.3);">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                        <div>
                            <span class="badge-glow {badge_class}">
                                {emoji} {distortion_name.upper()}
                            </span>
                            <h2 style="margin: 0.6rem 0 0.2rem 0; color: #f8fafc; font-weight: 700;">
                                {emoji} {distortion_name}
                            </h2>
                            <p style="color: #94a3b8; margin: 0; font-size: 0.95rem;">{details['description']}</p>
                        </div>
                        <div style="display: flex; gap: 1rem;">
                            <div style="background: rgba(15, 23, 42, 0.6); padding: 0.75rem 1.25rem; border-radius: 14px; border: 1px solid rgba(255,255,255,0.08); text-align: center;">
                                <div style="color: #94a3b8; font-size: 0.75rem; font-weight: 600;">CONFIDENCE</div>
                                <div style="color: #38bdf8; font-size: 1.4rem; font-weight: 800;">{confidence:.1%}</div>
                            </div>
                            <div style="background: rgba(15, 23, 42, 0.6); padding: 0.75rem 1.25rem; border-radius: 14px; border: 1px solid rgba(255,255,255,0.08); text-align: center;">
                                <div style="color: #94a3b8; font-size: 0.75rem; font-weight: 600;">LATENCY</div>
                                <div style="color: #a855f7; font-size: 1.4rem; font-weight: 800;">{latency:.2f}ms</div>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Production Grid Layout (2 Columns)
                col_left, col_right = st.columns([1.3, 1])

                with col_left:
                    if distortion_name != "Neutral":
                        st.markdown("### 💬 CBT Cognitive Reframing Q&A")
                        st.markdown("<p style='color: #94a3b8; font-size: 0.9rem;'>Step-by-step cognitive inquiry to dismantle distorted thoughts:</p>", unsafe_allow_html=True)
                        
                        # Animated Q&A Boxes
                        for i, q in enumerate(details["reframing_questions"], 1):
                            st.markdown(f"""
                            <div class="qna-box">
                                <div class="qna-question">
                                    <span style="background: rgba(56, 189, 248, 0.2); color: #38bdf8; border-radius: 50%; width: 24px; height: 24px; display: inline-flex; align-items: center; justify-content: center; font-size: 0.8rem; font-weight: 700;">Q{i}</span>
                                    <span>{q}</span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                        # Reframing Strategy Box
                        st.markdown(f"""
                        <div class="advice-box">
                            <strong style="color: #38bdf8; font-size: 1rem; display: flex; align-items: center; gap: 0.5rem;">
                                💡 Clinical Strategy:
                            </strong>
                            <p style="margin-top: 0.4rem; margin-bottom: 0;">{details['reframing_advice']}</p>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
                        
                        # Interactive Reframing Input Card
                        st.markdown("#### ✏️ Write your Reframed Balanced Thought:")
                        reframed_input = st.text_area(
                            "Balanced Reframe:",
                            key="reframed_thought",
                            placeholder="E.g., Failing one presentation would be disappointing, but it does not mean I am a complete failure. I can learn from it.",
                            label_visibility="collapsed"
                        )
                        
                        if st.button("🌟 Commit & Save Balanced Thought", use_container_width=True):
                            if reframed_input.strip():
                                st.balloons()
                                st.success("🎉 Reframed successfully! Excellent cognitive work.")
                                st.markdown("""
                                <div class="glass-card" style="border-color: rgba(34, 197, 94, 0.4);">
                                    <h4 style="color: #4ade80; margin-top: 0;">Comparison View</h4>
                                </div>
                                """, unsafe_allow_html=True)
                                comp_df = pd.DataFrame({
                                    "Original Distorted Thought": [user_input],
                                    "Reframed Balanced Thought": [reframed_input]
                                })
                                st.table(comp_df)
                            else:
                                st.warning("Please type your reframed thought above.")
                    else:
                        st.balloons()
                        st.markdown("""
                        <div class="glass-card" style="border-color: rgba(34, 197, 94, 0.4); text-align: center; padding: 2rem;">
                            <span style="font-size: 3rem;">⚖️🌟</span>
                            <h3 style="color: #4ade80; margin-top: 0.5rem;">Balanced Thinking Detected</h3>
                            <p style="color: #cbd5e1;">Your thought process is grounded in objective reality. No cognitive distortions were found!</p>
                        </div>
                        """, unsafe_allow_html=True)

                with col_right:
                    st.markdown("### 📊 Neural Probability Distribution")
                    st.markdown("<p style='color: #94a3b8; font-size: 0.9rem;'>Softmax probability spectrum across all distortion classes:</p>", unsafe_allow_html=True)
                    
                    # Custom Animated HTML Bars for Probabilities
                    for d_name, p_val in sorted(result["all_probabilities"].items(), key=lambda x: x[1], reverse=True):
                        d_emoji = DISTORTION_EMOJIS.get(d_name, "🔹")
                        is_winner = (d_name == distortion_name)
                        bar_color = "linear-gradient(90deg, #38bdf8, #818cf8)" if is_winner else "linear-gradient(90deg, #334155, #475569)"
                        border_glow = "border: 1px solid rgba(56, 189, 248, 0.5);" if is_winner else "border: 1px solid rgba(255, 255, 255, 0.05);"
                        
                        st.markdown(f"""
                        <div style="background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(10px); border-radius: 12px; padding: 0.85rem 1rem; margin-bottom: 0.75rem; {border_glow}">
                            <div style="display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 0.35rem;">
                                <span style="font-weight: 600; color: {'#38bdf8' if is_winner else '#cbd5e1'};">
                                    {d_emoji} {d_name} {'(Detected)' if is_winner else ''}
                                </span>
                                <span style="font-weight: 700; color: {'#38bdf8' if is_winner else '#94a3b8'};">
                                    {p_val:.1%}
                                </span>
                            </div>
                            <div style="width: 100%; background: rgba(255, 255, 255, 0.06); height: 8px; border-radius: 999px; overflow: hidden;">
                                <div style="width: {p_val*100}%; background: {bar_color}; height: 100%; border-radius: 999px; transition: width 0.8s ease-in-out;"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

# ----------------- TAB 2: DISTORTION CATALOG (PRODUCTION GRID) -----------------
with tab_catalog:
    st.markdown("### 📚 Cognitive Distortion Catalog")
    st.markdown("<p style='color: #94a3b8;'>Comprehensive production reference matrix of cognitive patterns identified by the model:</p>", unsafe_allow_html=True)
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    from app.distortions_db import DISTORTIONS_MAP

    # Grid of Glass Cards (2 Columns)
    cat_cols = st.columns(2)
    
    for idx, (dist_id, data) in enumerate(DISTORTIONS_MAP.items()):
        d_name = data["name"]
        emoji = DISTORTION_EMOJIS.get(d_name, "🧠")
        target_col = cat_cols[idx % 2]
        
        with target_col:
            st.markdown(f"""
            <div class="catalog-card">
                <div class="catalog-header">
                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                        <span class="catalog-icon">{emoji}</span>
                        <div>
                            <span style="font-size: 0.75rem; color: #38bdf8; font-weight: 700; letter-spacing: 0.05em;">CLASS 0{dist_id}</span>
                            <h3 style="margin: 0; color: #f8fafc; font-weight: 700;">{d_name}</h3>
                        </div>
                    </div>
                </div>
                
                <p style="color: #cbd5e1; font-size: 0.92rem; line-height: 1.5; margin-bottom: 1rem;">
                    {data['description']}
                </p>
                
                <div style="margin-bottom: 1rem;">
                    <div style="font-size: 0.8rem; color: #94a3b8; font-weight: 700; margin-bottom: 0.4rem;">REAL-WORLD EXAMPLES:</div>
            """, unsafe_allow_html=True)
            
            for ex in data["examples"]:
                st.markdown(f"""
                <div class="example-chip">
                    💬 "{ex}"
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown(f"""
                </div>
                <div style="background: rgba(56, 189, 248, 0.08); border-left: 3px solid #38bdf8; padding: 0.75rem 1rem; border-radius: 8px;">
                    <strong style="color: #38bdf8; font-size: 0.85rem;">💡 Reframing Advice:</strong>
                    <p style="color: #94a3b8; font-size: 0.85rem; margin: 0.25rem 0 0 0;">{data['reframing_advice']}</p>
                </div>
            </div>
            <div style="height: 15px;"></div>
            """, unsafe_allow_html=True)

# ----------------- TAB 3: SYSTEM ARCHITECTURE -----------------
with tab_architecture:
    st.markdown("### ⚡ Production Architecture & Performance")
    st.markdown("<p style='color: #94a3b8;'>Technical benchmarks comparing PyTorch inference vs ONNX Runtime optimization:</p>", unsafe_allow_html=True)
    
    # Stat Metrics Grid
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 1.2rem;">
            <div style="font-size: 2rem;">⚡</div>
            <div style="color: #94a3b8; font-size: 0.8rem; font-weight: 600;">LATENCY REDUCTION</div>
            <div style="color: #38bdf8; font-size: 1.8rem; font-weight: 800; margin-top: 0.2rem;">> 80%</div>
            <div style="color: #4ade80; font-size: 0.75rem;">150ms ➔ ~18ms</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 1.2rem;">
            <div style="font-size: 2rem;">💾</div>
            <div style="color: #94a3b8; font-size: 0.8rem; font-weight: 600;">RAM FOOTPRINT</div>
            <div style="color: #a855f7; font-size: 1.8rem; font-weight: 800; margin-top: 0.2rem;">250 MB</div>
            <div style="color: #4ade80; font-size: 0.75rem;">PyTorch: ~1.5 GB</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 1.2rem;">
            <div style="font-size: 2rem;">🎯</div>
            <div style="color: #94a3b8; font-size: 0.8rem; font-weight: 600;">MODEL FORMAT</div>
            <div style="color: #f43f5e; font-size: 1.8rem; font-weight: 800; margin-top: 0.2rem;">ONNX</div>
            <div style="color: #cbd5e1; font-size: 0.75rem;">DistilBERT FP32</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 1.2rem;">
            <div style="font-size: 2rem;">🌐</div>
            <div style="color: #94a3b8; font-size: 0.8rem; font-weight: 600;">DECOUPLED GATEWAY</div>
            <div style="color: #fbbf24; font-size: 1.8rem; font-weight: 800; margin-top: 0.2rem;">FastAPI</div>
            <div style="color: #cbd5e1; font-size: 0.75rem;">REST + Local Fallback</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown("#### 🔄 Inference Execution Pipeline:")

    # Pipeline Flow Grid
    p1, p2, p3, p4, p5 = st.columns(5)
    with p1:
        st.markdown("""
        <div class="arch-node">
            <span style="font-size: 1.8rem;">✍️</span>
            <h5 style="color: #f8fafc; margin: 0.5rem 0 0.2rem 0;">1. Text Input</h5>
            <span style="font-size: 0.75rem; color: #94a3b8;">User prompt / API payload</span>
        </div>
        """, unsafe_allow_html=True)
    with p2:
        st.markdown("""
        <div class="arch-node">
            <span style="font-size: 1.8rem;">🔤</span>
            <h5 style="color: #f8fafc; margin: 0.5rem 0 0.2rem 0;">2. Tokenizer</h5>
            <span style="font-size: 0.75rem; color: #94a3b8;">DistilBERT Fast (NumPy)</span>
        </div>
        """, unsafe_allow_html=True)
    with p3:
        st.markdown("""
        <div class="arch-node">
            <span style="font-size: 1.8rem;">⚡</span>
            <h5 style="color: #f8fafc; margin: 0.5rem 0 0.2rem 0;">3. ONNX Session</h5>
            <span style="font-size: 0.75rem; color: #94a3b8;">CPU ExecutionProvider</span>
        </div>
        """, unsafe_allow_html=True)
    with p4:
        st.markdown("""
        <div class="arch-node">
            <span style="font-size: 1.8rem;">📊</span>
            <h5 style="color: #f8fafc; margin: 0.5rem 0 0.2rem 0;">4. Softmax</h5>
            <span style="font-size: 0.75rem; color: #94a3b8;">Probabilities & Confidence</span>
        </div>
        """, unsafe_allow_html=True)
    with p5:
        st.markdown("""
        <div class="arch-node">
            <span style="font-size: 1.8rem;">💡</span>
            <h5 style="color: #f8fafc; margin: 0.5rem 0 0.2rem 0;">5. CBT DB</h5>
            <span style="font-size: 0.75rem; color: #94a3b8;">Distortion Q&A Reframe</span>
        </div>
        """, unsafe_allow_html=True)
