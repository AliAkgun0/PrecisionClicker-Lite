from PIL import Image, ImageDraw

# Create a new image with a white background
img = Image.new('RGB', (256, 256), color='white')
draw = ImageDraw.Draw(img)

# Draw a blue circle
draw.ellipse([20, 20, 236, 236], fill='#0d6efd')

# Draw a white mouse cursor symbol
draw.polygon([(128, 40), (180, 128), (128, 100), (76, 128)], fill='white')

# Save as PNG
img.save('assets/icon.png')

# Save as ICO (Windows icon)
img.save('assets/icon.ico', format='ICO') 