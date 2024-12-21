import os
import random
import numpy as np
import librosa
import sounddevice as sd
import pygame
import time
import threading
import cv2

# Configuration
AUDIO_INPUT_PATH = r"C:\Users\andre\Documents\GitHub\06 - I Think It Is Beautiful That You Are 256 Colors Too.wav"
TRANS_IMAGES_DIR = r"C:\Users\andre\Desktop\x-anylabeling-matting\onlybig"  # Directory with transparent insect images
MAX_IMAGES = 500  # Max number of images to load
hop_length = 512
IMAGE_SCALE = 0.6  # Scale images to 20% of their original size
BACKGROUND_IMAGE_SCALE = 0.1  # Scale background images to 10% of their original size
BEAT_INTERVAL = 16  # Change insect image every 16th beat
BACKGROUND_IMAGES_COUNT = 450  # Max number of background images

# Load the audio file
y, sr = librosa.load(AUDIO_INPUT_PATH)
#y, sr = librosa.load(librosa.example('nutcracker'))

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

# Load 50 random background images
background_images = load_images_from_directory(TRANS_IMAGES_DIR, BACKGROUND_IMAGES_COUNT, BACKGROUND_IMAGE_SCALE)

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
insect_positions = generate_random_positions(num_insects)
background_positions = generate_random_positions(BACKGROUND_IMAGES_COUNT)


# Set up OpenCV VideoWriter to save the video
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Choose codec (XVID)
video_filename = 'output_video.avi'  # Output video file
fps = 30  # Frames per second
video_writer = cv2.VideoWriter(video_filename, fourcc, fps, (WIDTH, HEIGHT))


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
current_insect_images = random.sample(insect_images, num_insects)
current_background_images = random.sample(background_images, BACKGROUND_IMAGES_COUNT)
screen.fill(background_color)
beat_counter = 0  # Count beats to change insect image every 16th beat

def get_complementary_color(color):
    return (255 - color[0], 255 - color[1], 255 - color[2])

# Calculate RMS of the signal
def calculate_rms(signal, frame_length):
    return np.sqrt(np.mean(signal**2))

while running:
    # Clear screen with the current background color
    screen.fill(background_color)

    # Get current time in seconds relative to the start of the song
    elapsed_time = time.time() - start_time
    frame_idx = int((elapsed_time * sr) // hop_length)

    if frame_idx >= len(chromagram):
        break  # Stop if audio has finished playing

    # Get current chroma intensity for this frame
    current_chroma = chromagram[frame_idx]

    # Calculate RMS for the current audio frame
    rms_value = calculate_rms(y[frame_idx * hop_length: (frame_idx + 1) * hop_length], hop_length)

    # Map RMS to the number of background images to display (1 to MAX_IMAGES)
    num_background_images_to_display = int(np.clip(rms_value * BACKGROUND_IMAGES_COUNT * 1, 1, BACKGROUND_IMAGES_COUNT))

    # Check if we're at a beat
    for beat_time in beat_times:
        if abs(elapsed_time - beat_time) < 0.05:  # If close to a beat time
            beat_counter += 1
            if beat_counter % BEAT_INTERVAL == 0:  # Change insect image every 16th beat
                # Pick a random insect to change
                insect_to_change = random.randint(0, num_insects - 1)
                # Change the image of the selected insect and place it at a new random position
                current_insect_images[insect_to_change] = random.choice(insect_images)
                insect_positions[insect_to_change] = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
            if beat_counter % BEAT_INTERVAL/4 == 0:  # Change insect image every 16th beat
                # Change background images
                current_background_images = random.sample(background_images, BACKGROUND_IMAGES_COUNT)
                background_positions = generate_random_positions(BACKGROUND_IMAGES_COUNT)

            # Change the background color randomly
            background_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            break

    # Draw background images
    for i in range(num_background_images_to_display):
        image = current_background_images[i]
        pos = background_positions[i]
        tinted_image = image.copy()
        # Tint the image with a complementary color of the background
        tint_color = get_complementary_color(background_color)
        tinted_image.fill(tint_color, special_flags=pygame.BLEND_RGB_ADD)
        
        # Draw the tinted image at the random position
        rect = tinted_image.get_rect(center=pos)
        screen.blit(tinted_image, rect)

    # Draw insect images at their random positions
    for i in range(num_insects):
        intensity = current_chroma[i]  # Intensity of this pitch class
        scale = 0.1 + intensity*2  # Scale factor (minimum 50% of original size)
        insect_image = current_insect_images[i]
        # Scale the insect image based on intensity
        scaled_image = pygame.transform.smoothscale(insect_image, (int(insect_image.get_width() * scale), 
                                                                   int(insect_image.get_height() * scale)))
        rect = scaled_image.get_rect(center=insect_positions[i])
        screen.blit(scaled_image, rect)

    # Capture the frame and write it to the video file
    frame = pygame.surfarray.array3d(pygame.display.get_surface())
    frame = np.transpose(frame, (1, 0, 2))  # Convert to OpenCV format (BGR)
    video_writer.write(frame)

    # Update display
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 FPS

    # Check for quit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Release the video writer
video_writer.release()

# Quit Pygame
pygame.quit()
