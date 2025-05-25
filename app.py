import streamlit as st
import requests
import re

# -------------------- Page Configuration --------------------
st.set_page_config(page_title="PromptWall – AI Wallpaper Generator", page_icon="🖼️", layout="centered")

st.title("🖼️ PromptWall")
st.caption("Create stunning wallpapers using AI (Stable Diffusion)")

# -------------------- Prompt Input --------------------
prompt = st.text_input("🎨 Enter a prompt for your wallpaper:", placeholder="e.g., A dreamlike forest in the morning fog")

# -------------------- Supported Resolutions --------------------
supported_resolutions = [
    "256x256",
    "384x384",
    "512x512",
    "512x768",
    "768x512",
    "768x768",
    "1024x1024",
    "Custom"
]

st.markdown("### Select or enter custom resolution")

resolution_option = st.selectbox(
    "🖼️ Select resolution:",
    options=supported_resolutions,
    index=2  # default to 512x512
)

custom_resolution = ""
if resolution_option == "Custom":
    custom_resolution = st.text_input("Enter custom resolution (WIDTHxHEIGHT), e.g., 1280x720")

def valid_resolution(res):
    # Check format: digits x digits, both divisible by 64
    match = re.match(r"^(\d+)x(\d+)$", res.strip())
    if not match:
        return False
    width, height = int(match.group(1)), int(match.group(2))
    return width % 64 == 0 and height % 64 == 0

# Determine which resolution to use
if resolution_option == "Custom":
    if valid_resolution(custom_resolution):
        resolution = custom_resolution.strip()
    else:
        resolution = None
else:
    resolution = resolution_option

if resolution is None and resolution_option == "Custom":
    st.warning("Please enter a valid custom resolution. Both width and height must be multiples of 64 (e.g., 1280x704).")

# -------------------- Hugging Face API Settings --------------------
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
headers = {"Authorization": f"Bearer {st.secrets['hf_token']}"}

# -------------------- Inference Function --------------------
def query_huggingface(prompt, resolution):
    # Note: The Hugging Face SD API doesn't support custom resolution in payload.
    # You can add support if using a different API.
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

# -------------------- Generate Button --------------------
if st.button("✨ Generate Wallpaper"):
    if not prompt:
        st.warning("Please enter a prompt first.")
    elif resolution is None:
        st.warning("Please enter a valid resolution.")
    else:
        with st.spinner("Generating your wallpaper..."):
            try:
                image_bytes = query_huggingface(prompt, resolution)
                st.image(image_bytes, caption=f"🖼️ Your AI Wallpaper ({resolution})", use_column_width=True)
                st.download_button("📥 Download Image", image_bytes, file_name="wallpaper.png")
            except Exception as e:
                st.error(f"⚠️ Error generating image: {e}")

# -------------------- Footer --------------------
st.markdown("---")
st.markdown("Created by **CibirajGL** | Powered by 🤗 Hugging Face + Streamlit")
