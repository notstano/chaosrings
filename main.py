import io

import streamlit as st
from PIL import Image, ImageOps

img1 = st.file_uploader(label='Background (original avatar) - a normal image file',
                        help='Supports Square, Portrait and Landscape orientation - the top image is centered above '
                             'the background.')
'---'
img2 = st.file_uploader(label='Overlay (chaos ring) - an image with transparency to be superimposed on '
                              '(put above) the background',
                        help='This image should support transparency to be used as a top layer. Try using a png file.')
'---'


def _empty_pixel(pixel):
    return sum(pixel[0:3]) == 0


if img1 and img2:
    img1 = Image.open(img1).convert("RGBA")
    img2 = Image.open(img2).convert("RGBA")

    if img2.format and img2.format.lower() != 'png':
        st.warning(
            'The overlay image should be in a format that supports transparent parts (e.g. png) in order to be drawn'
            ' above the avatar.')

    img2 = ImageOps.contain(img2, size=img1.size)

    x = round(img2.width / 2)
    circumference_width = sum([1 if not _empty_pixel(img2.getpixel((x, y))) else 0
                               for y in range(0, img2.height//2)])

    # The Regulars Ring is not symmetric and a little tweaking helps.
    # 2 is for the way borders work in expand
    # .25 is manual adjustment for the Regulars ring
    img1 = ImageOps.expand(img1, border=round(circumference_width * 2.25))
    img2 = ImageOps.contain(img2, size=img1.size)

    img1 = Image.alpha_composite(img1, img2)
    st.image(img1)

    buffer = io.BytesIO()
    img1.save(buffer, format='png')

    st.download_button(label='Download new avatar',
                       data=buffer.getvalue(),
                       file_name=f'new_avatar.png',
                       mime=f'image/png')
