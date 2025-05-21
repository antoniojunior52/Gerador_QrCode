from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import qrcode
from PIL import Image, ImageDraw
import base64
from io import BytesIO
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def generate_qrcode(content: str = Form(...)):
    # Configura QR Code
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(content)
    qr.make(fit=True)

    # Cria imagem base
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    draw = ImageDraw.Draw(img)

    # Tenta carregar o logo
    try:
        icon_path = os.path.join(os.path.dirname(__file__), "image", "logo.png")
        icon = Image.open(icon_path)

        # Redimensiona o logo
        qr_width, qr_height = img.size
        icon_size = qr_width // 4
        icon = icon.resize((icon_size, icon_size), Image.Resampling.LANCZOS)

        # Calcula a posição central
        pos = ((qr_width - icon_size) // 2, (qr_height - icon_size) // 2)

        # Limpa um espaço no QR para o logo (desenha um quadrado branco)
        draw.rectangle(
            [pos, (pos[0] + icon_size, pos[1] + icon_size)],
            fill="white"
        )

        # Cola o logo com transparência (se tiver)
        img.paste(icon, pos, mask=icon if icon.mode == "RGBA" else None)

    except FileNotFoundError:
        print("⚠️ 'logo.png' não encontrado em ./images — QR será gerado sem ícone.")

    # Converte para base64
    buf = BytesIO()
    img.save(buf, format="PNG")
    img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    return JSONResponse(content={"image": f"data:image/png;base64,{img_base64}"})
