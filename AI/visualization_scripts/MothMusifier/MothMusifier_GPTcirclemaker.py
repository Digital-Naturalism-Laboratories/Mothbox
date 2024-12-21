import numpy as np
import librosa
import sounddevice as sd
import pygame
import random
import time
from threading import Thread

# Load the audio file and extract features
AUDIO_INPUT_PATH = r"C:\Users\andre\Documents\GitHub\06 - I Think It Is Beautiful That You Are 256 Colors Too.mp3"
#y, sr = librosa.load(AUDIO_INPUT_PATH)
y, sr = librosa.load(librosa.ex('nutcracker'))
hop_length = 512

# Separate harmonics and percussive signals
y_harmonic, y_percussive = librosa.effects.hpss(y)

# Beat tracking
tempo, beat_frames = librosa.beat.beat_track(y=y_percussive, sr=sr)
beat_times = librosa.frames_to_time(beat_frames, sr=sr)

# Beat-synchronous features
mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=hop_length, n_mfcc=13)
mfcc_delta = librosa.feature.delta(mfcc)
beat_mfcc_delta = librosa.util.sync(np.vstack([mfcc, mfcc_delta]), beat_frames)
chromagram = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr)
beat_chroma = librosa.util.sync(chromagram, beat_frames, aggregate=np.median)

# Prepare audio playback
def play_audio():
    sd.play(y, samplerate=sr)

# Helper to map chroma features to RGB colors
def chroma_to_color(chroma):
    chroma = chroma / np.max(chroma)  # Normalize chroma to [0, 1]
    r = int(chroma[0] * 255)  # Map to red
    g = int(chroma[5] * 255)  # Map to green
    b = int(chroma[10] * 255)  # Map to blue
    return (r, g, b)

# Visualization function
def visualize():
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Beat Features Visualization")

    clock = pygame.time.Clock()
    running = True

    current_beat = 0
    start_time = time.time()
    circles = []  # Store all circles as (position, radius, color)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get elapsed time since start
        elapsed_time = time.time() - start_time

        # Trigger events based on beat_times
        if current_beat < len(beat_times) and elapsed_time >= beat_times[current_beat]:
            chroma = beat_chroma[:, current_beat]
            color = chroma_to_color(chroma)
            feature = beat_mfcc_delta[:, current_beat]
            intensity = np.mean(feature) * 100  # Scale intensity
            radius = int(20 + intensity)
            position = (random.randint(0, 800), random.randint(0, 600))
            circles.append((position, radius, color))
            current_beat += 1

        # Draw all circles
        screen.fill((0, 0, 0))  # Clear screen
        for pos, rad, col in circles:
            pygame.draw.circle(screen, col, pos, rad)

        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()

# Run audio playback and visualization in parallel
audio_thread = Thread(target=play_audio)
audio_thread.start()

visualize()
