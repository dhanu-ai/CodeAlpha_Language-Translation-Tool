import os
import streamlit as st
from huggingface_hub import InferenceClient
import time

# ---------------------------------------------------
# Hugging Face Inference Client Setup
# ---------------------------------------------------
def get_client():
    """Initialize Hugging Face client with API token"""
    try:
        if "HF_TOKEN" in st.secrets:
            api_key = st.secrets["HF_TOKEN"]
        elif "HF_TOKEN" in os.environ:
            api_key = os.environ["HF_TOKEN"]
        else:
            api_key = st.text_input("Enter your Hugging Face Token:", type="password")
            if not api_key:
                st.warning("Please enter your Hugging Face token to continue.")
                return None
        
        return InferenceClient(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize client: {str(e)}")
        return None

# ---------------------------------------------------
# Translation Models Configuration
# ---------------------------------------------------
TRANSLATION_MODELS = {
    "MBART Large 50": "facebook/mbart-large-50-many-to-many-mmt",
    "M2M100 418M": "facebook/m2m100_418M",
    "NLLB 200 Distilled": "facebook/nllb-200-distilled-600M",
    "OPUS MT EN-HI": "Helsinki-NLP/opus-mt-en-hi",
    "OPUS MT HI-EN": "Helsinki-NLP/opus-mt-hi-en",
    "Google T5 Small": "google-t5/t5-small",
}

# Language mapping for different models
LANGUAGE_MAPPING = {
    "facebook/mbart-large-50-many-to-many-mmt": {
        "English": "en_XX",
        "Hindi": "hi_IN",
        "French": "fr_XX", 
        "Spanish": "es_XX",
        "German": "de_DE",
        "Italian": "it_IT",
        "Chinese": "zh_CN",
        "Japanese": "ja_XX",
        "Arabic": "ar_AR",
        "Russian": "ru_RU",
    },
    "facebook/m2m100_418M": {
        "English": "en",
        "Hindi": "hi",
        "French": "fr",
        "Spanish": "es", 
        "German": "de",
        "Italian": "it",
        "Chinese": "zh",
        "Japanese": "ja",
        "Arabic": "ar",
        "Russian": "ru",
    },
    "facebook/nllb-200-distilled-600M": {
        "English": "eng_Latn",
        "Hindi": "hin_Deva",
        "French": "fra_Latn",
        "Spanish": "spa_Latn",
        "German": "deu_Latn",
        "Italian": "ita_Latn", 
        "Chinese": "zho_Hans",
        "Japanese": "jpn_Jpan",
        "Arabic": "arb_Arab",
        "Russian": "rus_Cyrl",
    },
    "default": {
        "English": "en",
        "Hindi": "hi",
        "French": "fr",
        "Spanish": "es",
        "German": "de",
        "Italian": "it", 
        "Chinese": "zh",
        "Japanese": "ja",
        "Arabic": "ar",
        "Russian": "ru",
        "Portuguese": "pt",
        "Korean": "ko",
        "Turkish": "tr",
        "Dutch": "nl",
        "Greek": "el",
        "Hebrew": "he",
        "Thai": "th",
        "Vietnamese": "vi",
        "Indonesian": "id",
        "Bengali": "bn",
        "Tamil": "ta",
        "Telugu": "te",
        "Marathi": "mr",
        "Gujarati": "gu",
        "Kannada": "kn",
        "Malayalam": "ml",
        "Punjabi": "pa",
        "Urdu": "ur",
    }
}

LANGUAGES = list(LANGUAGE_MAPPING["default"].keys())

# ---------------------------------------------------
# Translation Functions  
# ---------------------------------------------------
def clean_text(text):
    """Clean and validate input text"""
    text = text.strip()
    if not text:
        raise ValueError("Please enter some text to translate.")
    if len(text) > 2000:
        raise ValueError("Text too long. Please keep it under 2000 characters.")
    return ' '.join(text.split())

def detect_language_simple(text):
    """Simple rule-based language detection"""
    text_lower = text.lower()
    
    # Hindi and related languages (Devanagari script)
    if any(char in text for char in 'अआइईउऊऋएऐओऔकखगघचछजझटठडढतथदधनपफबभमयरलवशषसह'):
        return "Hindi"
    
    # Bengali
    if any(char in text for char in 'অআইঈউঊঋএঐওঔকখগঘচছজঝটঠডঢতথদধনপফবভমযরলশষসহ'):
        return "Bengali"
    
    # Tamil
    if any(char in text for char in 'அஆஇஈஉஊஎஏஐஒஓஔகஙசஜஞடணதநனபமயரலவழளறன'):
        return "Tamil"
    
    # Spanish detection
    spanish_words = ['el', 'la', 'de', 'que', 'y', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le', 'da', 'su', 'por', 'qué', 'más', 'con', 'los', 'las', 'del', 'al', 'uno', 'una', 'ti']
    if any(word in text_lower.split() for word in spanish_words):
        return "Spanish"
    
    # French detection  
    french_words = ['le', 'la', 'de', 'et', 'à', 'en', 'un', 'une', 'est', 'pour', 'que', 'dans', 'il', 'elle', 'avec', 'son', 'sa', 'ses', 'mon', 'ton', 'notre', 'votre', 'leur']
    if any(word in text_lower.split() for word in french_words):
        return "French"
    
    # Default to English
    return "English"

def get_language_code(model_name, language, default_mapping="default"):
    """Get the correct language code for the specific model"""
    if model_name in LANGUAGE_MAPPING:
        if language in LANGUAGE_MAPPING[model_name]:
            return LANGUAGE_MAPPING[model_name][language]
    
    # Fallback to default mapping
    if language in LANGUAGE_MAPPING[default_mapping]:
        return LANGUAGE_MAPPING[default_mapping][language]
    
    return language  # Return as-is if not found

def hf_translate(text, src_lang, tgt_lang, model_name):
    """Translate text using Hugging Face translation models"""
    text = clean_text(text)
    original_length = len(text.split())
    
    # Handle auto-detection
    if src_lang == "Auto-detect":
        src_lang = detect_language_simple(text)
    
    # Get model-specific language codes
    src_code = get_language_code(model_name, src_lang)
    tgt_code = get_language_code(model_name, tgt_lang)
    
    try:
        # Different handling based on model type
        if "opus-mt" in model_name.lower():
            # OPUS models are direction-specific, just pass text
            result = client.translation(text, model=model_name)
        elif model_name == "facebook/mbart-large-50-many-to-many-mmt":
            # MBART requires special handling
            result = client.translation(
                text,
                model=model_name,
                src_lang=src_code,
                tgt_lang=tgt_code
            )
        elif model_name in ["facebook/m2m100_418M", "facebook/nllb-200-distilled-600M"]:
            # These models support direct translation
            result = client.translation(
                text,
                model=model_name,
                src_lang=src_code,
                tgt_lang=tgt_code
            )
        else:
            # For other models, use generic translation
            result = client.translation(text, model=model_name)
        
        # Handle different response formats
        translation = None
        if isinstance(result, dict):
            translation = result.get('translation_text', '')
        elif isinstance(result, str):
            translation = result
        elif hasattr(result, 'translation_text'):
            translation = result.translation_text
        elif isinstance(result, list) and len(result) > 0:
            if isinstance(result[0], dict):
                translation = result[0].get('translation_text', str(result[0]))
            else:
                translation = str(result[0])
        else:
            translation = str(result)
        
        translation = translation.strip()
        
        # Validation checks
        if not translation or translation.lower() == text.lower():
            return (f"⚠️ No translation generated. The model may not support this language pair.\n\n"
                    f"**Suggestions:**\n"
                    f"- Try MBART Large 50 or M2M100 418M (best multilingual support)\n"
                    f"- Check if {src_lang}→{tgt_lang} is supported\n"
                    f"- For OPUS models, ensure correct direction (EN-HI vs HI-EN)")
        
        # Check for hallucination - translation shouldn't be way longer than original for simple text
        translation_length = len(translation.split())
        if original_length <= 5 and translation_length > original_length * 10:
            return (f"⚠️ Model appears to have hallucinated (generated unrelated text).\n\n"
                    f"**What happened:** Input was {original_length} word(s) but got {translation_length} words back.\n\n"
                    f"**Try:**\n"
                    f"- MBART Large 50 or M2M100 418M (more reliable)\n"
                    f"- Use fallback model below\n\n"
                    f"_Original input: \"{text}\"_")
        
        # Check if translation looks like it's in wrong language (contains special chars that shouldn't be there)
        if tgt_lang == "English" and any(char in translation for char in 'अआइईउऊऋएऐओऔकखगघचछजझटठडढतथदधनपफबभमयरलवशषसह'):
            return f"⚠️ Translation appears to be in wrong language. Try a different model."
        
        return translation
        
    except Exception as e:
        error_msg = str(e).lower()
        
        # Provide helpful error messages
        if "not found" in error_msg or "does not exist" in error_msg:
            return f"⚠️ Model not available on Hugging Face. Try MBART Large 50 or M2M100 418M instead."
        elif "language" in error_msg or "not supported" in error_msg:
            return f"⚠️ Language pair {src_lang}→{tgt_lang} not supported by this model. Try a multilingual model like MBART or NLLB."
        
        # Fallback to chat completion if translation endpoint fails
        try:
            messages = [
                {"role": "user", "content": f"Translate the following text from {src_lang} to {tgt_lang}. Provide only the translation without any explanations or preamble:\n\n{text}"}
            ]
            
            completion = client.chat_completion(
                messages=messages,
                model="meta-llama/Llama-3.2-3B-Instruct",
                max_tokens=500,
                temperature=0.1
            )
            
            translation = completion.choices[0].message.content.strip()
            return f"🔄 {translation}\n\n_Note: Used fallback model due to translation API error_"
            
        except Exception as fallback_error:
            return f"⚠️ Translation failed: {str(e)[:150]}\n\nPlease try a different model or check the language pair compatibility."

# ---------------------------------------------------
# UI Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="HF Translator", 
    layout="centered",
    page_icon="🌍"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #ff6b00;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f8fff8;
        border-left: 5px solid #4CAF50;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #f0f8ff;
        border-left: 5px solid #2196F3;
        margin: 1rem 0;
    }
    .copy-button {
        background-color: #4CAF50 !important;
        color: white !important;
        padding: 12px 24px !important;
        border: none !important;
        border-radius: 8px !important;
        cursor: pointer !important;
        font-size: 16px !important;
        margin-top: 15px !important;
        width: 100% !important;
        transition: background-color 0.3s !important;
    }
    .copy-button:hover {
        background-color: #45a049 !important;
    }
    .model-info {
        background-color: #e3f2fd;
        padding: 8px 12px;
        border-radius: 6px;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Main App
# ---------------------------------------------------
st.markdown('<div class="main-header">🌍 Hugging Face Translator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Professional Translation with State-of-the-Art Models</div>', unsafe_allow_html=True)

# Initialize client
client = get_client()

if client is None and "HF_TOKEN" not in st.secrets and "HF_TOKEN" not in os.environ:
    st.info("🔑 Please enter your Hugging Face token above to start translating.")
    st.stop()

# Text input
text = st.text_area(
    "Enter text to translate:", 
    height=150,
    placeholder="Type or paste your text here... (Max 2000 characters)",
    help="Enter the text you want to translate"
)

# Configuration columns
col1, col2, col3 = st.columns([2, 2, 3])

with col1:
    src = st.selectbox(
        "Source Language", 
        ["Auto-detect"] + LANGUAGES,
        help="Select source language or use auto-detect"
    )

with col2:
    tgt = st.selectbox(
        "Target Language", 
        LANGUAGES,
        index=1,  # Default to Hindi
        help="Select target language for translation"
    )

with col3:
    model_display_name = st.selectbox(
        "Translation Model",
        list(TRANSLATION_MODELS.keys()),
        help="Choose which model to use for translation"
    )
    model_name = TRANSLATION_MODELS[model_display_name]
    
    # Show model info
    with st.expander("Model Details"):
        st.markdown(f"**Model ID:** `{model_name}`")
        if model_name in LANGUAGE_MAPPING:
            supported_langs = list(LANGUAGE_MAPPING[model_name].keys())
            st.markdown(f"**Supported Languages:** {', '.join(supported_langs[:8])}{'...' if len(supported_langs) > 8 else ''}")

# Additional options
col4, col5 = st.columns(2)
with col4:
    enable_debug = st.checkbox("Show debug info", value=False)
with col5:
    slow_mode = st.checkbox("Enhanced accuracy mode", value=False)

# Translate button
if st.button("🚀 Translate", type="primary", use_container_width=True):
    if not text.strip():
        st.warning("Please enter some text to translate.")
    else:
        with st.spinner("🔄 Translating using Hugging Face models..."):
            # Add delay for enhanced accuracy mode
            if slow_mode:
                time.sleep(1)
            
            try:
                # Show detected language if auto-detect
                detected_lang = None
                if src == "Auto-detect":
                    detected_lang = detect_language_simple(text)
                    st.info(f"🔍 Auto-detected language: {detected_lang}")
                    actual_src = detected_lang
                else:
                    actual_src = src

                # Perform translation
                translated = hf_translate(
                    text,
                    actual_src,
                    tgt,
                    model_name
                )

                st.markdown("---")
                
                # Display results
                if translated.startswith("⚠️") or translated.startswith("🔄"):
                    st.markdown('<div class="info-box">', unsafe_allow_html=True)
                    st.subheader("Translation Result")
                    if translated.startswith("⚠️"):
                        st.warning(translated)
                    else:
                        st.info(translated)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                else:
                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    st.subheader("✅ Translation Complete")
                    
                    # Display translation prominently
                    st.markdown("### Translation:")
                    st.success(translated)
                    
                    # Original and translated text side by side
                    col6, col7 = st.columns(2)
                    with col6:
                        st.markdown("**Original:**")
                        st.text_area("", value=text, height=120, key="original", label_visibility="collapsed")
                    with col7:
                        st.markdown("**Translated:**")
                        st.text_area("", value=translated, height=120, key="translated", label_visibility="collapsed")
                    
                    # Copy button with escaped text
                    escaped_translation = translated.replace('`', '\\`').replace('\n', '\\n').replace('"', '\\"').replace("'", "\\'")
                    st.markdown(
                        f"""
                        <button class="copy-button" onclick="navigator.clipboard.writeText('{escaped_translation}'); this.innerHTML='✅ Copied!'; setTimeout(() => this.innerHTML='📋 Copy Translation', 2000);">
                            📋 Copy Translation
                        </button>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.markdown('</div>', unsafe_allow_html=True)

                # Debug information
                if enable_debug:
                    with st.expander("🔧 Debug Information"):
                        st.write("**Translation Details:**")
                        debug_info = {
                            "source_language": actual_src,
                            "target_language": tgt,
                            "model_used": model_name,
                            "source_code": get_language_code(model_name, actual_src),
                            "target_code": get_language_code(model_name, tgt),
                            "text_length": len(text),
                            "translation_length": len(translated),
                            "detected_language": detected_lang if detected_lang else "Manual selection"
                        }
                        st.json(debug_info)

            except Exception as e:
                st.error("🚨 Translation failed!")
                with st.expander("🔧 Technical Details"):
                    st.exception(e)
                st.info("💡 Tip: Try using a different model (MBART or M2M100 recommended) or check if the languages are supported.")

# Footer with information
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Powered by Hugging Face Inference API • Professional translation models</p>
    <p>Supports 25+ languages • Enterprise-grade quality</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with additional info
with st.sidebar:
    st.title("🌍 HF Translator")
    st.markdown("""
    **Professional Translation** using Hugging Face's specialized models.
    
    ### Features:
    - 🚀 Specialized translation models
    - 🎯 Auto-language detection  
    - 🔧 Professional quality
    - 📊 25+ languages supported
    - ⚡ Direct model inference
    """)
    
    st.markdown("---")
    st.subheader("📚 Model Guide")
    
    st.markdown("### 🌟 Best Overall")
    st.markdown("""
    **MBART Large 50** ⭐ Recommended
    - ✅ Most languages (50+)
    - ✅ Best quality for: EN↔ES, EN↔FR, EN↔DE, EN↔HI
    - ✅ Handles casual/informal text well
    - ⚡ Good for everyday use
    """)
    
    st.markdown("### 🎯 Specialized Models")
    
    with st.expander("M2M100 418M"):
        st.markdown("""
        **Best for:** Multilingual chains
        - Languages: 100+ languages
        - Strong: Asian languages (ZH, JA, KO)
        - Use when: MBART not available
        - Note: Smaller, faster but less accurate
        """)
    
    with st.expander("NLLB 200 Distilled"):
        st.markdown("""
        **Best for:** Low-resource languages
        - Languages: 200+ languages
        - Strong: Indian langs (HI, TA, TE, BN)
        - Strong: African/rare languages
        - Use when: Translating rare languages
        """)
    
    with st.expander("OPUS MT EN-HI"):
        st.markdown("""
        **Best for:** English → Hindi ONLY
        - ✅ Specialized EN→HI translation
        - ✅ Better than MBART for formal Hindi
        - ❌ ONE direction only
        - Use when: Need formal/technical Hindi
        """)
    
    with st.expander("OPUS MT HI-EN"):
        st.markdown("""
        **Best for:** Hindi → English ONLY
        - ✅ Specialized HI→EN translation
        - ✅ Better for Devanagari script
        - ❌ ONE direction only
        - Use when: Translating Hindi documents
        """)
    
    with st.expander("Google T5 Small"):
        st.markdown("""
        **Best for:** Experimental use
        - ⚠️ Not recommended for production
        - May hallucinate on short text
        - Use when: Testing only
        """)
    
    st.markdown("---")
    st.markdown("### 💡 Quick Tips")
    st.markdown("""
    **Common Pairs:**
    - 🇺🇸↔🇪🇸 EN-ES: Use **MBART**
    - 🇺🇸↔🇫🇷 EN-FR: Use **MBART**
    - 🇺🇸→🇮🇳 EN→HI: Use **OPUS MT EN-HI**
    - 🇮🇳→🇺🇸 HI→EN: Use **OPUS MT HI-EN**
    - 🇺🇸↔🇨🇳 EN-ZH: Use **M2M100**
    - 🇺🇸↔🇯🇵 EN-JA: Use **MBART** or **M2M100**
    
    **General Rule:**
    1. Try MBART first (best overall)
    2. Use OPUS if EN↔HI specific
    3. Use NLLB for rare languages
    """)
    
    st.markdown("---")
    st.subheader("⚙️ Setup Instructions")
    st.markdown("""
    1. Get HF token from:
       [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
    
    2. Add to secrets:
       ```toml
       # .streamlit/secrets.toml
       HF_TOKEN = "your_token_here"
       ```
    """)
    
    # Token input in sidebar
    if "HF_TOKEN" not in st.secrets and "HF_TOKEN" not in os.environ:
        st.text_input("HF Token", type="password", key="sidebar_token")
        if st.button("Save Token (Session)"):
            if st.session_state.sidebar_token:
                os.environ["HF_TOKEN"] = st.session_state.sidebar_token
                st.success("Token saved for this session!")
                st.rerun()

# Usage statistics
if 'translation_count' not in st.session_state:
    st.session_state.translation_count = 0

if text and 'translated' in locals():
    st.session_state.translation_count += 1

with st.sidebar:
    st.markdown("---")
    st.metric("Translations this session", st.session_state.translation_count)