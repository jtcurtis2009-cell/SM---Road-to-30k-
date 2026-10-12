"""Generate an original, royalty free backing beat for a Reel (no licensing issues).

Usage:
    python3 scripts/make_beat.py <out.wav> [--bpm 86] [--seconds 20] [--mood dark|bright]

Dark: half time trap feel, deep 808, minor key pad, crisp hats. Good for training and discipline.
Bright: upbeat four on the floor, major pad. Good for joy and travel.
Put the output in raw/music/ and point reel.json "music.file" at it.
"""
import argparse
import wave

import numpy as np

SR = 44100


def env(n, attack=0.002, decay=0.2):
    t = np.arange(n) / SR
    a = np.clip(t / attack, 0, 1)
    return a * np.exp(-t / decay)


def kick(len_s=0.5):
    n = int(len_s * SR); t = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.22) * 1.0


def eight08(freq, len_s):
    n = int(len_s * SR); t = np.arange(n) / SR
    f = freq * (1 + 0.6 * np.exp(-t * 40))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR)
    return np.tanh(s * 1.8) * env(n, 0.003, len_s * 0.55) * 0.55


def snare(len_s=0.3):
    n = int(len_s * SR); t = np.arange(n) / SR
    noise = np.random.randn(n)
    noise = noise - np.convolve(noise, np.ones(8) / 8, "same")  # brighten
    tone = np.sin(2 * np.pi * 190 * t) * env(n, 0.001, 0.05)
    return (noise * env(n, 0.001, 0.09) * 0.45 + tone * 0.35) * 0.9


def hat(len_s=0.06, open_=False):
    n = int((0.25 if open_ else len_s) * SR)
    noise = np.random.randn(n)
    noise = noise - np.convolve(noise, np.ones(4) / 4, "same")
    return noise * env(n, 0.0005, 0.08 if open_ else 0.018) * 0.16


def pad(freqs, len_s, vol=0.08):
    n = int(len_s * SR); t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 2.003 * t) for f in freqs)
    fade = np.minimum(1, np.minimum(t / 0.8, (len_s - t) / 0.8))
    return s / len(freqs) * fade * vol


def place(buf, sound, at):
    i = int(at * SR); j = min(len(buf), i + len(sound))
    if i < len(buf):
        buf[i:j] += sound[: j - i]


def build(bpm, seconds, mood):
    np.random.seed(7)
    beat = 60 / bpm
    buf = np.zeros(int(seconds * SR) + SR)
    bar = beat * 4
    dark = mood == "dark"
    chords = ([[55, 65.4, 82.4], [43.65, 65.4, 87.3], [49, 61.7, 73.4], [41.2, 61.7, 82.4]] if dark
              else [[65.4, 82.4, 98], [73.4, 87.3, 110], [55, 69.3, 82.4], [61.7, 77.8, 98]])
    roots = [55, 43.65, 49, 41.2] if dark else [65.4, 73.4, 55, 61.7]
    nbars = int(seconds / bar) + 1
    for b in range(nbars):
        t0 = b * bar
        ch = chords[b % 4]
        place(buf, pad([f * 2 for f in ch], bar + 0.4, 0.07 if dark else 0.06), t0)
        intro = b == 0
        if dark:
            if not intro:
                for k in (0, 2.5):
                    place(buf, kick(), t0 + k * beat)
                place(buf, eight08(roots[b % 4], beat * 2.2), t0)
                place(buf, eight08(roots[b % 4], beat * 1.2), t0 + 2.5 * beat)
                place(buf, snare(), t0 + 2 * beat)
            steps = 16 if not intro else 8
            for h in range(steps):
                place(buf, hat(open_=(h % 8 == 6)), t0 + h * beat / 4 * (16 / steps))
            if b % 2 == 1 and not intro:  # hat roll fill
                for r in range(6):
                    place(buf, hat(0.03) * 0.8, t0 + 3.5 * beat + r * beat / 12)
        else:
            for k in range(4):
                if not intro:
                    place(buf, kick(0.35), t0 + k * beat)
                place(buf, hat(open_=True) * 0.6, t0 + (k + 0.5) * beat)
            if not intro:
                for k in (1, 3):
                    place(buf, snare(0.2) * 0.8, t0 + k * beat)
                place(buf, eight08(roots[b % 4], beat * 3.5) * 0.7, t0)
    buf = buf[: int(seconds * SR)]
    buf = np.tanh(buf * 1.2)
    return buf / (np.max(np.abs(buf)) + 1e-9) * 0.89


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("--bpm", type=float, default=86)
    ap.add_argument("--seconds", type=float, default=20); ap.add_argument("--mood", default="dark")
    a = ap.parse_args()
    x = build(a.bpm, a.seconds, a.mood)
    stereo = np.stack([x, np.roll(x, 40)], 1)
    with wave.open(a.out, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((stereo * 32767).astype(np.int16).tobytes())
    print(f"Beat: {a.out} ({a.seconds}s, {a.bpm} bpm, {a.mood})")


if __name__ == "__main__":
    main()
