import streamlit as st
import requests
import time

# Theme enforcement
def set_theme():
    theme = {
        "base": "light",
        "primaryColor": "#7e29cd",
        "backgroundColor": "#f0f0f0",  # Your custom background
        "secondaryBackgroundColor": "#ffffff",
        "textColor": "#31333f"
    }
    st.markdown(f"""<style>
        :root {{
            --primary-color: {theme['primaryColor']};
            --background-color: {theme['backgroundColor']};
            --secondary-background-color: {theme['secondaryBackgroundColor']};
            --text-color: {theme['textColor']};
        }}
        .stApp {{
            background-color: var(--background-color);
        }}
    </style>""", unsafe_allow_html=True)

set_theme()

# Rest of your existing code below...
# [Keep all your previous UI and logic components]


# Check for API key
if 'HF_API_KEY' not in st.secrets:
    st.error("🔑 API key missing! Follow these steps:")
    st.markdown("""
    1. Get Hugging Face token from [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
    2. In Streamlit Cloud → Settings → Secrets → Add:
       ```toml
       HF_API_KEY = "your_token_here"
       ```
    """)
    st.stop()

API_KEY = st.secrets.HF_API_KEY

# ========== UI Components ========== #
st.title("AI Wallpaper Studio 🖼️")

# Style presets
STYLE_PRESETS = {
    "🎨 Default": "",
    "🌃 Cyberpunk": "cyberpunk style, neon lights, futuristic cityscape",
    "🖼️ Watercolor": "watercolor painting, soft edges, pastel colors",
    "🌌 Space": "cosmic landscape, vibrant nebulae, 8k resolution",
    "🍂 Minimalist": "minimalist design, simple shapes, muted colors",
    "🐉 Fantasy": "epic fantasy landscape, magical aura, digital art"
}

# Resolution options
RESOLUTIONS = {
    "🖼️ 512x512": (512, 512),
    "📱 768x1024 (Mobile)": (768, 1024),
    "🖥️ 1024x576 (Widescreen)": (1024, 576),
    "🌟 1024x1024": (1024, 1024)
}

# Main UI
col1, col2 = st.columns(2)
with col1:
    style = st.selectbox("Style preset:", list(STYLE_PRESETS.keys()))
with col2:
    resolution = st.selectbox("Resolution:", list(RESOLUTIONS.keys()))

prompt = st.text_input("Describe your wallpaper:", 
                      placeholder="e.g. 'A futuristic city under northern lights'")

with st.expander("⚙️ Advanced Settings"):
    negative_prompt = st.text_input("Exclude from image:", 
                                  "low quality, blurry, text, watermark")
    guidance_scale = st.slider("Creativity level:", 1.0, 20.0, 7.5)
    steps = st.slider("Generation steps:", 10, 100, 25)

# Generation logic
if st.button("✨ Generate Wallpaper"):
    if not prompt:
        st.warning("Please enter a description!")
        st.stop()

    final_prompt = f"{prompt}, {STYLE_PRESETS[style]}" if style != "🎨 Default" else prompt
    width, height = RESOLUTIONS[resolution]

    payload = {
        "inputs": final_prompt,
        "parameters": {
            "width": width,
            "height": height,
            "negative_prompt": negative_prompt,
            "guidance_scale": guidance_scale,
            "num_inference_steps": steps
        }
    }

    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        with st.spinner("🚀 Generating your wallpaper..."):
            headers = {"Authorization": f"Bearer {API_KEY}"}
            
            # Progress animation
            for percent in range(0, 101, 10):
                progress_bar.progress(percent)
                status_text.text(f"Progress: {percent}%")
                time.sleep(0.1)
            
            response = requests.post(API_URL, headers=headers, json=payload)
            
            if response.status_code == 200:
                st.image(response.content, use_container_width=True)
                
                # Download button
                st.download_button(
                    label="⬇️ Download Wallpaper",
                    data=response.content,
                    file_name=f"wallpaper_{width}x{height}.png",
                    mime="image/png"
                )
                
            elif response.status_code == 503:
                st.error("Model loading... Please wait 20 seconds and try again")
            else:
                st.error(f"API Error {response.status_code}: {response.text}")
                
    except Exception as e:
        st.error(f"🚨 Error: {str(e)}")
    finally:
        progress_bar.empty()
        status_text.empty()

# Footer
st.markdown("---")
st.caption("Pro Tip: Use terms like '4K resolution' or 'trending on ArtStation' for better results")
