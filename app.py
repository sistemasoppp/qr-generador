from flask import Flask, render_template, request, send_file
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image, ImageDraw, ImageFilter
import io
import os

app = Flask(__name__)

def generate_qr_image(data_url, logo_file=None):
    qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_H, 
        box_size=15,
        border=4,
    )
    qr.add_data(data_url)
    qr.make(fit=True)

    img_qr = qr.make_image(
        image_factory=StyledPilImage, 
        module_drawer=RoundedModuleDrawer(),
        color_mask=SolidFillColorMask(back_color=(255, 255, 255), front_color=(0, 153, 82))
    ).convert('RGB')

    img_qr = img_qr.filter(ImageFilter.SMOOTH_MORE)

    base_width, base_height = img_qr.size
    draw = ImageDraw.Draw(img_qr)

    centro_x, centro_y = base_width // 2, base_height // 2
    radio_blanco = int(base_width * 0.16)

    draw.ellipse(
        [centro_x - radio_blanco, centro_y - radio_blanco, 
         centro_x + radio_blanco, centro_y + radio_blanco], 
        fill=(255, 255, 255)
    )

    logo = None
    if logo_file:
        logo = Image.open(logo_file).convert("RGBA")
    else:
        logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
        if os.path.exists(logo_path):
            logo = Image.open(logo_path).convert("RGBA")

    if logo:
        logo_size = int(radio_blanco * 1.5)
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        
        pos_x = centro_x - (logo_size // 2)
        pos_y = centro_y - (logo_size // 2)
        
        # Create a mask to respect the alpha channel when pasting
        mask = logo.split()[3] if len(logo.split()) == 4 else logo
        img_qr.paste(logo, (pos_x, pos_y), mask)

    # Save to memory
    img_io = io.BytesIO()
    img_qr.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generar', methods=['POST'])
def generar():
    url = request.form.get('url', '')
    
    if not url:
        return {"error": "URL is required"}, 400

    logo_file = request.files.get('logo')

    try:
        img_io = generate_qr_image(url, logo_file)
        return send_file(img_io, mimetype='image/png', as_attachment=False, download_name='qr_institucional.png')
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
