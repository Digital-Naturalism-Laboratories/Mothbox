import os
import random
import numpy as np
import librosa
import sounddevice as sd
import pygame
import time
import threading

# Configuration
AUDIO_INPUT_PATH = r"C:\Users\andre\Documents\GitHub\06 - I Think It Is Beautiful That You Are 256 Colors Too.wav"
TRANS_IMAGES_DIR = r"C:\Users\andre\Desktop\x-anylabeling-matting\onlybig"  # Directory with transparent insect images
MAX_IMAGES = 500  # Max number of images to load
hop_length = 512
IMAGE_SCALE = 0.2  # Scale images to half their original size
BEAT_INTERVAL = 16  # Change insect images every 16th beat

# Load the audio file
y, sr = librosa.load(AUDIO_INPUT_PATH)

# Separate percussive and harmonic signals
y_harmonic, y_percussive = librosa.effects.hpss(y)

# Calculate the chromagram
chromagram = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr, hop_length=hop_length)
chromagram = chromagram.T  # Shape: (T, 12)
chromagram = chromagram / np.max(chromagram)  # Normalize chromagram

# Beat tracking
tempo, beat_frames = librosa.beat.beat_track(y=y_percussive, sr=sr, hop_length=hop_length)
beat_times = librosa.frames_to_time(beat_frames, sr=sr)

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


# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 1920, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Initialize display
pygame.display.set_caption("Dynamic Chromagram Visualization with Insects")
clock = pygame.time.Clock()

# Load insect images
insect_images = load_images_from_directory(TRANS_IMAGES_DIR, MAX_IMAGES, IMAGE_SCALE)

# Circle positions (12 evenly spaced notes in a circle)
circle_radius = 200
center_x, center_y = WIDTH // 2, HEIGHT // 2
angles = np.linspace(0, 2 * np.pi, 12, endpoint=False)
circle_positions = [(int(center_x + circle_radius * np.cos(a)), 
                     int(center_y + circle_radius * np.sin(a))) for a in angles]

# Play audio in a separate thread
def play_audio(audio, sr):
    sd.play(audio, sr)
    sd.wait()

audio_thread = threading.Thread(target=play_audio, args=(y, sr))
audio_thread.start()

# Visualization loop
start_time = time.time()
running = True
background_color = (255, 255, 255)  # Initial background color
current_insect_images = random.sample(insect_images, len(circle_positions))
screen.fill(background_color)
beat_counter = 0  # Count beats to change images every 16th beat

while running:
    # Clear screen with the current background color
    #screen.fill(background_color)

    # Get current time in seconds relative to the start of the song
    elapsed_time = time.time() - start_time
    frame_idx = int((elapsed_time * sr) // hop_length)

    if frame_idx >= len(chromagram):
        break  # Stop if audio has finished playing

    # Get current chroma intensity for this frame
    current_chroma = chromagram[frame_idx]


    # Check if we're at a beat
    for beat_time in beat_times:
        if abs(elapsed_time - beat_time) < 0.05:  # If close to a beat time
            beat_counter += 1
            if beat_counter % BEAT_INTERVAL == 0:  # Change images every 16th beat
                # Change to new random insect images for all positions
                current_insect_images = random.sample(insect_images, len(circle_positions))
                #current_insect_masks = [insect_masks[insect_images.index(img)] for img in current_insect_images]
                # Reset outline growth
                outline_growth = [1] * len(circle_positions)
            # Change the background color randomly
            background_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            break



    # Draw insect images at circle positions
    for i, (x, y) in enumerate(circle_positions):
        intensity = current_chroma[i]  # Intensity of this pitch class
        scale = 0.5 + intensity  # Scale factor (minimum 50% of original size)
        insect_image = current_insect_images[i]
        scaled_image = pygame.transform.smoothscale(insect_image, (int(insect_image.get_width() * scale), 
                                                                   int(insect_image.get_height() * scale)))
        rect = scaled_image.get_rect(center=(x, y))
        screen.blit(scaled_image, rect)

    # Update display
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 FPS

    # Check for quit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()
