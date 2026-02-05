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

# --- Simplified CSS (Cloud Compatible) ---
st.markdown("""
    <style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Ensure text is visible - Changed from black to dark blue */
    body, .stApp, div, p, span, h1, h2, h3, h4, h5, h6, label, input, textarea, select, option {
        color: #1e40af !important;
    }
    
    /* Main background */
    .stApp {
        background: #f7fafc;
    }
    
    /* Remove sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {
        visibility: hidden;
    }
    
    /* Improve button visibility */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
    }
    
    /* Input fields - Changed from black to dark blue */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stSelectbox > div > div {
        background: white !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        color: #1e40af !important;
        padding: 0.75rem !important;
    }
    
    /* Selectbox options */
    .stSelectbox option {
        background: white !important;
        color: #1e40af !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: #f1f5f9;
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #64748b !important;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        border: 2px dashed #cbd5e1;
        border-radius: 16px;
        padding: 2rem;
        background: white;
    }
    
    [data-testid="stFileUploader"] label,
    [data-testid="stFileUploader"] p,
    [data-testid="stFileUploader"] span {
        color: #1e40af !important;
    }
    
    /* Expander - Changed from black to dark blue */
    .streamlit-expanderHeader {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem;
        color: #1e40af !important;
        font-weight: 600;
    }
    
    .streamlit-expanderHeader p,
    .streamlit-expanderHeader span {
        color: #1e40af !important;
    }
    
    /* Success/Error/Warning/Info boxes */
    .stSuccess, .stError, .stWarning, .stInfo {
        padding: 1rem;
        border-radius: 12px;
        border-left: 4px solid;
    }
    
    /* Checkbox labels - Changed from black to dark blue */
    .stCheckbox > label,
    .stCheckbox > label > div,
    .stCheckbox > label > div > p,
    .stCheckbox span {
        color: #1e40af !important;
        font-weight: 500;
    }
    
    /* Radio button labels */
    .stRadio > label,
    .stRadio > label > div > p {
        color: #1e40af !important;
    }
    
    /* Slider labels */
    .stSlider > label,
    .stSlider > label > div > p {
        color: #1e40af !important;
    }
    
    /* Multiselect */
    .stMultiSelect > label,
    .stMultiSelect > label > div > p,
    .stMultiSelect span {
        color: #1e40af !important;
    }
    
    /* Make sure all text is visible - Changed from black to dark blue */
    * {
        color: #1e40af !important;
    }
    
    /* Markdown text - Changed from black to dark blue */
    .markdown-text-container,
    .markdown-text-container * {
        color: #1e40af !important;
    }
    
    /* Code blocks - keep them distinct */
    code, pre {
        color: #059669 !important;
        background: #f0fdf4 !important;
    }
    
    /* Links */
    a {
        color: #667eea !important;
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
if 'last_analyzed_image' not in st.session_state:
    st.session_state.last_analyzed_image = None

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
        return "🎮 **Demo Mode Active**\n\nTo use real AI features:\n1. Logout\n2. Get free API key from ai.google.dev\n3. Login with your API key"
    
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
        return "🎮 Demo Mode - Image analysis requires API key"
    
    try:
        img = Image.open(image_file)
        if max(img.size) > 1024:
            img.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
        
        prompt = """Analyze this image for AI video generation. Describe:
        1. Physical appearance
        2. Hair style, color, length
        3. Clothing and accessories
        4. Age range and gender
        5. Overall style and vibe
        
        Be specific for AI prompts."""
        
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
    """Generate video prompts for selected camera angles"""
    try:
        if model is None:
            return None, "🎮 Demo Mode - Requires real API key"
        
        # Load and analyze image
        img = Image.open(image_file)
        if max(img.size) > 1024:
            img.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
        
        st.info("📝 Analyzing image...")
        
        analysis_prompt = """Analyze this image for AI video prompts. Include:
        - Subject/character details
        - Setting and environment
        - Mood and atmosphere
        - Colors and lighting
        - Notable features
        
        Be specific and detailed."""
        
        try:
            analysis_response = model.generate_content([analysis_prompt, img])
            base_description = analysis_response.text.strip()
            st.session_state.api_calls_count += 1
            st.success("✅ Image analyzed!")
        except Exception as ve:
            return None, f"⚠️ Analysis failed: {str(ve)}"
        
        generated_prompts = []
        
        for idx, angle_name in enumerate(selected_angles):
            angle_description = ""
            for category, angles in CAMERA_ANGLES.items():
                for name, desc in angles:
                    if name == angle_name:
                        angle_description = desc
                        break
                if angle_description:
                    break
            
            st.info(f"🎬 Generating {angle_name} prompt ({idx+1}/{len(selected_angles)})...")
            
            prompt_template = f"""Create professional AI video prompt:

IMAGE ANALYSIS:
{base_description}

CAMERA ANGLE: {angle_name}
ANGLE DESCRIPTION: {angle_description}
VISUAL STYLE: {selected_style}

Generate detailed video prompt with:
1. Character/subject description
2. Camera angle and movement
3. Composition and framing
4. Lighting setup and mood
5. Visual style and atmosphere
6. Technical specifications
7. Motion/animation details
8. Color grading notes

Format for Runway ML, Pika Labs, etc.
Make it production-ready and cinematic."""
            
            try:
                response = model.generate_content(prompt_template)
                prompt_text = response.text.strip()
                st.session_state.api_calls_count += 1
                
                generated_prompts.append({
                    'angle': angle_name,
                    'prompt': prompt_text
                })
                st.success(f"✅ {angle_name} done!")
                
            except Exception as e:
                st.warning(f"⚠️ {angle_name} failed: {str(e)}")
            
            if idx < len(selected_angles) - 1:
                time.sleep(1)
        
        if generated_prompts:
            return generated_prompts, None
        else:
            return None, "No prompts generated"
        
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            return None, "⏳ Rate limit reached. Wait 60 seconds."
        elif "quota" in error_msg.lower():
            return None, "💳 API quota exceeded"
        else:
            return None, f"⚠️ Error: {error_msg}"


# --- LOGIN PAGE ---
if not st.session_state.logged_in:
    st.markdown("## ✨ Ultra Studio V13 Pro")
    st.markdown("### Multi-Angle AI Generator")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            api_key_input = st.text_input(
                "Gemini API Key",
                type="password",
                placeholder="Enter your API key...",
                help="Get free API key from ai.google.dev"
            )
            
            login_button = st.form_submit_button("🚀 Login", use_container_width=True)
            
            if login_button:
                if api_key_input.strip():
                    with st.spinner("🔍 Validating..."):
                        try:
                            genai.configure(api_key=api_key_input)
                            test_model = genai.GenerativeModel('gemini-3-flash-preview')
                            response = test_model.generate_content("Hi")
                            
                            st.session_state.logged_in = True
                            st.session_state.api_key = api_key_input
                            st.success("✅ Login successful!")
                            time.sleep(1)
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"❌ Login failed: {str(e)}")
                            st.info("💡 Get API key from https://ai.google.dev")
                else:
                    st.warning("⚠️ Please enter API key")
        
        st.markdown("---")
        
        if st.button("🎮 Try Demo Mode", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.api_key = "DEMO_MODE"
            st.rerun()
        
        with st.expander("📖 How to get API key"):
            st.markdown("""
            1. Visit [ai.google.dev](https://ai.google.dev)
            2. Sign in with Google
            3. Click "Get API Key"
            4. Create API Key
            5. Copy and paste above
            
            **Free to use!** 🎉
            """)
    
    st.stop()

# --- MAIN APP ---
is_demo = (st.session_state.api_key == "DEMO_MODE")

if not is_demo:
    genai.configure(api_key=st.session_state.api_key)
    model = genai.GenerativeModel('gemini-3-flash-preview')
else:
    model = None
    st.warning("🎮 Demo Mode - Login with API key for full features")

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("✨ Ultra Studio V13 Pro")
    st.caption(f"API Calls: {st.session_state.api_calls_count} | Prompts: {len(st.session_state.generated_prompts)}")
with col2:
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.api_key = ""
        st.rerun()

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📸 Multi-Angle",
    "📝 Script Doctor",
    "🎬 Video Generator",
    "🖼️ Image Prompts",
    "🚀 Viral Manager"
])

# TAB 1: Multi-Angle Generator
with tab1:
    st.header("📸 Custom Camera Angle Generator")
    
    if is_demo:
        st.info("🎮 Demo Mode - Login for full features")
    
    st.info("💡 Upload image → Select angles → Get professional prompts!")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("📤 Upload Image")
        
        uploaded_image = st.file_uploader(
            "Choose image",
            type=["jpg", "jpeg", "png", "webp"],
            key="multi_angle_upload"
        )
        
        if uploaded_image:
            st.image(uploaded_image, use_container_width=True)
            
            # Auto-analyze on upload
            if 'last_analyzed_image' not in st.session_state or st.session_state.last_analyzed_image != uploaded_image.name:
                with st.spinner("🔍 Auto-analyzing image..."):
                    analysis = analyze_image(uploaded_image, model)
                    if "Error" not in analysis and "Demo Mode" not in analysis:
                        st.session_state.img_description = analysis
                        st.session_state.last_analyzed_image = uploaded_image.name
                        st.success("✅ Image analyzed automatically!")
                        with st.expander("📋 View Analysis", expanded=True):
                            st.write(analysis)
            
            # Manual re-analyze option
            if st.button("🔄 Re-analyze Image", key="reanalyze_multi"):
                with st.spinner("🔍 Analyzing..."):
                    analysis = analyze_image(uploaded_image, model)
                    if "Error" not in analysis and "Demo Mode" not in analysis:
                        st.session_state.img_description = analysis
                        st.success("✅ Analysis updated!")
                        with st.expander("📋 View Analysis", expanded=True):
                            st.write(analysis)
        
        st.markdown("---")
        st.subheader("🎨 Visual Style")
        
        selected_style = st.selectbox(
            "Choose style",
            [
                "Photorealistic/Cinematic",
                "Digital Art", 
                "Oil Painting",
                "Anime/Manga",
                "3D Render/CGI",
                "Cyberpunk",
                "Fantasy Art",
                "Retro/Vintage",
                "Documentary",
                "Music Video"
            ]
        )
    
    with col_right:
        st.subheader("🎯 Select Camera Angles")
        st.info("💡 Select one or more angles")
        
        angle_tabs = st.tabs(list(CAMERA_ANGLES.keys()))
        
        all_selected_angles = []
        
        for tab, (category, angles) in zip(angle_tabs, CAMERA_ANGLES.items()):
            with tab:
                st.markdown(f"**{category}**")
                
                for angle_name, angle_desc in angles:
                    is_selected = st.checkbox(
                        angle_name,
                        key=f"angle_{angle_name}",
                        help=angle_desc
                    )
                    if is_selected:
                        all_selected_angles.append(angle_name)
        
        st.markdown("---")
        
        if all_selected_angles:
            st.success(f"✅ {len(all_selected_angles)} angles selected")
            with st.expander("View Selected"):
                for idx, angle in enumerate(all_selected_angles, 1):
                    st.write(f"{idx}. {angle}")
        else:
            st.warning("⚠️ Select at least one angle")
        
        generate_btn = st.button(
            f"🎬 Generate {len(all_selected_angles)} Prompts",
            type="primary",
            disabled=is_demo or not uploaded_image or not all_selected_angles
        )
        
        if generate_btn and uploaded_image and all_selected_angles:
            with st.spinner(f"🎨 Generating {len(all_selected_angles)} prompts..."):
                prompts, error = generate_selected_angle_prompts(
                    uploaded_image,
                    model,
                    all_selected_angles,
                    selected_style
                )
                
                if prompts:
                    st.success(f"✅ Generated {len(prompts)} prompts!")
                    
                    st.markdown("---")
                    st.subheader("🎬 Generated Prompts")
                    
                    all_text = f"""MULTI-ANGLE VIDEO PROMPTS
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Style: {selected_style}
Total: {len(prompts)}

{'='*80}

"""
                    
                    for idx, p in enumerate(prompts):
                        with st.expander(f"🎬 {p['angle']} - #{idx+1}", expanded=(idx==0)):
                            st.markdown(f"**Angle:** {p['angle']}")
                            st.markdown(f"**Style:** {selected_style}")
                            st.code(p['prompt'])
                            
                            st.download_button(
                                f"📥 Download",
                                data=p['prompt'],
                                file_name=f"{p['angle'].replace(' ', '_')}.txt",
                                key=f"dl_{idx}"
                            )
                        
                        all_text += f"{p['angle']}\n{'-'*80}\n{p['prompt']}\n\n{'='*80}\n\n"
                    
                    st.markdown("---")
                    st.download_button(
                        f"📦 Download All {len(prompts)} Prompts",
                        data=all_text,
                        file_name=f"all_prompts_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        type="primary"
                    )
                else:
                    st.error(f"❌ {error}")

# TAB 2: Script Doctor
with tab2:
    st.header("📝 Script Doctor")
    
    col1, col2 = st.columns(2)
    
    with col1:
        raw_script = st.text_area(
            "Input Script",
            height=300,
            placeholder="Paste your script here..."
        )
        
        col_a, col_b = st.columns(2)
        with col_a:
            mode = st.selectbox("Style", [
                "🎯 Viral Hook",
                "💼 Professional",
                "😂 Funny",
                "🎓 Educational",
                "💰 Sales"
            ])
        with col_b:
            length = st.selectbox("Length", [
                "Keep Original",
                "Make Shorter",
                "Make Longer"
            ])
        
        enhance_btn = st.button("✨ Enhance", type="primary", use_container_width=True)
    
    with col2:
        st.subheader("Enhanced Result")
        
        if enhance_btn and raw_script:
            with st.spinner("Enhancing..."):
                prompt = f"""Rewrite professionally:
Style: {mode}
Length: {length}
Input: {raw_script}"""
                
                result = safe_generate(prompt, model)
                
                if "Error" not in result:
                    st.success("✅ Done!")
                    st.text_area("Output", result, height=300)
                    
                    col_m1, col_m2 = st.columns(2)
                    with col_m1:
                        st.metric("Original", len(raw_script.split()))
                    with col_m2:
                        st.metric("Enhanced", len(result.split()))
                    
                    st.download_button(
                        "📥 Download",
                        data=result,
                        file_name=f"enhanced_{datetime.now().strftime('%H%M')}.txt"
                    )
                else:
                    st.error(result)

# TAB 3: Video Generator
with tab3:
    st.header("🎬 Video Prompt Generator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_char = st.file_uploader(
            "Upload Character Image",
            type=["jpg", "jpeg", "png", "webp"],
            key="char_img"
        )
        
        if uploaded_char:
            st.image(uploaded_char, use_container_width=True)
            
            if st.button("🔍 Analyze Image"):
                with st.spinner("Analyzing..."):
                    analysis = analyze_image(uploaded_char, model)
                    if "Error" not in analysis:
                        st.session_state.img_description = analysis
                        st.success("✅ Done!")
        
        char_desc = st.text_area(
            "Character Description",
            value=st.session_state.img_description,
            height=150,
            placeholder="Describe character..."
        )
        
        visual_style = st.selectbox("Style", [
            "🎯 Photorealistic",
            "🎬 Cinematic",
            "🎪 Disney/Pixar 3D",
            "🌃 Cyberpunk"
        ])
        
        script = st.text_area(
            "Video Script",
            height=150,
            placeholder="Enter dialogue..."
        )
        
        max_words = st.slider("Words per clip", 8, 25, 15)
        
        if script:
            clips = split_dialogue(script, max_words)
            st.info(f"📊 Will create {len(clips)} clips")
        
        gen_btn = st.button("🚀 Generate", type="primary")
    
    with col2:
        st.subheader("Generated Prompts")
        
        if gen_btn and char_desc and script:
            clips = split_dialogue(script, max_words)
            progress = st.progress(0)
            
            for i, clip in enumerate(clips):
                progress.progress((i + 1) / len(clips))
                
                style = visual_style.split(" ", 1)[1] if " " in visual_style else visual_style
                
                prompt_txt = f"""Create video prompt:
CHARACTER: {char_desc}
DIALOGUE: "{clip}"
STYLE: {style}

Include camera, lighting, expressions."""
                
                result = safe_generate(prompt_txt, model)
                
                with st.expander(f"🎬 Clip {i+1}", expanded=(i==0)):
                    if "Error" not in result:
                        st.code(result)
                        st.download_button(
                            "💾 Download",
                            data=result,
                            file_name=f"clip_{i+1}.txt",
                            key=f"dlc_{i}"
                        )
                    else:
                        st.warning(result)
                
                time.sleep(1)
            
            st.success("✅ All prompts generated!")

# TAB 4: Image Prompts
with tab4:
    st.header("🖼️ Image Prompt Generator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        idea = st.text_area(
            "Describe Image",
            height=250,
            placeholder="A futuristic city at sunset..."
        )
        
        col_a, col_b = st.columns(2)
        with col_a:
            aspect = st.selectbox("Aspect", [
                "1:1 Square",
                "16:9 Landscape",
                "9:16 Portrait"
            ])
        with col_b:
            detail = st.selectbox("Detail", [
                "High Detail",
                "Medium Detail",
                "Simple"
            ])
        
        art_style = st.selectbox("Art Style", [
            "Photorealistic",
            "Digital Art",
            "Oil Painting",
            "Anime",
            "3D Render",
            "Cyberpunk",
            "Fantasy"
        ])
        
        create_btn = st.button("✨ Create Prompt", type="primary")
    
    with col2:
        st.subheader("Generated Prompt")
        
        if create_btn and idea:
            with st.spinner("Creating..."):
                prompt = f"""Create image prompt:
Vision: {idea}
Style: {art_style}
Aspect: {aspect}
Detail: {detail}

Include composition, lighting, colors."""
                
                result = safe_generate(prompt, model)
                
                if "Error" not in result:
                    st.success("✅ Done!")
                    st.code(result)
                    st.download_button(
                        "📥 Download",
                        data=result,
                        file_name=f"image_prompt_{datetime.now().strftime('%H%M')}.txt"
                    )
                else:
                    st.error(result)

# TAB 5: Viral Manager
with tab5:
    st.header("🚀 Viral Content Manager")
    
    col1, col2 = st.columns(2)
    
    with col1:
        topic = st.text_input(
            "Topic",
            placeholder="How to make perfect coffee"
        )
        
        platforms = st.multiselect(
            "Platforms",
            ["YouTube", "Instagram", "TikTok", "Twitter", "LinkedIn"],
            default=["YouTube"]
        )
        
        audience = st.selectbox("Audience", [
            "General Public",
            "Young Adults",
            "Professionals",
            "Tech Enthusiasts"
        ])
        
        tone = st.selectbox("Tone", [
            "Exciting",
            "Educational",
            "Funny",
            "Professional"
        ])
        
        viral_btn = st.button("🚀 Generate Strategy", type="primary")
    
    with col2:
        st.subheader("Viral Package")
        
        if viral_btn and topic:
            with st.spinner("Creating strategy..."):
                prompt = f"""Create viral strategy:
Topic: {topic}
Platforms: {', '.join(platforms)}
Audience: {audience}
Tone: {tone}

Generate:
1. 5 Viral Titles
2. SEO Description
3. 30 Hashtags
4. Call-to-Actions
5. Hooks"""
                
                result = safe_generate(prompt, model)
                
                if "Error" not in result:
                    st.success("✅ Done!")
                    st.markdown(result)
                    st.download_button(
                        "📥 Download",
                        data=result,
                        file_name=f"viral_{datetime.now().strftime('%H%M')}.txt"
                    )
                else:
                    st.error(result)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; background: white; border-radius: 16px;'>
    <h3 style='color: #667eea;'>Ultra Studio V13 Pro</h3>
    <p style='color: #64748b;'>40+ Camera Angles • Custom Selection • Professional Prompts</p>
    <p style='color: #94a3b8; font-size: 0.9em;'>Powered by gemini-3-flash-preview ✨</p>
</div>
""", unsafe_allow_html=True)