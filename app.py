import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# --- Page Setup ---
st.set_page_config(page_title="AI Wallpaper Generator", layout="centered")
st.title("🖼️ Prompt-based AI Wallpaper Generator")

# --- Prompt Input ---
prompt = st.text_input("Enter your wallpaper prompt:", placeholder="e.g. Sunset over a calm lake")

# --- Hugging Face API ---
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
headers = {"Authorization": f"Bearer {st.secrets['hf_token']}"}

def generate_image(prompt):
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    return response.content

# --- Generate Button ---
if st.button("✨ Generate Wallpaper"):
    if not prompt:
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Generating..."):
            try:
                image_data = generate_image(prompt)
                image = Image.open(BytesIO(image_data))
                st.image(image, caption="Your AI Wallpaper", use_container_width=True)
                st.download_button("📥 Download", image_data, file_name="wallpaper.png")
            except Exception as e:
                st.error("❌ Failed to generate image. Try a simpler prompt or check your Hugging Face token.")

# --- Footer ---
st.markdown("---")
st.caption("Made with ❤️ using Streamlit + Hugging Face")
