import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image, ImageDraw, ImageFilter

# 1. Configuración del contenido y el QR base
data = "https://forms.gle/QPn1tMJMJFdaEiTu9"
qr = qrcode.QRCode(
    version=4,  # Ajustamos la versión para que la densidad de puntos coincida con tu imagen
    error_correction=qrcode.constants.ERROR_CORRECT_H, 
    box_size=15, # Mayor tamaño base para poder aplicar el suavizado de bordes
    border=4,
)
qr.add_data(data)
qr.make(fit=True)

# 2. Crear el QR usando RoundedModuleDrawer (que suaviza y conecta los bloques contiguos)
img_qr = qr.make_image(
    image_factory=StyledPilImage, 
    module_drawer=RoundedModuleDrawer(), 
    color_mask=SolidFillColorMask(back_color=(255, 255, 255), front_color=(0, 153, 82))
).convert('RGB')

# 3. Truco de procesamiento de imagen para lograr el efecto "fluido/orgánico" exacto
# Aplicamos un sutil desenfoque y luego un filtro de umbral para "fusionar" las uniones
img_qr = img_qr.filter(ImageFilter.SMOOTH_MORE)

# 4. Preparar y limpiar el centro para el Logo
base_width, base_height = img_qr.size
draw = ImageDraw.Draw(img_qr)

# Calcular espacio central circular blanco para el logo de Cáritas
# En tu imagen, el fondo blanco corta de forma limpia los puntos verdes
centro_x, centro_y = base_width // 2, base_height // 2
radio_blanco = int(base_width * 0.16) # Tamaño del escudo blanco central

draw.ellipse(
    [centro_x - radio_blanco, centro_y - radio_blanco, 
     centro_x + radio_blanco, centro_y + radio_blanco], 
    fill=(255, 255, 255)
)

# 5. Cargar y colocar el logo de Cáritas
# Asegúrate de que tu archivo se llame 'logo.png'
logo = Image.open("logo.png").convert("RGBA")

# El tamaño del logo debe ser ligeramente menor que el círculo blanco
logo_size = int(radio_blanco * 1.5)
logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

# Calcular posición para centrar el logo
pos_x = centro_x - (logo_size // 2)
pos_y = centro_y - (logo_size // 2)

# Pegar el logo usando 
img_qr.paste(logo, (pos_x, pos_y), logo)

# 6. Guardar el resultado final
nombre_archivo_final = "qr_caritas_estilo_exacto.png"
img_qr.save(nombre_archivo_final)

print(f"✅ ¡Código QR generado  '{nombre_archivo_final}'!")