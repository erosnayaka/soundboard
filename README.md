# Soundboard

Soundboard Windows sederhana: taruh file audio sendiri, atur global hotkey bebas, suara bunyi walau lagi main game / buka aplikasi lain.

Terinspirasi dari [DCSB](https://github.com/kalejin/dcsb) (Deathcounter and Soundboard).

## Cara pakai (tanpa install ribet)

1. Download `Soundboard.zip` dari [Releases](../../releases) (atau build sendiri, lihat bawah), ekstrak.
2. Taruh file suara kamu (mp3/wav/ogg) ke folder `sounds/`.
3. Edit `config.txt` buat atur hotkey:
   ```
   num 1 = airhorn.mp3, 1.0
   f9    = laugh.mp3, 0.8
   ```
   Format: `hotkey = nama file, volume (0.0 - 1.0)`.
   Numpad pakai spasi: `num 1` ... `num 9` (bukan `num1`), dan NumLock harus nyala.
4. Double-click `Soundboard.exe`. Biarkan jalan di background (bisa di-minimize).

Hotkey khusus:

| config | fungsi |
|---|---|
| `stop = ctrl+alt+0` | matikan semua suara yang lagi bunyi |
| `quit = ctrl+alt+q` | keluar dari soundboard |

Catatan:
- Suara bisa bunyi bareng (overlap, 16 channel).
- Kalau hotkey nggak jalan di dalam game, klik kanan exe → *Run as administrator*.
- Salah ketik nama hotkey di config tidak bikin crash — cuma dilewati dengan peringatan.

## Jalan dari source (Python)

Butuh Python 3.10+ (Windows):

```cmd
pip install -r requirements.txt
python soundboard.py
```

Tanpa `config.txt`, mapping default diambil dari bagian `SETTING` di atas `soundboard.py`.

## Keamanan

Script ini murni Python + 2 library umum (`keyboard`, `pygame`): tidak ada akses network, tidak nulis registry, tidak download apa pun. Cek sendiri isi `soundboard.py` — cuma ~150 baris. Kalau ragu sama file `.exe`, build sendiri dari source (lihat `BUILD.md`) atau scan di [VirusTotal](https://www.virustotal.com/).

## Lisensi

MIT — bebas pakai, ubah, dan share.
