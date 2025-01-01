import os
import random
import cv2
import numpy as np
import pygame

# Global variables
TRANS_IMAGES_DIR = r"C:\Users\andre\Desktop\x-anylabeling-matting\onlybig"  # Directory with transparent insect images
MAX_IMAGES = 12  # Maximum number of images to load
WIDTH, HEIGHT = 1920, 1080
DISPLAY_SIZE = (WIDTH, HEIGHT)  # Size of the Pygame window
SCALE = 0.5  # Scale factor for images
OUTLINE_GROWTH_RATE = 1  # Initial growth rate for outlines

# Load up to MAX_IMAGES from the specified directory
def load_images_from_directory(directory, max_images, scale):
    image_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.png')]
    selected_files = random.sample(image_files, min(len(image_files), max_images))
    images = []
    for file in selected_files:
        image = pygame.image.load(file).convert_alpha()
        # Scale image
        scaled_size = (int(image.get_width() * scale), int(image.get_height() * scale))
        image = pygame.transform.smoothscale(image, scaled_size)
        images.append(image)
    return images


def create_growing_outline(image, outline_color, growth_rate):
    """Create a growing outline effect using dilation."""
    # Convert Pygame surface to a numpy array (RGBA)
    image_array = pygame.surfarray.pixels_alpha(image).copy()
    # Create a binary mask from the alpha channel
    _, binary_mask = cv2.threshold(image_array, 1, 255, cv2.THRESH_BINARY)
    # Dilate the binary mask
    dilated_mask = cv2.dilate(binary_mask, None, iterations=growth_rate)
    # Create a colored outline from the dilated mask
    outline = np.zeros((*dilated_mask.shape, 3), dtype=np.uint8)
    for i in range(3):  # Apply the outline color to all channels
        outline[:, :, i] = dilated_mask * outline_color[i] // 255
    return outline

def random_pastel_color():
    """Generate a random pastel color."""
    return tuple(random.randint(128, 255) for _ in range(3))

def overlay_images(background, image, position):
    """Overlay an image with transparency onto a background."""
    x, y = position
    h, w, _ = image.shape
    if y + h > background.shape[0] or x + w > background.shape[1]:
        return  # Skip if the image exceeds the bounds of the background
    alpha = image[:, :, 0] / 255.0  # Use the red channel for alpha
    for c in range(3):  # Blend each color channel
        background[y:y+h, x:x+w, c] = (
            alpha * image[:, :, c] + (1 - alpha) * background[y:y+h, x:x+w, c]
        )

# Main script
pygame.init()
screen = pygame.display.set_mode(DISPLAY_SIZE)
pygame.display.set_caption("Growing Outline Visualization")
clock = pygame.time.Clock()

# Load images
images = load_images_from_directory(TRANS_IMAGES_DIR, MAX_IMAGES, SCALE)


# Generate initial random positions for the insects and background images
def generate_random_positions(num_positions):
    positions = []
    for _ in range(num_positions):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        positions.append((x, y))
    return positions

# Initialize random positions
num_insects = 12  # Number of insects to display
positions = generate_random_positions(num_insects)


# Pastel colors for outlines
outline_colors = [random_pastel_color() for _ in images]

# Main loop
running = True
frame_count = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Create the background
    background = np.ones((DISPLAY_SIZE[1], DISPLAY_SIZE[0], 3), dtype=np.uint8)

    # Draw images and their outlines
    for img, pos, color in zip(images, positions, outline_colors):
        outline = create_growing_outline(img, color, OUTLINE_GROWTH_RATE)
        h, w, _ = outline.shape
        x, y = pos
        # Ensure position stays within screen bounds
        if x + w > DISPLAY_SIZE[0] or y + h > DISPLAY_SIZE[1]:
            continue
        overlay_images(background, outline, pos)
        overlay_images(background, pygame.surfarray.array3d(img), pos)

    # Convert the background to a Pygame surface and display it
    surface = pygame.surfarray.make_surface(cv2.cvtColor(outline, cv2.COLOR_BGR2RGB))
    screen.blit(surface, (0, 0))
    pygame.display.flip()

    # Increment the frame count and update the growth rate
    frame_count += 1
    if frame_count % 30 == 0:  # Increment the growth rate every second
        OUTLINE_GROWTH_RATE += 1

    clock.tick(30)

pygame.quit()
