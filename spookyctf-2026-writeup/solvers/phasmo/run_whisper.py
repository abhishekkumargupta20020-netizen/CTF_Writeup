import os, wave
import numpy as np
from scipy.signal import resample_poly
from faster_whisper import WhisperModel

MODEL = "/home/hatch/workspace/whisper-models/base"
print(f"loading model {MODEL} ...", flush=True)
model = WhisperModel(MODEL, device="cpu", compute_type="int8")
print("model loaded", flush=True)

def load_audio_16k(path):
    with wave.open(path, 'rb') as w:
        n, sr, ch, sw = w.getnframes(), w.getframerate(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(n)
    assert sw == 2, f"unexpected sampwidth {sw} in {path}"
    a = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    if ch == 2:
        a = a.reshape(-1, 2).mean(axis=1)
    if sr != 16000:
        from math import gcd
        g = gcd(16000, sr)
        a = resample_poly(a, 16000 // g, sr // g).astype(np.float32)
    return a

FILES = [
    "/home/hatch/workspace/user/files/PhasmophobiaChallenge__1.wav",
    "/home/hatch/workspace/phasmo/reversed.wav",
    "/home/hatch/workspace/phasmo/slowed.wav",
    "/home/hatch/workspace/phasmo/mono16k.wav",
    "/home/hatch/workspace/phasmo/reversed16k.wav",
    "/home/hatch/workspace/phasmo/v_bp.wav",
    "/home/hatch/workspace/phasmo/v_gaps.wav",
    "/home/hatch/workspace/phasmo/v_hp2k.wav",
    "/home/hatch/workspace/phasmo/v_mid.wav",
    "/home/hatch/workspace/phasmo/v_rev.wav",
    "/home/hatch/workspace/phasmo/v_side.wav",
    "/home/hatch/workspace/phasmo/v_slow05_44100.wav",
    "/home/hatch/workspace/phasmo/hb_all.wav",
    "/home/hatch/workspace/phasmo/hb_burst1.wav",
    "/home/hatch/workspace/phasmo/hb_burst2.wav",
    "/home/hatch/workspace/phasmo/hb_burst3.wav",
    "/home/hatch/workspace/phasmo/hb_burst4.wav",
    "/home/hatch/workspace/phasmo/w_tail_amp.wav",
    "/home/hatch/workspace/phasmo/w_hp1500.wav",
    "/home/hatch/workspace/phasmo/w_hpss_resid.wav",
]

out = open("/home/hatch/workspace/phasmo/whisper_results.txt", "w")
def log(s):
    print(s, flush=True)
    out.write(s + "\n"); out.flush()

for f in FILES:
    name = os.path.basename(f)
    log(f"\n===== {name} =====")
    if not os.path.exists(f):
        log("FILE MISSING"); continue
    try:
        audio = load_audio_16k(f)
        log(f"audio: {len(audio)/16000:.2f}s @16k mono, peak={np.abs(audio).max():.4f}")
        segments, info = model.transcribe(audio, language="en", beam_size=5,
                                          vad_filter=False, word_timestamps=False)
        log(f"detected_language={info.language} prob={info.language_probability:.2f} duration={info.duration:.1f}s")
        segs = list(segments)
        if not segs:
            log("NO SEGMENTS -> no speech detected")
        for s in segs:
            log(f"[{s.start:6.2f}-{s.end:6.2f}] nosp={s.no_speech_prob:.2f} logp={s.avg_logprob:.2f} text={s.text!r}")
        full = "".join(s.text for s in segs).strip()
        log(f"FULL TEXT: {full!r}" if full else "FULL TEXT: <empty> -> no speech detected")
    except Exception as e:
        import traceback; traceback.print_exc()
        log(f"ERROR: {type(e).__name__}: {e}")
out.close()
print("DONE", flush=True)
