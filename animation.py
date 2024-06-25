import numpy as np
from PIL import Image

# Load the logo image
logo = Image.open("logo.png").convert("RGBA")

def generate(res):
    # Create an image
    img = np.zeros((res[1], res[0], 3), dtype=np.uint8)

    # Define the starting position and direction of the logo
    if not hasattr(generate, "x"):
        generate.x = 0
    if not hasattr(generate, "y"):
        generate.y = 0
    if not hasattr(generate, "dx"):
        generate.dx = 1
    if not hasattr(generate, "dy"):
        generate.dy = 1

    # Paste the logo onto the image at the current position
    img[generate.y:generate.y+logo.height, generate.x:generate.x+logo.width] = np.array(logo)[:,:,:3]

    # Update the direction of the logo
    generate.x += generate.dx
    generate.y += generate.dy
    if generate.x < 0 or generate.x + logo.width > res[0]:
        generate.dx = -generate.dx
        generate.x += generate.dx
    if generate.y < 0 or generate.y + logo.height > res[1]:
        generate.dy = -generate.dy
        generate.y += generate.dy

    # Convert the image to a PIL Image object
    image = Image.fromarray(img)

    return image