# 🗂️ File Organizer — Python Automation

A Python automation tool that instantly sorts a messy folder into organized subfolders by file extension — built using the `os` and `shutil` libraries.

---

## 💡 The Real Scenario

You're an IT administrator. Your manager asks you to find the **database file** from a shared folder.

You open the folder and find **941 mixed files**:

```
photo_1.jpg, movie.avi, script.py, backup.zip, song.mp3,
report.pdf, employees.db, animation.swift, archive.rar ...
```

❌ **Without the organizer** — you scroll through 941 files trying to spot the database file. Takes forever. Easy to miss.

✅ **With the organizer** — run the script. Files are sorted instantly:

```
My_Files/
├── Database/
│   └── database file   ← found in 1 second
├── Images/
├── Videos/
├── Documents/
├── Code/
└── ...
```

---

## 🚀 How to Use

### Step 1 — Generate the demo folder
Run `Creating_files.py` to instantly create 941 mixed files:
```bash
python Creating_files.py
```

### Step 2 — The challenge
Your manager asks you to contact the HR recruiter urgently. The database is somewhere in that folder — find it, open it, and look up **Doroteo Arnaiz's email**.

Open `Generated_Files/` — good luck finding it among 941 files. 😅

### Step 3 — Run the organizer
```bash
python File_organizer.py
```

### Step 4 — Try again
Open `Generated_Files/Database/` — it's right there. 🎯

### Step 5 — 🔐 Bonus challenge
Found the email? Send a message to **Doroteo Arnaiz** and mention the **passkey** you found in the database. Let's see if you really looked closely. 👀

---

## 📁 Supported Categories

| Category | Extensions |
|---|---|
| Images | jpg, jpeg, png, gif, bmp, svg, ico, tif, raw, psd, webp |
| Videos | mp4, avi, mov, mkv, wmv, flv, webm, mpeg, 3gpp |
| Documents | pdf, doc, docx, xls, xlsx, ppt, pptx, txt, csv, rtf |
| Code | py, js, html, css, json, java, cpp, php, ts, jsx, swift, dart |
| Audio | mp3, wav, aac, flac, ogg, m4a, wma, opus, aiff |
| Archives | zip, rar, tar, gz, 7z, bz2, cab |
| Executables | exe, msi, apk, deb, rpm |
| Fonts | ttf, otf, woff, woff2 |
| Database | sqlite, sql, db, mdb |
| Ebooks | epub, mobi, cbr, azw3 |
| Disk Images | iso, img, bin, vmdk |
| Backup | bak, bkp, tmp |
| System | dll, sys, ini, cfg, bat, log, reg, conf |
| Others | anything not listed above |

---

## 🐢 Want to Watch It Happen in Slow Motion?

The code includes two commented lines that add a 0.5s delay between each file move — so you can visually watch each file being organized one by one.

To enable it, uncomment these two lines in `File_organizer.py`:

```python
# import time        ← uncomment this (line 3)
# time.sleep(0.5)    ← uncomment this (inside the loop)
```

---

## 🛠️ Built With

- Python 3
- `os` module — for reading and navigating the file system
- `shutil` module — for moving files between folders

---

## 👤 Author

**Ibrahim Mejjadi** — [linkedin.com/in/ibrahimmejjadi](https://linkedin.com/in/ibrahimmejjadi) · [github.com/ibrahimmejjadi](https://github.com/ibrahimmejjadi)
