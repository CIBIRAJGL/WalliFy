import streamlit as st
import requests

# -------------------- Page Configuration --------------------
st.set_page_config(page_title="PromptWall – AI Wallpaper Generator", page_icon="🖼️", layout="centered")

st.title("🖼️ PromptWall")
st.caption("Create stunning wallpapers using AI (Stable Diffusion)")

# -------------------- Prompt Input --------------------
prompt = st.text_input("🎨 Enter a prompt for your wallpaper:", placeholder="e.g., A dreamlike forest in the morning fog")

# -------------------- Image Resolution Option --------------------
resolution = st.selectbox(
    "🖼️ Select resolution:",
    options=["1024x1024", "1024x1792", "1792x1024"],
    index=0
)

# -------------------- Hugging Face API Settings --------------------
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
headers = {"Authorization": f"Bearer {st.secrets['hf_token']}"}

# -------------------- Inference Function --------------------
def query_huggingface(prompt):
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

# -------------------- Generate Button --------------------
if st.button("✨ Generate Wallpaper"):
    if not prompt:
        st.warning("Please enter a prompt first.")
    else:
        with st.spinner("Generating your wallpaper..."):
            try:
                image_bytes = query_huggingface(prompt)
                st.image(image_bytes, caption="🖼️ Your AI Wallpaper", use_column_width=True)
                st.download_button("📥 Download Image", image_bytes, file_name="wallpaper.png")
            except Exception as e:
                st.error(f"⚠️ Error generating image: {e}")

# -------------------- Footer --------------------
st.markdown("---")
st.markdown("Created by **CibirajGL** | Powered by 🤗 Hugging Face + Streamlit")
