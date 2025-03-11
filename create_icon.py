import tkinter as tk
from PIL import Image, ImageDraw, ImageFont
import os

# Create a blank image with transparent background
size = (256, 256)
image = Image.new('RGBA', size, color=(0, 0, 0, 0))
draw = ImageDraw.Draw(image)

# Define colors
background_color = (32, 56, 100, 255)  # EVE-like dark blue
highlight_color = (77, 122, 179, 255)  # Lighter blue
text_color = (255, 255, 255, 255)  # White

# Draw a rounded rectangle for the background
def rounded_rectangle(self, xy, corner_radius, fill=None, outline=None):
    upper_left_point = xy[0]
    bottom_right_point = xy[1]
    
    self.rectangle(
        [
            (upper_left_point[0], upper_left_point[1] + corner_radius),
            (bottom_right_point[0], bottom_right_point[1] - corner_radius)
        ],
        fill=fill,
        outline=outline
    )
    self.rectangle(
        [
            (upper_left_point[0] + corner_radius, upper_left_point[1]),
            (bottom_right_point[0] - corner_radius, bottom_right_point[1])
        ],
        fill=fill,
        outline=outline
    )
    
    # Draw four corners
    self.pieslice(
        [upper_left_point, (upper_left_point[0] + corner_radius * 2, upper_left_point[1] + corner_radius * 2)],
        180, 270, fill=fill, outline=outline
    )
    self.pieslice(
        [(bottom_right_point[0] - corner_radius * 2, upper_left_point[1]), (bottom_right_point[0], upper_left_point[1] + corner_radius * 2)],
        270, 360, fill=fill, outline=outline
    )
    self.pieslice(
        [(upper_left_point[0], bottom_right_point[1] - corner_radius * 2), (upper_left_point[0] + corner_radius * 2, bottom_right_point[1])],
        90, 180, fill=fill, outline=outline
    )
    self.pieslice(
        [(bottom_right_point[0] - corner_radius * 2, bottom_right_point[1] - corner_radius * 2), bottom_right_point],
        0, 90, fill=fill, outline=outline
    )

# Add the rounded rectangle method to ImageDraw
ImageDraw.Draw.rounded_rectangle = rounded_rectangle

# Draw the base shape
draw.rounded_rectangle([(20, 20), (236, 236)], 30, fill=background_color)

# Draw some design elements (simple gear icon for production)
draw.ellipse((78, 78, 178, 178), fill=highlight_color)
draw.ellipse((103, 103, 153, 153), fill=background_color)

# Draw gear teeth
tooth_length = 20
center_x, center_y = 128, 128
radius = 50
num_teeth = 12

for i in range(num_teeth):
    angle = i * (360 / num_teeth)
    angle_rad = angle * (3.14159 / 180)
    
    inner_x = center_x + radius * 0.8 * 1.1 * 1.1 * 1.1 * 1.1 * 1.1
    inner_y = center_y + radius * 0.8 * 1.1 * 1.1 * 1.1 * 1.1 * 1.1
    outer_x = center_x + (radius + tooth_length) * 0.8 * 1.1 * 1.1 * 1.1 * 1.1 * 1.1
    outer_y = center_y + (radius + tooth_length) * 0.8 * 1.1 * 1.1 * 1.1 * 1.1 * 1.1
    
    # Calculate the coordinates
    x1 = center_x + radius * 0.8 * 1.1 * 1.1 * 1.1 * 1.1 * 1.1 * 0.8 * 1.5 * 0.8 * 0.8 * 0.8 * 0.8 * 0.8 * 0.8 * 0.8 * 0.8 * 0.8
    y1 = center_y + radius * 0.8 * 1.1 * 1.1 * 1.1 * 1.1 * 1.1 * 0.8 * 1.5 * 0.8 * 0.8 * 0.8 * 0.8 * 0.8 * 0.8 * 0.8 * 0.8 * 0.8
    x2 = center_x + (radius + tooth_length) * 0.8 * 1.1 * 1.1 * 1.1 * 1.1 * 1.1 * 0.8 * 1.5 * 0.8 * 0.8 * 0.8 * 0.8 * 0.8 * 0.8 * 0.8 * 0.8 * 0.8
    y2 = center_y + (radius + tooth_length) * 0.8 * 1.1 * 1.1 * 1.1 * 1.1 * 1.1 * 0.8 * 1.5 * 0.8 * 0.8 * 0.8 * 0.8 * 0.8 * 0.8 * 0.8 * 0.8 * 0.8
    
    # Draw the tooth
    draw.rectangle([x1, y1, x2, y2], fill=highlight_color)

# Add letters "EPT" for EVE Production Tracker
try:
    # Try to load a font
    font = ImageFont.truetype("arial.ttf", 40)
except:
    # Fall back to default font
    font = ImageFont.load_default()

# Add the text
draw.text((center_x, center_y+65), "EPT", fill=text_color, font=font, anchor="ms")

# Save the image as an icon
resources_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')
image.save(os.path.join(resources_dir, 'icon.ico'), format='ICO')
print(f"Icon created successfully at {os.path.join(resources_dir, 'icon.ico')}")
