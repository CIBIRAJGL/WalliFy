import streamlit as st
import requests
import time

# Hugging Face Configuration
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

# App Configuration
st.set_page_config(
    page_title="AI Wallpaper Studio",
    page_icon="🎨",
    layout="centered"
)

# Authentication Check
if 'HF_API_KEY' not in st.secrets:
    st.error("🔑 Authentication Required")
    st.markdown("""
    1. Get API key from [Hugging Face](https://huggingface.co/settings/tokens)
    2. Add to Streamlit Cloud secrets as `HF_API_KEY`
    """)
    st.stop()

API_KEY = st.secrets.HF_API_KEY

# ========== UI Components ========== #
st.title("AI Wallpaper Studio")

# Style Presets
STYLE_PRESETS = {
    "🎨 Default": "",
    "🌃 Cyberpunk": "cyberpunk style, neon lights, futuristic cityscape",
    "🖼️ Watercolor": "watercolor painting, soft edges, pastel colors",
    "🌌 Space": "cosmic landscape, vibrant nebulae, 8k resolution"
}

# Resolution Options
RESOLUTIONS = {
    "🖼️ 512x512": (512, 512),
    "📱 768x1024 (Mobile)": (768, 1024),
    "🖥️ 1024x576 (Widescreen)": (1024, 576)
}

# Main Interface
col1, col2 = st.columns(2)
with col1:
    style = st.selectbox(
        "Style preset:",
        list(STYLE_PRESETS.keys()),
        help="Select a visual style for your wallpaper"
    )
    
with col2:
    resolution = st.selectbox(
        "Resolution:",
        list(RESOLUTIONS.keys()),
        help="Choose output dimensions"
    )

prompt = st.text_input(
    "Describe your wallpaper:",
    placeholder="e.g. 'A futuristic city under northern lights'",
    help="Be descriptive for best results!"
)

# Advanced Settings
with st.expander("⚙️ Advanced Options"):
    negative_prompt = st.text_input(
        "Exclude elements:",
        "low quality, blurry, text",
        help="Elements to remove from the image"
    )
    guidance = st.slider("Creativity Level:", 5.0, 15.0, 7.5)
    steps = st.slider("Generation Steps:", 20, 50, 25)

# Generation Button
if st.button("✨ Generate Wallpaper", type="primary"):
    if not prompt:
        st.warning("Please enter a description!")
        st.stop()

    # Build final prompt
    final_prompt = f"{prompt}, {STYLE_PRESETS[style]}" if style != "🎨 Default" else prompt
    width, height = RESOLUTIONS[resolution]

    # API Payload
    payload = {
        "inputs": final_prompt,
        "parameters": {
            "width": width,
            "height": height,
            "negative_prompt": negative_prompt,
            "guidance_scale": guidance,
            "num_inference_steps": steps
        }
    }

    # Progress UI
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        with st.spinner("🚀 Generating your masterpiece..."):
            headers = {"Authorization": f"Bearer {API_KEY}"}
            
            # Simulated progress
            for pct in range(0, 101, 10):
                progress_bar.progress(pct)
                status_text.text(f"Progress: {pct}%")
                time.sleep(0.15)
            
            # API Call
            response = requests.post(API_URL, headers=headers, json=payload)
            
            if response.status_code == 200:
                # Display results
                st.image(response.content, use_container_width=True)
                
                # Download button
                st.download_button(
                    label="⬇️ Download Wallpaper",
                    data=response.content,
                    file_name=f"wallpaper_{width}x{height}.png",
                    mime="image/png",
                    type="primary"
                )
                
            elif response.status_code == 503:
                st.error("Model loading... Please wait 20 seconds and try again")
            else:
                st.error(f"Generation failed (Error {response.status_code})")

    except Exception as e:
        st.error(f"Critical error: {str(e)}")
    finally:
        progress_bar.empty()
        status_text.empty()
#
