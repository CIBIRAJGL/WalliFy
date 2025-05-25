import streamlit as st
import requests
import re

# Page config
st.set_page_config(page_title="PromptWall – AI Wallpaper Generator", page_icon="🖼️", layout="centered")

st.title("🖼️ PromptWall")
st.caption("Create stunning wallpapers using AI (Stable Diffusion)")

# Prompt input
prompt = st.text_input("🎨 Enter a prompt for your wallpaper:", placeholder="e.g., A dreamlike forest in the morning fog")

st.markdown("### Select or enter custom resolution")

# Supported resolutions
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

resolution_option = st.selectbox(
    "🖼️ Select resolution:",
    options=supported_resolutions,
    index=2
)

custom_resolution = ""
if resolution_option == "Custom":
    # Add some vertical spacing before custom input
    st.write("")  # empty line for spacing
    custom_resolution = st.text_input("Enter custom resolution (WIDTHxHEIGHT), e.g., 1280x704")

def valid_resolution(res):
    match = re.match(r"^(\d+)x(\d+)$", res.strip())
    if not match:
        return False
    width, height = int(match.group(1)), int(match.group(2))
    return width % 64 == 0 and height % 64 == 0

if resolution_option == "Custom":
    if custom_resolution == "":
        resolution = None
        st.info("Please enter a custom resolution (both width and height must be multiples of 64).")
    elif not valid_resolution(custom_resolution):
        resolution = None
        st.error("Invalid format or values! Width and height must be multiples of 64, e.g., 1280x704.")
    else:
        resolution = custom_resolution.strip()
else:
    resolution = resolution_option

# The rest of your app...

# For demonstration, show chosen resolution
if resolution:
    st.markdown(f"**Selected resolution:** {resolution}")

# [Your existing API call and image generation code here]
