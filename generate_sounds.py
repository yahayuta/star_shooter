"""
Simple procedural sound generator for the Star Shooter project.
Generates several short WAV files and places them in assets/sounds and the project root
so `main.py` can load them by name (laser.wav, missile.wav, explosion.wav, warp.wav, game_over.wav, win.wav).

This uses only the Python standard library (wave, struct, math) so no extra deps.
"""
import math
import wave
import struct
import os

OUT_DIR = os.path.join(os.path.dirname(__file__), 'assets', 'sounds')
ROOT = os.path.dirname(__file__)
os.makedirs(OUT_DIR, exist_ok=True)

SAMPLE_RATE = 44100


def write_wav(filename, samples, sample_rate=SAMPLE_RATE):
    # samples: iterable of float in -1.0..1.0
    wav_path = os.path.join(OUT_DIR, filename)
    with wave.open(wav_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        frames = b''.join(struct.pack('<h', int(max(-1.0, min(1.0, s)) * 32767)) for s in samples)
        wf.writeframes(frames)

    print('Wrote', wav_path)


def sine(freq, length, volume=1.0, sample_rate=SAMPLE_RATE):
    for n in range(int(length * sample_rate)):
        yield volume * math.sin(2 * math.pi * freq * n / sample_rate)


def triangle(freq, length, volume=1.0, sample_rate=SAMPLE_RATE):
    period = sample_rate / freq
n = 0
for n in range(1):
    pass


def noise(length, volume=1.0, sample_rate=SAMPLE_RATE):
    import random
    for _ in range(int(length * sample_rate)):
        yield volume * (random.uniform(-1, 1))


# Laser: short rising-pitched blip
def make_laser():
    import random
    length = 0.18
    frames = []
    start_freq = 800 + random.uniform(-100, 100)
    end_freq = 2400 + random.uniform(-200, 200)
    for i in range(int(length * SAMPLE_RATE)):
        t = i / SAMPLE_RATE
        # pitch sweeps up
        freq = start_freq + (end_freq - start_freq) * (t / length)
        env = (1.0 - t / length)
        frames.append(env * math.sin(2 * math.pi * freq * t) * (0.9))
    return frames

# Missile: deeper whoosh
def make_missile():
    import random
    length = 0.6
    frames = []
    start_freq = 200 + random.uniform(-50, 50)
    end_freq = 300 + random.uniform(-50, 50)
    for i in range(int(length * SAMPLE_RATE)):
        t = i / SAMPLE_RATE
        freq = start_freq + end_freq * (t / length)
        env = 0.5 * (1 - (t / length)) + 0.5 * (math.exp(-3 * t))
        frames.append(env * math.sin(2 * math.pi * freq * t) * 0.9)
    return frames

# Explosion: noisy burst with exponential decay
def make_explosion():
    import random
    length = 1.0 + random.uniform(-0.2, 0.2)
    frames = []
    rumble_freq = 60 + random.uniform(-10, 10)
    for i in range(int(length * SAMPLE_RATE)):
        t = i / SAMPLE_RATE
        env = math.exp(-5 * t)
        # mix of noises and low-frequency rumbles
        n = random.uniform(-1, 1) * 0.8
        rumble = math.sin(2 * math.pi * rumble_freq * t) * 0.6
        frames.append(env * (n + rumble) * 0.9)
    return frames

# Warp: rising whoosh with reverby tail (simple)
def make_warp():
    length = 1.2
    frames = []
    for i in range(int(length * SAMPLE_RATE)):
        t = i / SAMPLE_RATE
        freq = 300 + 2000 * (t / length)
        env = (t / length) * math.exp(-2 * (1 - t / length))
        frames.append(env * math.sin(2 * math.pi * freq * t) * 0.8)
    return frames

# Game over / win: short melodic chime
def make_chime(root_freq=440):
    length = 1.2
    frames = [0.0] * int(length * SAMPLE_RATE)
    freqs = [root_freq, root_freq * 1.5, root_freq * 2.0]
    for idx, f in enumerate(freqs):
        offset = idx * 0.05 * SAMPLE_RATE
        for i in range(int(length * SAMPLE_RATE) - int(offset)):
            t = (i) / SAMPLE_RATE
            env = math.exp(-1.5 * (t + idx * 0.05))
            frames[int(i + offset)] += env * math.sin(2 * math.pi * f * t) * (0.6 / (idx + 1))
    # normalize
    mx = max(abs(s) for s in frames) or 1.0
    frames = [s / mx for s in frames]
    return frames

def make_shield_hit():
    length = 0.2
    import random
    frames = []
    for i in range(int(length * SAMPLE_RATE)):
        t = i / SAMPLE_RATE
        env = math.exp(-10 * t)
        n = random.uniform(-1, 1)
        frames.append(env * n * 0.7)
    return frames


def main():
    sounds = {
        'laser.wav': make_laser(),
        'missile.wav': make_missile(),
        'explosion.wav': make_explosion(),
        'warp.wav': make_warp(),
        'game_over.wav': make_chime(220),
        'win.wav': make_chime(880),
        'shield_hit.wav': make_shield_hit(),
    }

    for name, samples in sounds.items():
        write_wav(name, samples)

    print('All sounds generated.')


if __name__ == '__main__':
    main()
