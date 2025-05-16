import streamlit as st
from PIL import Image
import io
from mosaic_generator import generate_photo_mosaic

st.title("📸 Selfie to Photo Mosaic")

selfie_file = st.file_uploader("Upload a selfie image", type=["jpg", "jpeg", "png"])
filler_files = st.file_uploader("Upload filler images (10–100 recommended)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

grid_size = st.slider("Mosaic Grid Size (Higher = more tiles)", min_value=10, max_value=100, value=30)

if selfie_file and filler_files:
    selfie_img = Image.open(selfie_file).convert("RGB")
    filler_imgs = [Image.open(f).convert("RGB") for f in filler_files]

    with st.spinner("Generating mosaic..."):
        mosaic_img = generate_photo_mosaic(selfie_img, filler_imgs, grid_size=grid_size)

    st.subheader("Mosaic Output")
    st.image(mosaic_img, use_column_width=True)

    # Download button
    buf = io.BytesIO()
    mosaic_img.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="Download Mosaic Image",
        data=byte_im,
        file_name="photo_mosaic.png",
        mime="image/png"
    )
