import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# --- Streamlit page config ---
st.set_page_config(page_title="PromptWall – AI Wallpaper", page_icon="🖼️")

st.title("🎨 PromptWall")
st.caption("Generate a beautiful wallpaper from your prompt using AI")

# --- Prompt input ---
prompt = st.text_input("Enter your wallpaper prompt", placeholder="e.g., A futuristic city skyline at sunset")

# --- Hugging Face API setup (uses a public free model) ---
API_URL = "https://api-inference.huggingface.co/models/prompthero/openjourney"
headers = {"Authorization": f"Bearer {st.secrets['hf_token']}"}

# --- Image generation function ---
def generate_image(prompt):
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200 and "image" in response.headers.get("content-type", ""):
        return Image.open(BytesIO(response.content))
    else:
        return None

# --- Generate button ---
if st.button("✨ Create Wallpaper"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Generating your wallpaper..."):
            image = generate_image(prompt)
            if image:
                st.image(image, caption="🖼️ Your AI Wallpaper", use_container_width=True)
                buf = BytesIO()
                image.save(buf, format="PNG")
                st.download_button("📥 Download", buf.getvalue(), "wallpaper.png")
            else:
                st.error("Failed to generate image. Try again with a simpler prompt or check your API token.")

# --- Footer ---
st.markdown("---")
st.markdown("Made with ❤️ using Hugging Face + Streamlit")
