import io

import streamlit as st
from PIL import Image, ImageOps, ImageDraw

img1 = st.file_uploader(label='Background (original avatar) - a normal image file',
                        help='Supports Square, Portrait and Landscape orientation - the top image is centered above '
                             'the background.')
'---'
img2 = st.file_uploader(label='Overlay (chaos ring) - an image with transparency to be superimposed on '
                              '(put above) the background',
                        help='This image should support transparency to be used as a top layer. Try using a png file.')
'---'


def _is_transparent(pixel):
    return pixel[3] == 0


if img1 and img2:
    img1 = Image.open(img1).convert('RGBA')
    img2 = Image.open(img2)

    if not img2.format or img2.format.lower() != 'png':
        st.warning(
            'The overlay image should be in a format that supports transparency (e.g. png) in order to be drawn'
            ' above the avatar.')
        st.stop()

    # Calculate the width of the ring
    # First, rescale the ring to the size of the original image
    img2 = ImageOps.contain(img2, size=img1.size)
    # Second, take a look at the middle column (just the top half ot it) and count non-transparent pixels
    x = round(img2.width / 2)
    circumference_width = sum([1 if not _is_transparent(img2.getpixel((x, y))) else 0
                               for y in range(0, img2.height//2)])

    img1 = ImageOps.expand(img1, border=round(circumference_width))
    img2 = ImageOps.contain(img2, size=img1.size)
    alpha_mask = Image.new("L", img2.size, 0)
    ImageDraw.Draw(alpha_mask)\
        .ellipse((0, 0) + alpha_mask.size, fill=255)

    # Calculate the position of the ring (and the mask)
    top_left_mask = (img1.width // 2 - img2.width // 2, img1.height // 2 - img2.height // 2)
    mask = Image.new("L", img1.size, 0)

    # Paste the ring and the mask
    img1.paste(img2, top_left_mask, mask=img2)
    mask.paste(alpha_mask, top_left_mask, alpha_mask)
    img1.putalpha(mask)

    # Crop the image back to the original size, matching the ring
    img1 = img1.crop((top_left_mask[0], top_left_mask[1], top_left_mask[0] + img2.width, top_left_mask[1] + img2.height))

    st.image(img1)

    buffer = io.BytesIO()
    img1.save(buffer, format='png')

    st.download_button(label='Download new avatar',
                       data=buffer.getvalue(),
                       file_name=f'new_avatar.png',
                       mime=f'image/png')
