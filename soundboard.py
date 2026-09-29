#!/usr/bin/env python3
"""
Soundboard sederhana (ala DCSB) — Windows.
- Taruh file suara di folder "sounds/" (mp3 / wav / ogg)
- Atur hotkey di bagian SETTING bawah
- Cara jalanin:  python soundboard.py
  (biarkan jalan di background; hotkey aktif walau lagi main game)

Butuh sekali saja:  pip install keyboard pygame
"""

import os
import sys

# ==================== SETTING — EDIT BAGIAN INI ====================
SOUNDS = [
    # format: ("hotkey", "nama file di folder sounds/", volume 0.0 - 1.0)
    # contoh hotkey: "ctrl+alt+1", "ctrl+shift+a", "f9", "alt+z"
    ("ctrl+alt+1", "airhorn.mp3",  1.0),
    ("ctrl+alt+2", "laugh.mp3",    0.9),
    ("ctrl+alt+3", "dramatic.mp3", 0.8),
]

STOP_ALL_HOTKEY = "ctrl+alt+0"   # matikan semua suara yang lagi bunyi
QUIT_HOTKEY     = "ctrl+alt+q"   # keluar dari soundboard
# ===================================================================

BASE_DIR = None
BUNDLED_SOUNDS_DIR = None
if getattr(sys, "frozen", False):
    # jalan sebagai .exe hasil PyInstaller: folder tempat exe berada
    BASE_DIR = os.path.dirname(sys.executable)
    # suara yang di-bundle via --add-data ada di folder temp _MEIPASS
    BUNDLED_SOUNDS_DIR = os.path.join(getattr(sys, "_MEIPASS", BASE_DIR), "sounds")
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUNDS_DIR = os.path.join(BASE_DIR, "sounds")


def find_sound(filename):
    """Cari file suara: sefolder sama exe/script dulu, lalu folder sounds/
    di sebelahnya, terakhir yang di-bundle di dalam exe."""
    for d in (BASE_DIR, SOUNDS_DIR, BUNDLED_SOUNDS_DIR):
        if d:
            p = os.path.join(d, filename)
            if os.path.isfile(p):
                return p
    return None

try:
    import keyboard
except ImportError:
    sys.exit("Belum install: pip install keyboard")

try:
    import pygame
except ImportError:
    sys.exit("Belum install: pip install pygame")


def load_config():
    """Baca config.txt di sebelah script/exe kalau ada (opsional).

    Format per baris:
        ctrl+alt+1 = airhorn.mp3, 1.0
        f9 = laugh.mp3, 0.8
        stop = ctrl+alt+0
        quit = ctrl+alt+q
    Baris kosong dan yang diawali # diabaikan.
    Kalau file tidak ada / kosong, pakai SETTING bawaan di atas.
    """
    sounds = list(SOUNDS)
    stop_key, quit_key = STOP_ALL_HOTKEY, QUIT_HOTKEY
    cfg = os.path.join(BASE_DIR, "config.txt")
    if not os.path.isfile(cfg):
        return sounds, stop_key, quit_key
    parsed = []
    with open(cfg, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, _, val = line.partition("=")
            key, val = key.strip().lower(), val.strip()
            if key == "stop":
                if val:
                    stop_key = val
                continue
            if key == "quit":
                if val:
                    quit_key = val
                continue
            if key and val:
                parts = [p.strip() for p in val.split(",")]
                try:
                    vol = float(parts[1]) if len(parts) > 1 and parts[1] else 1.0
                except ValueError:
                    vol = 1.0
                if parts[0]:
                    parsed.append((key, parts[0], vol))
    if parsed:
        sounds = parsed
    return sounds, stop_key, quit_key


def main():
    os.makedirs(SOUNDS_DIR, exist_ok=True)
    sounds_cfg, stop_key, quit_key = load_config()
    pygame.mixer.init()
    pygame.mixer.set_num_channels(16)  # biar beberapa suara bisa bunyi bareng

    loaded = {}
    for hotkey, filename, volume in sounds_cfg:
        path = find_sound(filename)
        if not path:
            print(f"[!] File tidak ketemu, dilewati: {filename}")
            continue
        try:
            snd = pygame.mixer.Sound(path)
            snd.set_volume(max(0.0, min(1.0, float(volume))))
            loaded[hotkey.lower()] = (filename, snd)
            print(f"[ok] {hotkey:15} -> {filename} (vol {volume})")
        except Exception as e:  # file rusak / format tidak didukung
            print(f"[!] Gagal load {filename}: {e}")

    if not loaded:
        sys.exit("Tidak ada suara yang ke-load. Taruh file suara di folder sounds/ "
                 "lalu sesuaikan nama file di SETTING.")

    def play(hotkey):
        filename, snd = loaded[hotkey]
        snd.play()  # otomatis pakai channel bebas -> bisa overlap
        print(f"main: {filename}")

    def stop_all():
        pygame.mixer.stop()
        print("semua suara dimatikan")

    def safe_add_hotkey(hotkey, callback, args=(), fallback=None):
        """Daftarkan hotkey; kalau nama tombol tidak dikenal, lewati tanpa crash."""
        try:
            keyboard.add_hotkey(hotkey, callback, args=args)
            return hotkey
        except Exception as e:
            print(f"[!] Hotkey tidak dikenal, dilewati: {hotkey} — cek config.txt")
            if fallback:
                try:
                    keyboard.add_hotkey(fallback, callback, args=args)
                    print(f"    -> pakai fallback: {fallback}")
                    return fallback
                except Exception:
                    print(f"[!] Fallback {fallback} juga gagal.")
            return None

    for hotkey in loaded:
        safe_add_hotkey(hotkey, play, args=(hotkey,))

    stop_key = safe_add_hotkey(stop_key, stop_all, fallback=STOP_ALL_HOTKEY) or stop_key
    quit_key = safe_add_hotkey(quit_key, lambda: (print("Keluar."), os._exit(0)),
                              fallback=QUIT_HOTKEY) or quit_key

    print(f"\nSoundboard jalan. {len(loaded)} suara aktif.")
    print(f"Stop semua: {stop_key}  |  Keluar: {quit_key}")
    print("Biarkan window ini terbuka (bisa di-minimize).")
    keyboard.wait()  # standby sampai hotkey quit ditekan


if __name__ == "__main__":
    main()
