from PIL import Image, ImageDraw, ImageFont

from UDDF_telemetry import ParameterReader

# Define the initiql size of the image
width, height = 200, 100

# Create a new image with RGBA mode (A stands for alpha, which controls transparency)
image = Image.new("RGBA", (width, height), (255, 255, 255, 0))

# Initialize the drawing context
draw = ImageDraw.Draw(image)

# Define the text and font
text = "Hello, World!"
font = ImageFont.load_default()

# Calculate the width and height of the text to be drawn
text_width, text_height = 100, 100

# Calculate X, Y position of the text
x = (width - text_width) / 2
y = (height - text_height) / 2

# Draw the text on the image
draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))

# Save the image
image.save("text_image.png") """



def TextDrawer():


def main():
    
    Parameters=ParameterReader()


if __name__ == "__main__":
    main()
