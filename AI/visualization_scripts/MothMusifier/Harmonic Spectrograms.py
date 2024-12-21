import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
#from google.colab import files

AUDIO_INPUT_PATH = r"C:\Users\andre\Documents\GitHub\06 - I Think It Is Beautiful That You Are 256 Colors Too.wav"

y, sr = librosa.load(AUDIO_INPUT_PATH)

# Compute the Short-Time Fourier Transform (STFT) with a high number of FFT points for better frequency resolution
D = librosa.stft(y, n_fft=4096)

# Convert the complex-valued STFT to magnitude
S = np.abs(D)

# Convert to dB
S_db = librosa.amplitude_to_db(S, ref=np.max)

# Plot the spectrogram with high frequency resolution
plt.figure(figsize=(12, 6))
librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Spectrogram with High Frequency Resolution')
plt.tight_layout()
plt.show()

# Harmonic-Percussive Source Separation (HPSS)
harmonic, percussive = librosa.effects.hpss(y)

# Compute and plot harmonic spectrogram
D_harmonic = librosa.stft(harmonic, n_fft=4096)
S_harmonic = np.abs(D_harmonic)
S_harmonic_db = librosa.amplitude_to_db(S_harmonic, ref=np.max)

plt.figure(figsize=(12, 6))
librosa.display.specshow(S_harmonic_db, sr=sr, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Harmonic Spectrogram')
plt.tight_layout()
plt.show()

# Compute and plot percussive spectrogram
D_percussive = librosa.stft(percussive, n_fft=4096)
S_percussive = np.abs(D_percussive)
S_percussive_db = librosa.amplitude_to_db(S_percussive, ref=np.max)

plt.figure(figsize=(12, 6))
librosa.display.specshow(S_percussive_db, sr=sr, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Percussive Spectrogram')
plt.tight_layout()
plt.show()

# Compute and plot chromagram
chromagram = librosa.feature.chroma_stft(y=y, sr=sr, n_fft=4096,n_chroma=24)

plt.figure(figsize=(12, 6))
librosa.display.specshow(chromagram, sr=sr, x_axis='time', y_axis='chroma')
plt.colorbar()
plt.title('Chromagram')
plt.tight_layout()
plt.show()