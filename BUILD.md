# Build Soundboard.exe sendiri (Windows)

## Cara gampang (di PC Windows)

```cmd
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --noconsole --name Soundboard soundboard.py
```

Hasilnya ada di `dist/Soundboard.exe`. File `config.txt` dan folder `sounds/` tetap dibaca dari sebelah exe (tidak ikut dibundel, biar gampang diganti).

> Catatan: contoh ini pakai `--noconsole` (tanpa jendela console). Build rilis di repo ini pakai console supaya error kelihatan saat troubleshooting.

## Cara yang dipakai buat rilis di repo ini

Exe rilis dibuild di Linux pakai [Wine](https://www.winehq.org/) 9.0 + Python 3.12 Windows + PyInstaller 6.22.3, dengan `Soundboard.spec`:

```
pyinstaller Soundboard.spec
```

Spec tersebut membundel 3 suara demo (`sounds/demo*.wav`) ke dalam exe sebagai fallback, dan mengaktifkan UPX. Hasilnya PE32+ x86-64 yang terverifikasi bisa start di Wine (audio dummy) sebelum dirilis.

## Bikin zip rilis

```
Soundboard/
├── Soundboard.exe
├── config.txt
└── sounds/
    └── (taruh mp3/wav/ogg kamu di sini)
```

Zip folder itu jadi `Soundboard.zip`, upload ke GitHub Releases.
