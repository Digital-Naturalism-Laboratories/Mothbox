import numpy as np
import librosa
import sounddevice as sd
import pygame
import time
import threading
import random  # Add this for generating random colors

# Load the audio file
AUDIO_INPUT_PATH = r"C:\Users\andre\Documents\GitHub\06 - I Think It Is Beautiful That You Are 256 Colors Too.wav"
y, sr = librosa.load(AUDIO_INPUT_PATH)
hop_length = 512

# Separate percussive and harmonic signals
y_harmonic, y_percussive = librosa.effects.hpss(y)

# Calculate the chromagram
chromagram = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr, hop_length=hop_length)
chromagram = chromagram.T  # Shape: (T, 12)

# Normalize chromagram
chromagram = chromagram / np.max(chromagram)

# Beat tracking
tempo, beat_frames = librosa.beat.beat_track(y=y_percussive, sr=sr, hop_length=hop_length)
beat_times = librosa.frames_to_time(beat_frames, sr=sr)  # Convert beats to times

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dynamic Chromagram Visualization")
clock = pygame.time.Clock()

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
background_color = (0, 0, 0)  # Initial background color

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

    # Check if we're at a beat
    for beat_time in beat_times:
        if abs(elapsed_time - beat_time) < 0.05:  # If close to a beat time
            # Change the background color randomly
            background_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            break

    # Draw circles
    for i, (x, y) in enumerate(circle_positions):
        intensity = current_chroma[i]  # Intensity of this pitch class
        radius = int(50 + 100 * intensity)  # Scale radius based on intensity
        color = (int(255 * intensity), 50, 255 - int(255 * intensity))  # Dynamic color
        pygame.draw.circle(screen, color, (x, y), radius)

    # Update display
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 FPS

    # Check for quit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()
