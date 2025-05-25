import streamlit as st
import requests

st.set_page_config(page_title="AI Wallpaper Generator", layout="centered")
st.title("🎨 Prompt to Wallpaper")

# Prompt Input
prompt = st.text_input("Enter your prompt for the wallpaper:")

# Generate Button
if st.button("Generate"):
    if not prompt:
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Generating image..."):
            try:
                response = requests.post(
                    "https://api.deepai.org/api/text2img",
                    data={"text": prompt},
                    headers={"api-key": st.secrets["deepai_key"]}
                )
                image_url = response.json()["output_url"]
                st.image(image_url, caption="Your AI Wallpaper", use_container_width=True)
                st.markdown(f"[📥 Download Image]({image_url})")
            except Exception as e:
                st.error(f"Error: {e}")
