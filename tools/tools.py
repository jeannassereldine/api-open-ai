import base64
from io import BytesIO
from pdf2image import convert_from_bytes
from langgraph.config import get_stream_writer

def pdf_base64_to_images_base64(pdf_base64: str, dpi=200, img_format="PNG"):
    """
    Convert a base64-encoded PDF to a list of base64-encoded images (one per page).
    Args:
        pdf_base64 (str): Base64 string of PDF file.
        dpi (int): Resolution for the output images.
        img_format (str): Output image format, e.g., "PNG" or "JPEG".

    Returns:
        List[str]: Base64 strings of images, one per page.
    """
    
    if pdf_base64.startswith("data:application/pdf;base64,"):
     pdf_base64 = pdf_base64.split(",", 1)[1]
    
    # Decode PDF from base64
    pdf_bytes = base64.b64decode(pdf_base64)

    # Convert PDF pages to PIL Images
    images = convert_from_bytes(pdf_bytes, dpi=dpi)
    writer = get_stream_writer()
    writer('Start processing pdf\n')

    # Convert each page to base64
    base64_images = []
    for img in images:
        buffer = BytesIO()
        img.save(buffer, format=img_format)
        img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        base64_images.append(img_b64)
    writer('PDF converted to images')

    return base64_images
