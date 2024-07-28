from PIL import Image

def add_logo_watermark(input_image_path, output_image_path, logo_path, position=("center", "center"), transparency=128):
    # Open the base image
    base_image = Image.open(input_image_path).convert("RGBA")
    width, height = base_image.size

    # Open the watermark (logo) image
    logo = Image.open(logo_path).convert("RGBA")
    
    # Resize logo to be 40% of the width of the base image (adjust as needed)
    logo_width, logo_height = logo.size
    desired_logo_width = int(width * 0.25)  # 40% of the image width
    if logo_width > desired_logo_width:
        ratio = desired_logo_width / float(logo_width)
        new_logo_size = (int(logo_width * ratio), int(logo_height * ratio))
        logo = logo.resize(new_logo_size, Image.Resampling.LANCZOS)

    # Adjust the logo transparency
    alpha = logo.split()[3]  # Get the alpha channel
    alpha = alpha.point(lambda p: p * (transparency / 255.0))  # Modify transparency
    logo.putalpha(alpha)  # Apply modified alpha back to the logo

    # Position logo
    logo_width, logo_height = logo.size
    if position[0] == "center":
        x = (width - logo_width) // 2
    elif position[0] == "right":
        x = width - logo_width - 10
    else:
        x = 10

    if position[1] == "center":
        y = (height - logo_height) // 2
    elif position[1] == "bottom":
        y = height - logo_height - 10
    else:
        y = 10

    # Create a new image with transparency for watermarking
    watermark = Image.new("RGBA", base_image.size, (0, 0, 0, 0))
    watermark.paste(logo, (x, y), logo)

    # Combine the base image with the watermark
    watermarked_image = Image.alpha_composite(base_image, watermark)

    # Save the final image
    watermarked_image.convert("RGB").save(output_image_path, "JPEG")

    return output_image_path
