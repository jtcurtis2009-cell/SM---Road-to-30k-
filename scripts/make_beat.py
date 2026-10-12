"""Generate an original, royalty free backing beat for a Reel (no licensing issues).

Usage:
    python3 scripts/make_beat.py <out.wav> [--bpm 86] [--seconds 20] [--mood dark|bright|boombap]

Dark: half time trap feel, deep 808, minor key pad, crisp hats. Good for training and discipline.
Bright: upbeat four on the floor, major pad. Good for joy and travel.
Boombap: 90s and early 2000s rap style, swung drums, Rhodes chords, vinyl crackle. Try 92 to 98 bpm.
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


def rhodes(freqs, len_s, vol=0.12):
    """Electric piano style chord: bell like harmonics, soft decay, gentle tremolo."""
    n = int(len_s * SR); t = np.arange(n) / SR
    s = np.zeros(n)
    for f in freqs:
        s += (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 6)
              + 0.12 * np.sin(2 * np.pi * f * 3.01 * t) * np.exp(-t * 9))
    trem = 1 + 0.12 * np.sin(2 * np.pi * 4.5 * t)
    return s / len(freqs) * env(n, 0.004, len_s * 0.6) * trem * vol


def bb_kick():
    n = int(0.45 * SR); t = np.arange(n) / SR
    f = 50 + 140 * np.exp(-t * 35)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.18)
    click = np.random.randn(n) * env(n, 0.0003, 0.004) * 0.4
    return np.tanh((body + click) * 2.2) * 0.95


def bb_snare():
    n = int(0.32 * SR); t = np.arange(n) / SR
    noise = np.random.randn(n)
    noise = noise - np.convolve(noise, np.ones(6) / 6, "same")
    body = np.sin(2 * np.pi * 185 * t) * env(n, 0.001, 0.06)
    return np.tanh((noise * env(n, 0.001, 0.12) * 0.7 + body * 0.6) * 1.8) * 0.75


def crackle(seconds):
    n = int(seconds * SR)
    hiss = np.convolve(np.random.randn(n), np.ones(30) / 30, "same") * 0.012
    pops = (np.random.rand(n) > 0.99965) * np.random.randn(n) * 0.25
    return hiss + np.convolve(pops, np.exp(-np.arange(60) / 8), "same")


def build_boombap(bpm, seconds):
    """90s / early 2000s boom bap: swung drums, dusty Rhodes chords, round bass, vinyl crackle."""
    np.random.seed(11)
    beat = 60 / bpm; step = beat / 4; bar = beat * 4; swing = step * 0.16
    buf = np.zeros(int(seconds * SR) + SR)
    # Am9, Dm9, Fmaj7, E7#9  (classic minor boom bap loop)
    chords = [[220, 261.6, 329.6, 392, 493.9], [146.8, 174.6, 220, 261.6, 329.6],
              [174.6, 220, 261.6, 329.6], [164.8, 207.7, 293.7, 392]]
    roots = [55, 73.4, 43.65, 41.2]
    kick_steps = [0, 7, 10]; snare_steps = [4, 12]
    for b in range(int(seconds / bar) + 1):
        t0 = b * bar
        ch = chords[b % 4]
        place(buf, rhodes(ch, beat * 1.6), t0)
        place(buf, rhodes(ch, beat * 1.2, 0.08), t0 + 6 * step + swing)
        for k in kick_steps:
            place(buf, bb_kick() * (1 if k == 0 else 0.85), t0 + k * step + (swing if k % 2 else 0))
            place(buf, eight08(roots[b % 4] * (1 if k != 10 else 1.5), step * 3) * 0.9, t0 + k * step + (swing if k % 2 else 0))
        for sn in snare_steps:
            place(buf, bb_snare(), t0 + sn * step)
        place(buf, bb_snare() * 0.18, t0 + 15 * step + swing)  # ghost note
        for h in range(16):
            vel = 1.0 if h % 4 == 0 else (0.75 if h % 2 == 0 else 0.45)
            if h % 2 == 1 and np.random.rand() < 0.4:
                continue
            place(buf, hat(open_=(h == 14)) * vel * 1.1, t0 + h * step + (swing if h % 2 else 0))
    buf = buf[: int(seconds * SR)] + crackle(seconds)
    buf = np.tanh(buf * 1.15)
    return buf / (np.max(np.abs(buf)) + 1e-9) * 0.89


def build(bpm, seconds, mood):
    if mood == "boombap":
        return build_boombap(bpm, seconds)
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
