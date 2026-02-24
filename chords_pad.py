import tkinter as tk
import pygame
import os, time, json, sys
import pyautogui
import keyboard
import subprocess

# ── Paths ─────────────────────────────────────────────────────────────────
if getattr(sys, 'frozen', False):
    BUNDLE_DIR = sys._MEIPASS
else:
    BUNDLE_DIR = os.path.dirname(os.path.abspath(__file__))

CHORDS_DIR = os.path.join(BUNDLE_DIR, "chords")

# ── Config (ενσωματωμένο) ─────────────────────────────────────────────────
cfg = json.loads("""
{
  "window": {
    "title": "Chords Pad",
    "always_on_top": true
  },
  "rows": [
    { "is_header": true, "labels": [ "Play Chord", "", "Insert Ch" ] },
    { "buttons": [
      { "label": "A",   "play": "A",   "insert": null,    "bg": "#cccccc", "fg": "#444444" },
      { "label": "Am",  "play": "Am",  "insert": null,    "bg": "#cccccc", "fg": "#444444" },
      { "label": "A",   "play": "A",   "insert": "[A]",   "bg": "#d4d0c8", "fg": "#000000" },
      { "label": "Am",  "play": "Am",  "insert": "[Am]",  "bg": "#d4d0c8", "fg": "#000000" }
    ]},
    { "buttons": [
      { "label": "Bb",  "play": "Bb",  "insert": null,    "bg": "#cccccc", "fg": "#444444" },
      { "label": "Bbm", "play": "Bbm", "insert": null,    "bg": "#cccccc", "fg": "#444444" },
      { "label": "Bb",  "play": "Bb",  "insert": "[Bb]",  "bg": "#d4d0c8", "fg": "#000000" },
      { "label": "Bbm", "play": "Bbm", "insert": "[Bbm]", "bg": "#d4d0c8", "fg": "#000000" }
    ]},
    { "buttons": [
      { "label": "B",   "play": "B",   "insert": null,   "bg": "#cccccc", "fg": "#444444" },
      { "label": "Bm",  "play": "Bm",  "insert": null,   "bg": "#cccccc", "fg": "#444444" },
      { "label": "B",   "play": "B",   "insert": "[B]",  "bg": "#d4d0c8", "fg": "#000000" },
      { "label": "Bm",  "play": "Bm",  "insert": "[Bm]", "bg": "#d4d0c8", "fg": "#000000" }
    ]},
    { "buttons": [
      { "label": "C",   "play": "C",   "insert": null,   "bg": "#cccccc", "fg": "#444444" },
      { "label": "Cm",  "play": "Cm",  "insert": null,   "bg": "#cccccc", "fg": "#444444" },
      { "label": "C",   "play": "C",   "insert": "[C]",  "bg": "#d4d0c8", "fg": "#000000" },
      { "label": "Cm",  "play": "Cm",  "insert": "[Cm]", "bg": "#d4d0c8", "fg": "#000000" }
    ]},
    { "buttons": [
      { "label": "C#",  "play": "Ch",  "insert": null,    "bg": "#cccccc", "fg": "#444444" },
      { "label": "C#m", "play": "Chm", "insert": null,    "bg": "#cccccc", "fg": "#444444" },
      { "label": "C#",  "play": "Ch",  "insert": "[C#]",  "bg": "#d4d0c8", "fg": "#000000" },
      { "label": "C#m", "play": "Chm", "insert": "[C#m]", "bg": "#d4d0c8", "fg": "#000000" }
    ]},
    { "buttons": [
      { "label": "D",   "play": "D",   "insert": null,   "bg": "#cccccc", "fg": "#444444" },
      { "label": "Dm",  "play": "Dm",  "insert": null,   "bg": "#cccccc", "fg": "#444444" },
      { "label": "D",   "play": "D",   "insert": "[D]",  "bg": "#d4d0c8", "fg": "#000000" },
      { "label": "Dm",  "play": "Dm",  "insert": "[Dm]", "bg": "#d4d0c8", "fg": "#000000" }
    ]},
    { "buttons": [
      { "label": "D#",  "play": "Dh",  "insert": null,    "bg": "#cccccc", "fg": "#444444" },
      { "label": "D#m", "play": "Dhm", "insert": null,    "bg": "#cccccc", "fg": "#444444" },
      { "label": "D#",  "play": "Dh",  "insert": "[D#]",  "bg": "#d4d0c8", "fg": "#000000" },
      { "label": "D#m", "play": "Dhm", "insert": "[D#m]", "bg": "#d4d0c8", "fg": "#000000" }
    ]},
    { "buttons": [
      { "label": "E",   "play": "E",   "insert": null,   "bg": "#cccccc", "fg": "#cc00cc" },
      { "label": "Em",  "play": "Em",  "insert": null,   "bg": "#cccccc", "fg": "#cc00cc" },
      { "label": "E",   "play": "E",   "insert": "[E]",  "bg": "#d4d0c8", "fg": "#cc00cc" },
      { "label": "Em",  "play": "Em",  "insert": "[Em]", "bg": "#d4d0c8", "fg": "#cc00cc" }
    ]},
    { "buttons": [
      { "label": "F",   "play": "F",   "insert": null,   "bg": "#cccccc", "fg": "#444444" },
      { "label": "Fm",  "play": "Fm",  "insert": null,   "bg": "#cccccc", "fg": "#444444" },
      { "label": "F",   "play": "F",   "insert": "[F]",  "bg": "#d4d0c8", "fg": "#000000" },
      { "label": "Fm",  "play": "Fm",  "insert": "[Fm]", "bg": "#d4d0c8", "fg": "#000000" }
    ]},
    { "buttons": [
      { "label": "F#",  "play": "Fh",  "insert": null,    "bg": "#cccccc", "fg": "#444444" },
      { "label": "F#m", "play": "Fhm", "insert": null,    "bg": "#cccccc", "fg": "#444444" },
      { "label": "F#",  "play": "Fh",  "insert": "[F#]",  "bg": "#d4d0c8", "fg": "#000000" },
      { "label": "F#m", "play": "Fhm", "insert": "[F#m]", "bg": "#d4d0c8", "fg": "#000000" }
    ]},
    { "buttons": [
      { "label": "G",   "play": "G",   "insert": null,   "bg": "#cccccc", "fg": "#444444" },
      { "label": "Gm",  "play": "Gm",  "insert": null,   "bg": "#cccccc", "fg": "#444444" },
      { "label": "G",   "play": "G",   "insert": "[G]",  "bg": "#d4d0c8", "fg": "#000000" },
      { "label": "Gm",  "play": "Gm",  "insert": "[Gm]", "bg": "#d4d0c8", "fg": "#000000" }
    ]},
    { "buttons": [
      { "label": "G#",  "play": "Gh",  "insert": null,    "bg": "#cccccc", "fg": "#444444" },
      { "label": "G#m", "play": "Ghm", "insert": null,    "bg": "#cccccc", "fg": "#444444" },
      { "label": "G#",  "play": "Gh",  "insert": "[G#]",  "bg": "#d4d0c8", "fg": "#000000" },
      { "label": "G#m", "play": "Ghm", "insert": "[G#m]", "bg": "#d4d0c8", "fg": "#000000" }
    ]},
    { "is_separator": true },
    { "buttons": [
      { "label": "Adim", "play": "Adim", "insert": null,     "bg": "#cccccc", "fg": "#444444" },
      { "label": "Ddim", "play": "Ddim", "insert": null,     "bg": "#cccccc", "fg": "#444444" },
      { "label": "Adim", "play": "Adim", "insert": "[Adim]", "bg": "#d4d0c8", "fg": "#000000" },
      { "label": "Ddim", "play": "Ddim", "insert": "[Ddim]", "bg": "#d4d0c8", "fg": "#000000" }
    ]},
    { "buttons": [
      { "label": "Edim", "play": "Edim", "insert": null,     "bg": "#cccccc", "fg": "#444444" },
      { "label": "(",    "play": null,   "insert": "(",       "bg": "#d4d0c8", "fg": "#000000" },
      { "label": "Edim", "play": "Edim", "insert": "[Edim]", "bg": "#d4d0c8", "fg": "#000000" },
      { "label": ")",    "play": null,   "insert": ")",       "bg": "#d4d0c8", "fg": "#000000" }
    ]},
    { "is_separator": true },
    { "buttons": [
      { "label": "S. C.", "play": null, "insert": "σόλο κουπλέ", "bg": "#d4d0c8", "fg": "#000000" },
      { "label": "S. R.", "play": null, "insert": "σόλο ρεφρέν",  "bg": "#d4d0c8", "fg": "#000000" },
      { "label": "Undo",  "play": null, "insert": "__UNDO__",     "bg": "#ff9999", "fg": "#cc0000" },
      { "label": "δις",   "play": null, "insert": "δις",          "bg": "#ffff99", "fg": "#9900ff" }
    ]}
  ]
}
""")

WIN = cfg["window"]

# ── Audio ──────────────────────────────────────────────────────────────────
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

def play_chord(stem):
    path = os.path.join(CHORDS_DIR, stem + ".mp3")
    if os.path.exists(path):
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

# ── Insert ────────────────────────────────────────────────────────────────
def do_insert(text, go_home=False):
    pyautogui.hotkey('alt', 'tab')
    time.sleep(0.1)
    if go_home:
        pyautogui.hotkey('ctrl', 'home')
    keyboard.write(text)

def do_undo():
    pyautogui.hotkey('alt', 'tab')
    time.sleep(0.1)
    keyboard.press_and_release('ctrl+z')

def insert_metadata():
    t_val = entry_t.get()
    s_val = entry_s.get()
    m_val = entry_m.get()
    k_val = entry_k.get()
    key_val = entry_key.get()
    
    metadata = f"{{t:{t_val}}}\n{{meta: custom {s_val}}}\n{{composer:{m_val}}}\n{{artist:{k_val}}}\n{{st:Ρεμπέτικο Στίχοι: {s_val} / Μουσική:{m_val}}}\n{{key:{key_val}}}"
    do_insert(metadata, go_home=True)
    keyboard.press_and_release('enter')

def insert_blue():
    do_insert("<span color=blue>")

def insert_green():
    do_insert("<span color=green>")

def insert_red():
    do_insert("<span color=red>")

# ── Button action ─────────────────────────────────────────────────────────
def btn_action(b):
    ins = b.get("insert")
    if ins == "__UNDO__":
        do_undo()
    elif ins == "__CLOSE__":
        root.destroy()
    elif ins == "__RESTART__":
        root.destroy()
        subprocess.Popen([sys.executable, __file__])
    elif ins:
        if b.get("play"):
            play_chord(b["play"])
        if not ins.startswith("[") and not ins.endswith("]"):
            ins = f"[{ins}]"
        do_insert(ins)
    elif b.get("play"):
        play_chord(b["play"])

# ── UI ─────────────────────────────────────────────────────────────────────
root = tk.Tk()
root.title(WIN.get("title", "Chords Pad"))
root.resizable(False, False)
root.attributes("-topmost", bool(WIN.get("always_on_top", True)))
root.attributes("-toolwindow", True)
root.configure(bg="#d4d0c8")

# ── Metadata Input Fields ──────────────────────────────────────────────────
metadata_frame = tk.Frame(root, bg="#d4d0c8")
metadata_frame.pack(padx=3, pady=3, fill="x")

fields_single = [
    ("Τ:", "entry_t"),
    ("Σ:", "entry_s"),
    ("Μ:", "entry_m"),
    ("Κ:", "entry_k")
]

for label_text, var_name in fields_single:
    field_frame = tk.Frame(metadata_frame, bg="#d4d0c8")
    field_frame.pack(pady=2)

    tk.Label(field_frame, text=label_text, bg="#d4d0c8", anchor="w").pack(side="left", padx=0)
    entry = tk.Entry(field_frame, width=18, font=("Tahoma", 8))
    entry.pack(side="left", padx=0)

    globals()[var_name] = entry

key_frame = tk.Frame(metadata_frame, bg="#d4d0c8")
key_frame.pack(pady=2)

tk.Label(key_frame, text="Key:", bg="#d4d0c8", anchor="w").pack(side="left", padx=0)
entry_key = tk.Entry(key_frame, width=3, font=("Tahoma", 8))
entry_key.pack(side="left", padx=0)

insert_meta_btn = tk.Button(key_frame, text="Insert", bg="#cccccc", fg="#000000",
                              font=("Tahoma", 8), command=insert_metadata)
insert_meta_btn.pack(side="left", padx=2)

btn_frame = tk.Frame(metadata_frame, bg="#d4d0c8")
btn_frame.pack(pady=2)

blue_btn = tk.Button(btn_frame, text="Blue", bg="#ffff99", fg="#000000",
                      font=("Tahoma", 8), command=insert_blue)
blue_btn.pack(side="left", padx=2)

green_btn = tk.Button(btn_frame, text="Green", bg="#ff99ff", fg="#000000",
                       font=("Tahoma", 8), command=insert_green)
green_btn.pack(side="left", padx=2)

red_btn = tk.Button(btn_frame, text="Red", bg="#99ccff", fg="#000000",
                     font=("Tahoma", 8), command=insert_red)
red_btn.pack(side="left", padx=2)

separator1 = tk.Frame(root, bg="#999999", height=2)
separator1.pack(fill="x", padx=3, pady=2)

for row_def in cfg["rows"]:
    if row_def.get("is_separator"):
        tk.Frame(root, bg="#999999", height=2).pack(fill="x", padx=3, pady=2)
        continue

    if row_def.get("is_header"):
        hf = tk.Frame(root, bg="#d4d0c8")
        hf.pack(padx=3, pady=(4, 0))
        hcol = 0
        for c, lbl in enumerate(row_def["labels"]):
            if c == 2:
                tk.Label(hf, text="", bg="#d4d0c8", width=1).grid(row=0, column=hcol)
                hcol += 1
            tk.Label(hf, text=lbl, bg="#d4d0c8", fg="#666666",
                     font=("Tahoma", 7, "italic")).grid(row=0, column=hcol, padx=1)
            hcol += 1
        continue

    rf = tk.Frame(root, bg="#d4d0c8")
    rf.pack(padx=3, pady=0)
    grid_col = 0
    for c, b in enumerate(row_def["buttons"]):
        if c == 2:
            tk.Frame(rf, bg="#999999", width=2).grid(row=0, column=grid_col, padx=3, pady=1, sticky="ns")
            grid_col += 1
        if b.get("hidden"):
            tk.Frame(rf, bg="#d4d0c8").grid(row=0, column=grid_col, padx=1, pady=1)
            grid_col += 1
            continue
        bg = b.get("bg", "#d4d0c8")
        fg = b.get("fg", "#000000")
        tk.Button(
            rf,
            text=b["label"],
            bg=bg, fg=fg,
            activebackground=bg,
            font=("Tahoma", 8),
            relief="raised", bd=1,
            padx=0, pady=4, height=1,
            width=4,
            cursor="hand2",
            command=lambda btn=b: btn_action(btn)
        ).grid(row=0, column=grid_col, padx=1, pady=1)
        grid_col += 1

root.mainloop()
