import wave, numpy as np
from scipy.signal import butter, sosfiltfilt, stft, istft
from scipy.ndimage import median_filter

SRC = "/home/hatch/workspace/user/files/PhasmophobiaChallenge__1.wav"
OUT = "/home/hatch/workspace/phasmo/"

def read_wav(path):
    with wave.open(path, 'rb') as w:
        n, sr, ch, sw = w.getnframes(), w.getframerate(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(n)
    assert sw == 2
    a = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    if ch == 2:
        a = a.reshape(-1, 2)
    return a, sr

def write_wav(path, mono, sr=16000):
    mono = np.clip(mono, -1.0, 1.0)
    pcm = (mono * 32767).astype(np.int16)
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(pcm.tobytes())

def resample_16k(x, sr):
    # simple polyphase-ish resample via np.interp on index grid (fine for this purpose)
    if sr == 16000:
        return x
    n_out = int(round(len(x) * 16000 / sr))
    idx = np.linspace(0, len(x) - 1, n_out)
    return np.interp(idx, np.arange(len(x)), x).astype(np.float32)

a, sr = read_wav(SRC)
print("src shape", a.shape, "sr", sr, "dur", len(a)/sr)
mono = a.mean(axis=1) if a.ndim == 2 else a
print("mono peak", np.abs(mono).max(), "rms", np.sqrt((mono**2).mean()))

# (a) tail 17.0-18.94s amplified to near full scale
tail = mono[int(17.0*sr):]
print("tail samples", len(tail), "peak before", np.abs(tail).max())
tail_amp = tail / (np.abs(tail).max() + 1e-12) * 0.99
write_wav(OUT + "w_tail_amp.wav", resample_16k(tail_amp, sr))
print("wrote w_tail_amp.wav peak", np.abs(tail_amp).max())

# (b) high-pass >1500 Hz full audio
sos = butter(4, 1500, btype='highpass', fs=sr, output='sos')
hp = sosfiltfilt(sos, mono)
print("hp peak", np.abs(hp).max())
hp_n = hp / (np.abs(hp).max() + 1e-12) * 0.9
write_wav(OUT + "w_hp1500.wav", resample_16k(hp_n, sr))
print("wrote w_hp1500.wav")

# (c) HPSS-style residual: STFT median-filter separation, keep percussive/non-harmonic part
f, t, Z = stft(mono, fs=sr, nperseg=2048, noverlap=1536)
mag = np.abs(Z)
harm_mag = median_filter(mag, size=(1, 31))   # median along time -> harmonic
perc_mag = median_filter(mag, size=(31, 1))   # median along freq -> percussive
eps = 1e-10
mask_p = (perc_mag**2) / (harm_mag**2 + perc_mag**2 + eps)
Zp = Z * mask_p
_, resid = istft(Zp, fs=sr, nperseg=2048, noverlap=1536)
resid = resid[:len(mono)]
print("hpss resid peak", np.abs(resid).max(), "rms", np.sqrt((resid**2).mean()))
resid_n = resid / (np.abs(resid).max() + 1e-12) * 0.9
write_wav(OUT + "w_hpss_resid.wav", resample_16k(resid_n, sr))
print("wrote w_hpss_resid.wav")
