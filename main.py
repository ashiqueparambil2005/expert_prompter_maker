import streamlit as st
import google.generativeai as genai
from PIL import Image
import time
from datetime import datetime
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="Ultra Studio V13 Pro",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Ultra Modern CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Manrope:wght@400;500;600;700;800&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Inter', sans-serif;
    }
    
    /* === LOGIN PAGE === */
    .login-container {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    .login-box {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 32px;
        padding: 3rem 2.5rem;
        max-width: 480px;
        width: 100%;
        box-shadow: 0 30px 90px rgba(0, 0, 0, 0.2);
        animation: slideUp 0.5s ease-out;
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .login-logo {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .login-logo-icon {
        font-size: 4em;
        margin-bottom: 1rem;
        display: inline-block;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .login-title {
        font-size: 2.5em;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        font-family: 'Manrope', sans-serif;
    }
    
    .login-subtitle {
        color: #64748b;
        font-size: 1.1em;
        margin-bottom: 2rem;
    }
    
    /* === MAIN APP === */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .main {
        padding: 0;
        max-width: 100%;
    }
    
    /* === NAVBAR === */
    .navbar {
        background: white;
        padding: 1rem 3rem;
        box-shadow: 0 2px 20px rgba(0, 0, 0, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: sticky;
        top: 0;
        z-index: 1000;
        margin-bottom: 2rem;
    }
    
    .navbar-brand {
        font-size: 1.8em;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Manrope', sans-serif;
    }
    
    .navbar-stats {
        display: flex;
        gap: 2rem;
        align-items: center;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-value {
        font-size: 1.5em;
        font-weight: 700;
        color: #667eea;
    }
    
    .stat-label {
        font-size: 0.85em;
        color: #64748b;
        margin-top: 0.2rem;
    }
    
    /* === HERO SECTION === */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 32px;
        padding: 4rem 3rem;
        margin: 0 3rem 3rem 3rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .hero-title {
        font-size: 3.5em;
        font-weight: 900;
        color: white;
        margin-bottom: 1rem;
        position: relative;
        z-index: 1;
        font-family: 'Manrope', sans-serif;
    }
    
    .hero-subtitle {
        font-size: 1.3em;
        color: rgba(255, 255, 255, 0.95);
        margin-bottom: 2rem;
        position: relative;
        z-index: 1;
    }
    
    .hero-features {
        display: flex;
        justify-content: center;
        gap: 3rem;
        margin-top: 2rem;
        position: relative;
        z-index: 1;
    }
    
    .hero-feature {
        color: white;
        font-size: 1.1em;
    }
    
    .hero-feature-icon {
        font-size: 2em;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    /* === TABS === */
    .stTabs {
        background: white;
        border-radius: 24px;
        padding: 2rem;
        margin: 0 3rem 3rem 3rem;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.08);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: #f8f9fa;
        border-radius: 16px;
        padding: 0.5rem;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px !important;
        padding: 1rem 2rem !important;
        font-weight: 600 !important;
        color: #64748b !important;
        border: none !important;
        font-size: 1.05em !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    /* === CARDS === */
    .feature-card {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        border: 2px solid #f1f5f9;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.15);
        border-color: #667eea;
    }
    
    /* === INPUT FIELDS === */
    .stTextArea textarea, .stTextInput input {
        border-radius: 16px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1) !important;
        outline: none !important;
    }
    
    /* === BUTTONS === */
    .stButton button {
        border-radius: 14px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1.05em !important;
        border: none !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15) !important;
    }
    
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    .stButton button[kind="secondary"] {
        background: white !important;
        border: 2px solid #e2e8f0 !important;
        color: #475569 !important;
    }
    
    /* === SELECT BOXES === */
    .stSelectbox > div > div {
        border-radius: 14px !important;
        border: 2px solid #e2e8f0 !important;
    }
    
    /* === FILE UPLOADER === */
    [data-testid="stFileUploader"] {
        border-radius: 20px !important;
        border: 3px dashed #cbd5e1 !important;
        padding: 2rem !important;
        background: #f8f9fa !important;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #667eea !important;
        background: white !important;
    }
    
    /* === PROGRESS BAR === */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        border-radius: 10px !important;
    }
    
    /* === ALERTS === */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 16px !important;
        padding: 1.2rem !important;
        border-left: 4px solid !important;
        animation: slideIn 0.3s ease;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* === EXPANDER === */
    .streamlit-expanderHeader {
        border-radius: 14px !important;
        background: white !important;
        font-weight: 600 !important;
        padding: 1.2rem !important;
        border: 2px solid #e2e8f0 !important;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: #667eea !important;
        background: #f8f9ff !important;
    }
    
    /* === IMAGE DISPLAY === */
    [data-testid="stImage"] {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    /* === HIDE DEFAULTS === */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    
    /* === RESPONSIVE === */
    @media (max-width: 768px) {
        .hero-title { font-size: 2em; }
        .navbar { padding: 1rem; }
        .stTabs { margin: 0 1rem 1rem 1rem; }
        .hero-section { margin: 0 1rem 1rem 1rem; padding: 2rem 1.5rem; }
        .hero-features { flex-direction: column; gap: 1rem; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- Initialize Session State ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'generated_prompts' not in st.session_state:
    st.session_state.generated_prompts = []
if 'api_calls_count' not in st.session_state:
    st.session_state.api_calls_count = 0
if 'img_description' not in st.session_state:
    st.session_state.img_description = ''
if 'last_image_gen_time' not in st.session_state:
    st.session_state.last_image_gen_time = 0

# --- Camera Angles Database ---
CAMERA_ANGLES = {
    "Basic Angles": [
        ("📷 Front View", "front view, direct facing camera, eye-level shot, straight-on angle"),
        ("👤 Side View (Profile)", "side view, 90 degree profile shot, capturing silhouette, lateral perspective"),
        ("🔄 Back View", "back view, rear angle, behind the subject, over-the-back shot"),
        ("🎯 Three-Quarter View", "three-quarter view, 45 degree angle, dynamic composition, semi-profile"),
    ],
    
    "Vertical Angles": [
        ("🦅 Top View (Bird's Eye)", "top view, bird's eye perspective, overhead angle, aerial shot"),
        ("⬇️ Low Angle (Worm's Eye)", "low angle, camera looking up, worm's eye view, dramatic upward perspective"),
        ("⬆️ High Angle", "high angle, camera looking down, god's eye view, downward perspective"),
        ("👁️ Eye Level", "eye level shot, neutral angle, human perspective, natural viewpoint"),
        ("🏔️ Dutch Angle (Tilted)", "dutch angle, tilted camera, canted angle, off-kilter perspective"),
    ],
    
    "Distance/Framing": [
        ("🔍 Extreme Close-Up (ECU)", "extreme close-up, macro detail, intimate framing, focus on specific feature"),
        ("😊 Close-Up (CU)", "close-up shot, head and shoulders, facial expressions, emotional detail"),
        ("👤 Medium Close-Up (MCU)", "medium close-up, chest up, personal shot, conversational framing"),
        ("🧍 Medium Shot (MS)", "medium shot, waist up, half body, standard framing"),
        ("🚶 Medium Wide Shot", "medium wide shot, knees up, three-quarter body, contextual framing"),
        ("🌄 Wide Shot (WS)", "wide shot, full body, establishing shot, showing environment"),
        ("🌍 Extreme Wide Shot (EWS)", "extreme wide shot, landscape view, vast scene, environmental context"),
    ],
    
    "Movement Shots": [
        ("🎬 Tracking Shot", "tracking shot, following movement, dynamic camera, smooth motion"),
        ("🔄 Pan Shot", "panning shot, horizontal movement, sweeping view, side-to-side motion"),
        ("⬆️⬇️ Tilt Shot", "tilting shot, vertical movement, up-down motion, revealing shot"),
        ("🎪 Dolly Shot", "dolly shot, camera moving forward/backward, approaching/receding, depth motion"),
        ("🎢 Crane Shot", "crane shot, elevated movement, swooping motion, dramatic reveal"),
        ("🚁 Aerial/Drone Shot", "aerial shot, drone perspective, flyover view, sky-level filming"),
    ],
    
    "POV & Perspective": [
        ("👔 Over-The-Shoulder (OTS)", "over the shoulder perspective, conversation angle, immersive POV"),
        ("👁️ Point of View (POV)", "point of view shot, first-person perspective, subjective camera, character's vision"),
        ("🪞 Reverse Angle", "reverse angle, opposite perspective, reaction shot, counter view"),
        ("🎭 Two-Shot", "two-shot, both subjects in frame, relationship composition, dual focus"),
        ("👥 Group Shot", "group shot, multiple subjects, ensemble framing, collective view"),
    ],
    
    "Creative/Artistic": [
        ("🎨 Symmetrical Composition", "symmetrical composition, balanced frame, centered subject, mirrored perspective"),
        ("🌟 Leading Lines", "leading lines composition, directional framing, guiding perspective, depth creation"),
        ("🖼️ Frame Within Frame", "frame within frame, layered composition, bordered subject, nested perspective"),
        ("🔲 Rule of Thirds", "rule of thirds composition, off-center framing, balanced asymmetry, grid placement"),
        ("🌀 Spiral/Circular", "spiral composition, circular framing, rotating perspective, vortex view"),
        ("🪟 Through Glass/Reflection", "through glass shot, reflection angle, layered reality, transparent barrier"),
        ("🌫️ Silhouette Shot", "silhouette shot, backlit subject, shadow composition, contrast perspective"),
        ("💡 Lens Flare Shot", "lens flare composition, light burst, dramatic lighting, cinematic glow"),
    ],
    
    "Specialty Shots": [
        ("🎯 Rack Focus", "rack focus shot, changing focal plane, depth transition, selective clarity"),
        ("🌊 Underwater Shot", "underwater perspective, aquatic view, submerged angle, liquid environment"),
        ("🔬 Macro/Microscopic", "macro shot, microscopic view, extreme detail, tiny subject magnified"),
        ("📱 Screen/Monitor POV", "screen perspective, monitor view, digital display angle, tech interface"),
        ("🎪 Fisheye/Wide Lens", "fisheye perspective, ultra-wide angle, distorted view, 180-degree vision"),
        ("🎭 Split Screen", "split screen composition, dual perspective, parallel view, divided frame"),
        ("⏱️ Time-Lapse Angle", "time-lapse perspective, compressed time, motion blur, temporal view"),
        ("🎬 Whip Pan", "whip pan shot, fast horizontal movement, blur transition, dynamic sweep"),
    ]
}

# --- Helper Functions ---
def safe_generate(prompt, model):
    """Safe API call with error handling"""
    if model is None:
        return "🎮 **Demo Mode Active**\n\nThis is a preview of what the AI would generate. To use real AI features, please:\n1. Logout\n2. Get a free API key from ai.google.dev\n3. Login with your API key\n\n[Sample output would appear here]"
    
    try:
        response = model.generate_content(prompt)
        st.session_state.api_calls_count += 1
        return response.text.strip()
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "ResourceExhausted" in error_msg:
            return "⏳ Rate limit reached. Please wait 60 seconds."
        elif "quota" in error_msg.lower():
            return "💳 API quota exceeded."
        elif "invalid" in error_msg.lower():
            return "🔑 Invalid API key."
        else:
            return f"⚠️ Error: {error_msg}"

def analyze_image(image_file, model):
    """Analyze uploaded image"""
    if model is None:
        return "🎮 **Demo Mode** - Image analysis not available. Login with API key to use this feature."
    
    try:
        img = Image.open(image_file)
        if max(img.size) > 1024:
            img.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
        
        prompt = """Analyze this image for AI video generation. Describe:
        1. Physical appearance (face, features, expressions)
        2. Hair (style, color, length)
        3. Clothing and accessories
        4. Age range and gender
        5. Overall style and vibe
        
        Be specific and concise for AI prompts."""
        
        response = model.generate_content([prompt, img])
        st.session_state.api_calls_count += 1
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Analysis failed: {str(e)}"

def split_dialogue(text, max_words=15):
    """Split dialogue into clips"""
    if not text:
        return []
    
    sentences = text.replace('!', '.').replace('?', '.').split('.')
    sentences = [s.strip() for s in sentences if s.strip()]
    
    clips = []
    current = []
    word_count = 0
    
    for sentence in sentences:
        words = sentence.split()
        
        if len(words) > max_words:
            if current:
                clips.append(" ".join(current))
                current = []
                word_count = 0
            
            for i in range(0, len(words), max_words):
                clips.append(" ".join(words[i:i+max_words]))
        else:
            if word_count + len(words) > max_words:
                clips.append(" ".join(current))
                current = [sentence]
                word_count = len(words)
            else:
                current.append(sentence)
                word_count += len(words)
    
    if current:
        clips.append(" ".join(current))
    
    return clips

def generate_selected_angle_prompts(image_file, model, selected_angles, selected_style):
    """Generate video prompts for selected camera angles only"""
    try:
        if model is None:
            return None, "🎮 Demo Mode - Prompt generation requires a real API key."
        
        # Load and analyze image
        img = Image.open(image_file)
        if max(img.size) > 1024:
            img.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
        
        # Analyze image first
        st.info("📝 Analyzing image...")
        analysis_prompt = """Analyze this image and provide a detailed description for AI video generation prompts. Include:
        - Subject/character details (appearance, clothing, style)
        - Setting and environment
        - Mood and atmosphere
        - Colors and lighting
        - Any notable features
        
        Be specific and detailed."""
        
        try:
            analysis_response = model.generate_content([analysis_prompt, img])
            base_description = analysis_response.text.strip()
            st.session_state.api_calls_count += 1
            st.success(f"✅ Image analyzed successfully!")
        except Exception as ve:
            return None, f"⚠️ Image analysis failed: {str(ve)}"
        
        generated_prompts = []
        
        # Generate prompt for each selected angle
        for idx, angle_name in enumerate(selected_angles):
            # Find the angle description from database
            angle_description = ""
            for category, angles in CAMERA_ANGLES.items():
                for name, desc in angles:
                    if name == angle_name:
                        angle_description = desc
                        break
                if angle_description:
                    break
            
            st.info(f"🎬 Generating {angle_name} prompt ({idx+1}/{len(selected_angles)})...")
            
            # Create detailed video prompt
            prompt_template = f"""Create a professional AI video generation prompt for the following setup:

IMAGE ANALYSIS:
{base_description}

CAMERA ANGLE: {angle_name}
ANGLE DESCRIPTION: {angle_description}
VISUAL STYLE: {selected_style}

Generate a detailed video prompt that includes:
1. Character/subject description
2. Camera angle and movement specifications
3. Composition and framing details
4. Lighting setup and mood
5. Visual style and atmosphere
6. Technical specifications (resolution, aspect ratio if relevant)
7. Any motion or animation details
8. Color grading and post-processing notes

Format the prompt professionally for AI video tools like Runway ML, Pika Labs, or similar platforms.
Make it production-ready, specific, and detailed. Use cinematic terminology."""
            
            try:
                response = model.generate_content(prompt_template)
                prompt_text = response.text.strip()
                st.session_state.api_calls_count += 1
                
                generated_prompts.append({
                    'angle': angle_name,
                    'prompt': prompt_text
                })
                st.success(f"✅ {angle_name} prompt generated!")
                
            except Exception as prompt_error:
                st.warning(f"⚠️ {angle_name} prompt generation failed: {str(prompt_error)}")
            
            # Small delay between generations
            if idx < len(selected_angles) - 1:
                time.sleep(1)
        
        if generated_prompts:
            return generated_prompts, None
        else:
            return None, "No prompts were generated successfully."
        
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "ResourceExhausted" in error_msg:
            return None, "⏳ Rate limit reached. Please wait 60 seconds and try again."
        elif "quota" in error_msg.lower():
            return None, "💳 API quota exceeded."
        elif "invalid" in error_msg.lower():
            return None, "🔑 Invalid API key."
        else:
            return None, f"⚠️ Error: {error_msg}"


# --- LOGIN PAGE ---
if not st.session_state.logged_in:
    st.markdown("""
    <div class="login-container">
        <div class="login-box">
            <div class="login-logo">
                <div class="login-logo-icon">✨</div>
                <h1 class="login-title">Ultra Studio V13</h1>
                <p class="login-subtitle">Multi-Angle AI Generator</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            api_key_input = st.text_input(
                "Gemini API Key",
                type="password",
                placeholder="Enter your API key...",
                help="Get your free API key from ai.google.dev"
            )
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                login_button = st.form_submit_button("🚀 Login", use_container_width=True, type="primary")
            
            if login_button:
                if api_key_input.strip():
                    with st.spinner("🔍 Validating API key..."):
                        try:
                            # Test API key
                            genai.configure(api_key=api_key_input)
                            test_model = genai.GenerativeModel('gemini-3-flash-preview')
                            response = test_model.generate_content("Hi")
                            
                            # Success
                            st.session_state.logged_in = True
                            st.session_state.api_key = api_key_input
                            st.success("✅ Login successful! Redirecting...")
                            time.sleep(1.5)
                            st.rerun()
                            
                        except Exception as e:
                            error_msg = str(e)
                            if "API_KEY_INVALID" in error_msg or "invalid" in error_msg.lower():
                                st.error("❌ Invalid API key. Please verify your key from ai.google.dev")
                            elif "quota" in error_msg.lower():
                                st.error("❌ API quota exceeded. Please check your quota limits.")
                            elif "permission" in error_msg.lower():
                                st.error("❌ API key doesn't have required permissions.")
                            else:
                                st.error(f"❌ Connection failed: {error_msg}")
                            
                            st.info("💡 Make sure your API key is active at https://ai.google.dev")
                else:
                    st.warning("⚠️ Please enter your API key")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.markdown("**Don't have an API key?**")
        if st.button("🎮 Try Demo Mode", use_container_width=False, help="Explore the interface without API key"):
            st.session_state.logged_in = True
            st.session_state.api_key = "DEMO_MODE"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.expander("📖 How to get your API key", expanded=False):
            st.markdown("""
            **Quick Setup (30 seconds):**
            
            1. Visit [ai.google.dev](https://ai.google.dev)
            2. Sign in with Google account
            3. Click **"Get API Key"** in Gemini API
            4. Click **"Create API Key"**
            5. Copy your key
            6. Paste above and login
            
            **It's completely FREE!** 🎉
            """)
        
        with st.expander("❓ Troubleshooting", expanded=False):
            st.markdown("""
            **If login fails, check these:**
            
            ✅ API key is copied correctly (no extra spaces)
            
            ✅ API key is from [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
            
            ✅ Gemini API is enabled in your Google Cloud project
            
            ✅ You have internet connection
            
            ✅ Your API quota hasn't been exceeded
            
            **Still having issues?** The API key should look like:
            `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`
            """)
    
    st.stop()

# --- MAIN APPLICATION (After Login) ---

# Check if demo mode
is_demo = (st.session_state.api_key == "DEMO_MODE")

# Configure API (skip if demo mode)
if not is_demo:
    genai.configure(api_key=st.session_state.api_key)
    model = genai.GenerativeModel('gemini-3-flash-preview')
else:
    model = None
    st.warning("🎮 **Demo Mode** - You're exploring the interface. Enter a real API key to use AI features.", icon="ℹ️")

# --- NAVBAR ---
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("""
    <div class="navbar">
        <div class="navbar-brand">✨ Ultra Studio V13 Pro</div>
        <div class="navbar-stats">
            <div class="stat-item">
                <div class="stat-value">{}</div>
                <div class="stat-label">API Calls</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{}</div>
                <div class="stat-label">Prompts</div>
            </div>
        </div>
    </div>
    """.format(st.session_state.api_calls_count, len(st.session_state.generated_prompts)), unsafe_allow_html=True)

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Logout", key="logout", help="Logout from Ultra Studio"):
        st.session_state.logged_in = False
        st.session_state.api_key = ""
        st.rerun()

# --- HERO SECTION ---
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">Multi-Angle Video Prompt Generator</h1>
    <p class="hero-subtitle">Upload 1 Image → Select Your Camera Angles → Get Professional Prompts</p>
    <div class="hero-features">
        <div class="hero-feature">
            <span class="hero-feature-icon">📸</span>
            <div>40+ Camera Angles</div>
        </div>
        <div class="hero-feature">
            <span class="hero-feature-icon">🎨</span>
            <div>Custom Selection</div>
        </div>
        <div class="hero-feature">
            <span class="hero-feature-icon">📝</span>
            <div>Script Doctor</div>
        </div>
        <div class="hero-feature">
            <span class="hero-feature-icon">🎬</span>
            <div>Video Prompts</div>
        </div>
        <div class="hero-feature">
            <span class="hero-feature-icon">🚀</span>
            <div>Viral Manager</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- TABS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📸 Multi-Angle Generator",
    "📝 Script Doctor",
    "🎬 Video Generator",
    "🖼️ Image Prompts",
    "🚀 Viral Manager"
])

# === TAB 1: MULTI-ANGLE GENERATOR ===
with tab1:
    st.markdown("### 📸 Custom Camera Angle Prompt Generator")
    
    if is_demo:
        st.info("🎮 **Demo Mode** - Multi-angle prompt generation requires a real API key. Please login to use this feature.")
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #e0e7ff 0%, #dbeafe 100%); padding: 1.5rem; border-radius: 16px; margin-bottom: 2rem;'>
        <h3 style='color: #4338ca; margin-bottom: 0.5rem;'>💡 How It Works</h3>
        <p style='color: #4338ca; margin: 0;'>
            1. Upload your image<br>
            2. Select the camera angles you want (multiple selection supported)<br>
            3. Choose your visual style<br>
            4. Get professional video prompts for only your selected angles!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main layout
    col_left, col_right = st.columns([1, 1], gap="large")
    
    with col_left:
        st.markdown("#### 📤 Upload Image")
        
        uploaded_image = st.file_uploader(
            "Choose an image",
            type=["jpg", "jpeg", "png", "webp"],
            help="Upload any image to generate video prompts from selected camera angles",
            key="multi_angle_upload"
        )
        
        if uploaded_image:
            st.image(uploaded_image, use_container_width=True, caption="Original Image")
        
        st.markdown("---")
        st.markdown("#### 🎨 Select Visual Style")
        
        selected_style = st.selectbox(
            "Choose visual style for prompts",
            [
                "Photorealistic/Cinematic",
                "Digital Art/Illustration", 
                "Oil Painting/Artistic",
                "Watercolor/Soft",
                "Anime/Manga Style",
                "3D Render/CGI",
                "Pencil Sketch/Drawing",
                "Cyberpunk/Futuristic",
                "Fantasy Art/Mystical",
                "Retro/Vintage Film",
                "Documentary/Raw",
                "Music Video/Dynamic",
                "Film Noir/Black & White",
                "Neon/Vibrant Colors",
                "Pastel/Soft Colors"
            ],
            key="multi_angle_style"
        )
    
    with col_right:
        st.markdown("#### 🎯 Select Camera Angles (Multiple Selection)")
        
        st.info("💡 Select one or more angles. Only selected angles will generate prompts!")
        
        # Create tabs for angle categories
        angle_tabs = st.tabs(list(CAMERA_ANGLES.keys()))
        
        all_selected_angles = []
        
        for tab, (category, angles) in zip(angle_tabs, CAMERA_ANGLES.items()):
            with tab:
                st.markdown(f"**{category}** ({len(angles)} options)")
                
                # Create checkboxes for each angle in this category
                for angle_name, angle_desc in angles:
                    col_check, col_info = st.columns([3, 1])
                    with col_check:
                        is_selected = st.checkbox(
                            angle_name,
                            key=f"angle_{angle_name}",
                            help=angle_desc
                        )
                        if is_selected:
                            all_selected_angles.append(angle_name)
                    with col_info:
                        with st.expander("ℹ️"):
                            st.caption(angle_desc)
        
        st.markdown("---")
        
        # Show selected angles count
        if all_selected_angles:
            st.success(f"✅ **{len(all_selected_angles)} angles selected**")
            
            with st.expander("📋 View Selected Angles", expanded=False):
                for idx, angle in enumerate(all_selected_angles, 1):
                    st.write(f"{idx}. {angle}")
        else:
            st.warning("⚠️ Please select at least one camera angle")
        
        # Generate button
        generate_btn = st.button(
            f"🎬 Generate Prompts for {len(all_selected_angles)} Selected Angle{'s' if len(all_selected_angles) != 1 else ''}",
            type="primary",
            use_container_width=True,
            disabled=is_demo or not uploaded_image or len(all_selected_angles) == 0,
            key="gen_prompts_btn"
        )
        
        if generate_btn and uploaded_image and all_selected_angles:
            with st.spinner(f"🎨 Generating {len(all_selected_angles)} camera angle prompts... This will take about {len(all_selected_angles) * 2} seconds..."):
                generated_prompts, error = generate_selected_angle_prompts(
                    uploaded_image,
                    model,
                    all_selected_angles,
                    selected_style
                )
                
                if generated_prompts:
                    st.success(f"✅ Generated {len(generated_prompts)} camera angle prompts!")
                    
                    st.markdown("---")
                    st.markdown("### 🎬 Generated Video Prompts:")
                    
                    # Compile all prompts
                    all_prompts_text = f"""MULTI-ANGLE VIDEO PROMPTS
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Style: {selected_style}
Total Angles: {len(generated_prompts)}

{'='*80}

"""
                    
                    # Display each prompt
                    for idx, prompt_data in enumerate(generated_prompts):
                        with st.expander(f"🎬 {prompt_data['angle']} - Prompt #{idx+1}", expanded=(idx==0)):
                            st.markdown(f"**Camera Angle:** {prompt_data['angle']}")
                            st.markdown(f"**Visual Style:** {selected_style}")
                            st.markdown("---")
                            st.markdown("**Video Prompt:**")
                            st.code(prompt_data['prompt'], language="text")
                            
                            # Individual download
                            st.download_button(
                                f"📥 Download {prompt_data['angle']} Prompt",
                                data=prompt_data['prompt'],
                                file_name=f"{prompt_data['angle'].replace(' ', '_')}_prompt_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                                mime="text/plain",
                                use_container_width=True,
                                key=f"dl_prompt_{idx}"
                            )
                        
                        # Add to combined text
                        all_prompts_text += f"""{prompt_data['angle']}
{'-'*80}
{prompt_data['prompt']}

{'='*80}

"""
                    
                    # Bulk download
                    st.markdown("---")
                    col_dl1, col_dl2 = st.columns(2)
                    with col_dl1:
                        st.download_button(
                            f"📦 Download ALL {len(generated_prompts)} Prompts (Combined)",
                            data=all_prompts_text,
                            file_name=f"all_{len(generated_prompts)}_angle_prompts_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                            mime="text/plain",
                            use_container_width=True,
                            type="primary",
                            key="dl_all_prompts"
                        )
                    with col_dl2:
                        # JSON format download
                        json_data = json.dumps({
                            'metadata': {
                                'generated': datetime.now().strftime('%Y-%m-%d %H:%M'),
                                'style': selected_style,
                                'total_angles': len(generated_prompts)
                            },
                            'prompts': generated_prompts
                        }, indent=2)
                        
                        st.download_button(
                            "📋 Download as JSON",
                            data=json_data,
                            file_name=f"prompts_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                            mime="application/json",
                            use_container_width=True,
                            key="dl_json"
                        )
                    
                    st.success("💡 Copy these prompts to Runway ML, Pika Labs, or your preferred AI video tool!")
                    
                else:
                    st.error(f"❌ {error}")

# === TAB 2: SCRIPT DOCTOR ===
with tab2:
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("### 📥 Input Script")
        raw_script = st.text_area(
            "Enter your content",
            height=300,
            placeholder="Paste your script, ideas, or bullet points here...",
            key="script_input"
        )
        
        col_a, col_b = st.columns(2)
        with col_a:
            mode = st.selectbox(
                "Style",
                ["🎯 Viral Hook", "💼 Professional", "😂 Funny", "🎓 Educational", 
                 "💰 Sales", "🌏 Malayalam → English", "✨ Creative"]
            )
        
        with col_b:
            length = st.selectbox(
                "Length",
                ["Keep Original", "Make Shorter", "Make Longer", "Expand Dramatically"]
            )
        
        enhance_btn = st.button("✨ Enhance Script", type="primary", use_container_width=True, key="enhance")
    
    with col2:
        st.markdown("### ✨ Enhanced Result")
        
        if enhance_btn:
            if raw_script.strip():
                with st.spinner("🤖 Enhancing your script..."):
                    prompt = f"""Rewrite this script professionally:

Style: {mode}
Length: {length}
Input: {raw_script}

Requirements:
- Maintain core message
- Apply {mode} style
- {length}
- Professional quality
- Clear and engaging

Output enhanced script only."""
                    
                    result = safe_generate(prompt, model)
                    
                    if result and "Error" not in result:
                        st.success("✅ Script enhanced!")
                        st.text_area("Enhanced Script", value=result, height=300, key="enhanced_output")
                        
                        col_m1, col_m2 = st.columns(2)
                        with col_m1:
                            st.metric("Original Words", len(raw_script.split()))
                        with col_m2:
                            st.metric("Enhanced Words", len(result.split()))
                        
                        st.download_button(
                            "📥 Download",
                            data=result,
                            file_name=f"enhanced_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                            use_container_width=True
                        )
                    else:
                        st.error(result)
            else:
                st.warning("⚠️ Please enter content first")

# === TAB 3: VIDEO GENERATOR ===
with tab3:
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("### 👤 Character Setup")
        
        uploaded_file = st.file_uploader(
            "Upload character image",
            type=["jpg", "jpeg", "png", "webp"],
            key="char_upload"
        )
        
        if uploaded_file:
            col_img, col_btn = st.columns([2, 1])
            with col_img:
                st.image(uploaded_file, use_container_width=True)
            with col_btn:
                if st.button("🔍 Analyze", use_container_width=True):
                    with st.spinner("Analyzing..."):
                        analysis = analyze_image(uploaded_file, model)
                        if "Error" not in analysis:
                            st.session_state.img_description = analysis
                            st.success("✅ Done!")
                        else:
                            st.error(analysis)
        
        img_desc = st.text_area(
            "Character description",
            value=st.session_state.img_description,
            height=150,
            placeholder="Describe the character appearance...",
            key="char_desc"
        )
        
        visual_style = st.selectbox(
            "Visual Style",
            ["🎯 Strict Realism", "🎬 Cinematic Movie", "🎪 Disney/Pixar 3D", 
             "🌃 Cyberpunk/Neon", "📼 Vintage Film", "🎨 Oil Painting"]
        )
        
        script = st.text_area(
            "Video Script",
            height=150,
            placeholder="Enter dialogue...",
            key="video_script"
        )
        
        max_words = st.slider("Words per clip", 8, 25, 15)
        
        if script:
            clips_preview = split_dialogue(script, max_words)
            st.info(f"📊 Will create {len(clips_preview)} clips")
        
        gen_btn = st.button("🚀 Generate Prompts", type="primary", use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Generated Prompts")
        
        if gen_btn:
            if img_desc.strip() and script.strip():
                clips = split_dialogue(script, max_words)
                
                progress = st.progress(0)
                st.success(f"✅ Generating {len(clips)} prompts...")
                
                for i, clip in enumerate(clips):
                    progress.progress((i + 1) / len(clips))
                    
                    style_name = visual_style.split(" ", 1)[1] if " " in visual_style else visual_style
                    
                    prompt_text = f"""Create professional video prompt for AI tools.

CLIP #{i+1}
CHARACTER: {img_desc}
DIALOGUE: "{clip}"
STYLE: {style_name}

Include:
- Character description
- Dialogue delivery
- Facial expressions
- Camera work
- Lighting
- Style elements

Production-ready format."""
                    
                    result = safe_generate(prompt_text, model)
                    
                    with st.expander(f"🎬 Clip {i+1}", expanded=(i==0)):
                        if "Error" not in result:
                            st.code(result, language="text")
                            st.download_button(
                                "💾 Download",
                                data=result,
                                file_name=f"clip_{i+1}.txt",
                                key=f"dl_{i}"
                            )
                        else:
                            st.warning(result)
                    
                    if i < len(clips) - 1:
                        time.sleep(1)
                
                st.success("✅ All prompts generated!")
            else:
                st.error("⚠️ Please provide character description and script")

# === TAB 4: IMAGE PROMPTS ===
with tab4:
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("### 💭 Your Vision")
        
        idea = st.text_area(
            "Describe your image",
            height=250,
            placeholder="Example: A futuristic city at sunset...",
            key="image_idea"
        )
        
        col_ar, col_det = st.columns(2)
        with col_ar:
            aspect = st.selectbox(
                "Aspect Ratio",
                ["1:1 Square", "16:9 Landscape", "9:16 Portrait", "4:3 Classic"]
            )
        
        with col_det:
            detail = st.selectbox(
                "Detail Level",
                ["High Detail", "Medium Detail", "Simple/Minimalist"]
            )
        
        img_style = st.selectbox(
            "Art Style (56+ Options)",
            [
                "Photorealistic", "Digital Art", "Oil Painting", "Watercolor",
                "Anime/Manga", "3D Render", "Pencil Sketch", "Charcoal Drawing",
                "Ink Drawing", "Pastel Art", "Acrylic Painting", "Abstract Art",
                "Pop Art", "Comic Book", "Cartoon", "Pixel Art",
                "Low Poly", "Voxel Art", "Cyberpunk", "Steampunk",
                "Fantasy Art", "Sci-Fi", "Horror", "Gothic",
                "Art Nouveau", "Art Deco", "Minimalist", "Impressionist",
                "Expressionist", "Surrealism", "Cubism", "Pointillism",
                "Graffiti", "Street Art", "Vintage Photo", "Retro 80s",
                "Film Noir", "Baroque", "Renaissance", "Medieval",
                "Egyptian", "Japanese Ukiyo-e", "Chinese Ink", "Stained Glass",
                "Mosaic", "Paper Cut", "Origami", "Clay Animation",
                "Stop Motion", "Glitch Art", "Vaporwave", "Synthwave",
                "Neon Art", "Holographic", "Psychedelic", "Geometric", "Isometric"
            ],
            key="img_style_select"
        )

        
        create_btn = st.button("✨ Create Prompt", type="primary", use_container_width=True)
    
    with col2:
        st.markdown("### 🎨 Generated Prompt")
        
        if create_btn:
            if idea.strip():
                with st.spinner("🤖 Creating prompt..."):
                    prompt = f"""Create professional image generation prompt:

Vision: {idea}
Style: {img_style}
Aspect: {aspect}
Detail: {detail}

Include:
- Main subject
- Composition
- Lighting
- Color palette
- Technical specs
- Style keywords

Format for Midjourney/DALL-E/Stable Diffusion"""
                    
                    result = safe_generate(prompt, model)
                    
                    if result and "Error" not in result:
                        st.success("✅ Prompt created!")
                        st.code(result, language="text")
                        
                        st.download_button(
                            "📥 Download Prompt",
                            data=result,
                            file_name=f"image_prompt_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                            use_container_width=True
                        )
                    else:
                        st.error(result)
            else:
                st.warning("⚠️ Please describe your image idea")

# === TAB 5: VIRAL MANAGER ===
with tab5:
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("### 📋 Content Details")
        
        topic = st.text_input(
            "Topic",
            placeholder="Example: How to make perfect coffee",
            key="viral_topic"
        )
        
        platform = st.multiselect(
            "Platforms",
            ["YouTube", "Instagram", "TikTok", "Twitter/X", "LinkedIn"],
            default=["YouTube"]
        )
        
        audience = st.selectbox(
            "Target Audience",
            ["General Public", "Young Adults (18-25)", "Professionals", 
             "Tech Enthusiasts", "Entrepreneurs"]
        )
        
        tone = st.selectbox(
            "Content Tone",
            ["Exciting/Energetic", "Educational", "Funny", "Inspirational", "Professional"]
        )
        
        viral_btn = st.button("🚀 Generate Strategy", type="primary", use_container_width=True)
    
    with col2:
        st.markdown("### 💎 Viral Package")
        
        if viral_btn:
            if topic.strip():
                with st.spinner("🤖 Creating strategy..."):
                    prompt = f"""Create viral content strategy:

Topic: {topic}
Platforms: {', '.join(platform)}
Audience: {audience}
Tone: {tone}

Generate:
1. 5 Viral Titles
2. SEO Description
3. 30 Hashtags
4. Call-to-Action options
5. Hook Ideas
6. Platform tips

Professional format."""
                    
                    result = safe_generate(prompt, model)
                    
                    if result and "Error" not in result:
                        st.success("✅ Strategy generated!")
                        st.markdown(result)
                        
                        st.download_button(
                            "📥 Download Strategy",
                            data=result,
                            file_name=f"viral_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                            use_container_width=True
                        )
                    else:
                        st.error(result)
            else:
                st.warning("⚠️ Please enter a topic")

# --- FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; padding: 2rem; background: white; border-radius: 20px; 
            margin: 0 3rem; box-shadow: 0 4px 20px rgba(0,0,0,0.08);'>
    <h3 style='color: #667eea; margin-bottom: 0.5rem; font-family: "Manrope", sans-serif;'>
        Ultra Studio V13 Pro
    </h3>
    <p style='color: #64748b; margin: 0;'>
        40+ Camera Angles • Custom Selection • Professional Content Creation
    </p>
    <p style='color: #94a3b8; font-size: 0.9em; margin-top: 0.5rem;'>
        Powered by Google Gemini 3 Flash Preview ✨
    </p>
</div>
""", unsafe_allow_html=True)