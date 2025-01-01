import os
import random
import numpy as np
import librosa
import sounddevice as sd
import pygame
import time
import threading

# Configuration
AUDIO_INPUT_PATH = r"C:\Users\andre\Downloads\construction-revisionist-official-audio-1080-publer.io.mp3"
TRANS_IMAGES_DIR = r"C:\Users\andre\Desktop\x-anylabeling-matting\coatesBig"  # Directory with transparent insect images
MAX_IMAGES = 500  # Max number of images to load
hop_length = 512
BEAT_INTERVAL = 16  # Change insect images every 16th beat
IMAGE_SCALE = 1  # Scale images to 60% of their original size
WIDTH, HEIGHT = 1920, 800


# Load the audio file
y, sr = librosa.load(AUDIO_INPUT_PATH)

# Compute spectrogram
S_full, phase = librosa.magphase(librosa.stft(y))

# Filter frames using cosine similarity and aggregate by median
S_filter = librosa.decompose.nn_filter(S_full,
                                       aggregate=np.median,
                                       metric='cosine',
                                       width=int(librosa.time_to_frames(2, sr=sr)))
S_filter = np.minimum(S_full, S_filter)

# Use soft masks to separate vocals and background
margin_i, margin_v = 2, 10
power = 2
mask_i = librosa.util.softmask(S_filter, margin_i * (S_full - S_filter), power=power)
mask_v = librosa.util.softmask(S_full - S_filter, margin_v * S_filter, power=power)

# Separate the components
S_foreground = mask_v * S_full  # Vocals
S_background = mask_i * S_full  # Instrumental

# Convert spectrogram back to time domain
vocals = librosa.istft(S_foreground * phase)
non_vocal = librosa.istft(S_background * phase)

# Separate harmonic and percussive signals from the background audio
y_harmonic, y_percussive = librosa.effects.hpss(non_vocal)

# Calculate the chromagram
chromagram = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr, hop_length=hop_length)
chromagram = chromagram.T  # Shape: (T, 12)
chromagram = chromagram / np.max(chromagram)  # Normalize chromagram

# Calculate RMS (intensity) of vocals
frame_length = 2048
hop_length_rms = 512
rms_vocals = librosa.feature.rms(y=vocals, frame_length=frame_length, hop_length=hop_length_rms).flatten()
vocal_times = librosa.frames_to_time(np.arange(len(rms_vocals)), sr=sr, hop_length=hop_length_rms)

# Calculate spectral flatness of non-vocal harmonic audio
spectral_flatness = librosa.feature.spectral_flatness(y=y_harmonic).flatten()
spectral_flatness_times = librosa.frames_to_time(np.arange(len(spectral_flatness)), sr=sr, hop_length=hop_length)

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
        scaled_size = (int(image.get_width() * scale), int(image.get_height() * scale))
        image = pygame.transform.smoothscale(image, scaled_size)
        images.append(image)
    return images

# Initialize Pygame
pygame.init()
# Initialize font for debugging text
font = pygame.font.SysFont('Arial', 24)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dynamic Chromagram Visualization with Insects")
clock = pygame.time.Clock()

# Load insect images
insect_images = load_images_from_directory(TRANS_IMAGES_DIR, MAX_IMAGES, IMAGE_SCALE)

# Play audio in a separate thread
def play_audio(audio, sr):
    sd.play(audio, sr)
    sd.wait()

audio_thread = threading.Thread(target=play_audio, args=(y, sr))
audio_thread.start()

# Visualization variables
start_time = time.time()
running = True
current_images = random.sample(insect_images, 12)  # Start with 12 random images
current_positions = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(12)]
beat_counter = 0

while running:
    # Clear screen with dynamic background color based on vocal intensity
    elapsed_time = time.time() - start_time
    current_vocal_idx = np.searchsorted(vocal_times, elapsed_time) - 1
    if 0 <= current_vocal_idx < len(rms_vocals):
        vocal_intensity = rms_vocals[current_vocal_idx]
        red_intensity = int(min(255, vocal_intensity * 255 / np.max(rms_vocals)))
    else:
        red_intensity = 0
    screen.fill((red_intensity, 0, 0))

    # Get current time in seconds relative to the start of the song
    frame_idx = int((elapsed_time * sr) // hop_length)

    if frame_idx >= len(chromagram):
        break  # Stop if audio has finished playing

    # Get current chroma intensities
    current_chroma = chromagram[frame_idx]


    # Check if we're at a beat
    for beat_time in beat_times:
        if abs(elapsed_time - beat_time) < 0.05:  # Close to a beat time
            beat_counter += 1
            if beat_counter % BEAT_INTERVAL == 0:
                # Refresh images and positions
                current_images = random.sample(insect_images, 12)
                current_positions = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(12)]
            break
    # Add jitter to image positions based on spectral flatness
    current_spectral_idx = np.searchsorted(spectral_flatness_times, elapsed_time) - 1
    if 0 <= current_spectral_idx < len(spectral_flatness):
        flatness_value = spectral_flatness[current_spectral_idx]*1000
        jitter_amount = int(flatness_value * 20)  # Adjust multiplier for desired jitter intensity
    else:
        flatness_value = 0
        jitter_amount = 0

    # Display debugging text for spectral flatness
    flatness_text = font.render(f"Spectral Flatness: {flatness_value:.3f}", True, (255, 255, 255))
    screen.blit(flatness_text, (10, 10))

    # Draw current images with jittered positions
    for i in range(12):
        image = current_images[i]
        intensity = current_chroma[i]
        alpha_image = image.copy()
        alpha_image.fill((255, 255, 255, int(255 * intensity)), special_flags=pygame.BLEND_RGBA_MULT)

        # Add jitter to position
        pos = current_positions[i]
        jittered_pos = (
            pos[0] + random.randint(-jitter_amount, jitter_amount),
            pos[1] + random.randint(-jitter_amount, jitter_amount),
        )
        rect = alpha_image.get_rect(center=jittered_pos)

        # Blit the image onto the screen
        screen.blit(alpha_image, rect.topleft)


    # Update the display
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 FPS

    # Check for quit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()
