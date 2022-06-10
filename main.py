import io

import streamlit as st
from PIL import Image

img1 = st.file_uploader(label='Background (original avatar) - a normal image file')
'---'
img2 = st.file_uploader(label='Overlay (chaos ring) - an image with transparency to be superimposed on '
                              '(put above) the background')
'---'

if img1 and img2:
    img1 = Image.open(img1)
    img2 = Image.open(img2)
    if img2.format != 'PNG':
        st.warning(
            'The overlay image should be in a format that supports transparent parts (e.g. png) in order to be drawn'
            ' above the avatar.')
    w1, h1 = img1.size
    w2, h2 = img2.size
    ratio = min(w1, h1) / min(w2, h2)
    img2 = img2.resize((int(w2 * ratio), int(h2 * ratio)))

    w1, h1 = img1.size
    w2, h2 = img2.size
    img1.paste(img2,
               (w1 // 2 - w2 // 2, h1 // 2 - h2 // 2),  # center img2 in img1
               mask=img2)

    st.image(img1)

    buffer = io.BytesIO()
    img1.save(buffer, format='JPEG')

    st.download_button(label='Download new avatar',
                       data=buffer.getvalue(),
                       file_name=f'new_avatar.jpeg',
                       mime='image/jpeg')
