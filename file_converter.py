import streamlit as st
import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont
import io

def create_error_image(text):
    img = Image.new('RGB', (600, 800), color = (250, 250, 250))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        font = ImageFont.load_default()
    
    text_bbox = d.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (600 - text_width) / 2
    y = (800 - text_height) / 2
    
    d.text((x, y), text, fill=(239, 68, 68), font=font)
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

def process_uploaded_file(uploaded_file):
    file_bytes = uploaded_file.getvalue()
    file_extension = uploaded_file.name.split('.')[-1].lower()

    if file_extension == 'pdf':
        try:
            pdf_doc = fitz.open(stream=file_bytes, filetype="pdf")
            page = pdf_doc.load_page(0)
            pix = page.get_pixmap(dpi=150)
            return pix.tobytes("png")
        except Exception as e:
            st.error(f"Erro ao converter PDF: {e}")
            return None
    elif file_extension in ['png', 'jpg', 'jpeg', 'gif']:
        return file_bytes
    else:
        st.error(f"Tipo de ficheiro '{file_extension}' não suportado.")
        return None
