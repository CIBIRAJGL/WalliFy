import streamlit as st
import requests
import re
from PIL import Image
from io import BytesIO

# -------------------- Page Configuration --------------------
st.set_page_config(page_title="PromptWall – AI Wallpaper Generator", page_icon="🖼️", layout="centered")

st.title("🖼️ PromptWall")
st.caption("Create stunning wallpapers using AI (Stable Diffusion)")

# -------------------- Prompt Input --------------------
prompt = st.text_input("🎨 Enter a prompt for your wallpaper:", placeholder="e.g., A dreamlike forest in the morning fog")

# -------------------- Resolution Selection --------------------
st.markdown("### Select or enter a custom resolution")

supported_resolutions = [
    "256x256",
    "384x384",
    "512x512",
    "512x768",
    "768x512",
    "768x768",
    "1024x1024",
    "1024x1792",
    "1792x1024",
    "Custom"
]

selected_option = st.selectbox("🖼️ Select resolution:", supported_resolutions, index=6)

custom_resolution = ""
if selected_option == "Custom":
    custom_resolution = st.text_input("Enter custom resolution (WIDTHxHEIGHT)", placeholder="e.g., 1280x704")

def is_valid_resolution(res):
    match = re.match(r"^(\d+)x(\d+)$", res.strip())
    if not match:
        return False
    width, height = int(match.group(1)), int(match.group(2))
    return width % 64 == 0 and height % 64 == 0

# Final resolution to use
if selected_option == "Custom":
    if is_valid_resolution(custom_resolution):
        resolution = custom_resolution.strip()
        st.success(f"Using custom resolution: {resolution}")
    else:
        resolution = None
        if custom_resolution != "":
            st.error("Invalid resolution. Width and height must be multiples of 64 (e.g., 1280x704).")
else:
    resolution = selected_option

# -------------------- Hugging Face API Settings --------------------
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
headers = {"Authorization": f"Bearer {st.secrets['hf_token']}"}

def query_huggingface(prompt):
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code != 200 or "image" not in response.headers.get("content-type", ""):
        raise Exception(f"API Error: {response.status_code} - {response.text}")
    
    return response.content

# -------------------- Generate Button --------------------
st.write("")  # spacing

if st.button("✨ Generate Wallpaper"):
    if not prompt:
        st.warning("Please enter a prompt first.")
    elif not resolution:
        st.warning("Please select or enter a valid resolution.")
    else:
        with st.spinner("Generating your wallpaper..."):
            try:
                image_bytes = query_huggingface(prompt)
                image = Image.open(BytesIO(image_bytes))
                st.image(image, caption=f"🖼️ Wallpaper ({resolution})", use_container_width=True)
                st.download_button("📥 Download Image", image_bytes, file_name="wallpaper.png")
            except Exception as e:
                st.error(f"⚠️ Error generating image: {e}")

# -------------------- Footer --------------------
st.markdown("---")
st.markdown("Created by **CibirajGL** | Powered by 🤗 Hugging Face + Streamlit")
