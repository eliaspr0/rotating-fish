"""
gifpopup.py - shows a GIF for a set time at a random spot on screen,
at random intervals, repeating all day.

Run:    python gifpopup.py [path/to/file.gif]
Build:  see build instructions in the chat (PyInstaller).
Quit:   right-click the GIF (dismisses it), or press Ctrl+Alt+Q... see below,
        or end "gifpopup.exe" in Task Manager. Closing is never hidden.
"""
import os
import random
import sys
import tkinter as tk
from PIL import Image, ImageSequence, ImageTk

# ---------------- settings ----------------
PERMANENT = False            # True: show the GIF once at launch and keep it on screen
                             # until you right-click it (which quits the app)
SHOW_SECONDS = (10, 10)        # how long each popup stays (min, max) seconds
GAP_MINUTES = (60, 60)       # random wait between popups (min, max) minutes
MAX_SHOWS_PER_DAY = 0        # 0 = unlimited
SHOW_AT_LAUNCH = True       # also show once right after the app starts (boot/login)
SCALE = (0.8, 1.2)           # random size multiplier (min, max)
KEY = "#ff00ff"              # color treated as transparent (don't use in your GIF)
# ------------------------------------------


def resource_path(name):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)


def load_frames(path, scale):
    img = Image.open(path)
    frames, delays = [], []
    for frame in ImageSequence.Iterator(img):
        rgba = frame.convert("RGBA")
        w, h = rgba.size
        rgba = rgba.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)
        bg = Image.new("RGBA", rgba.size, KEY)
        bg.paste(rgba, mask=rgba.split()[3].point(lambda a: 255 if a > 128 else 0))
        frames.append(bg.convert("RGB"))
        delays.append(max(20, frame.info.get("duration", 100)))
    return frames, delays


class App:
    def __init__(self, gif_path):
        self.gif_path = gif_path
        self.root = tk.Tk()
        self.root.withdraw()
        self.shows_today = 0
        self.day = None
        if PERMANENT or SHOW_AT_LAUNCH:
            self.root.after(0, self.show)
        else:
            self.schedule_next()

    def schedule_next(self):
        gap = random.uniform(*GAP_MINUTES) * 60
        self.root.after(int(gap * 1000), self.show)

    def show(self):
        today = __import__("datetime").date.today()
        if self.day != today:
            self.day, self.shows_today = today, 0
        if MAX_SHOWS_PER_DAY and self.shows_today >= MAX_SHOWS_PER_DAY:
            self.schedule_next()
            return
        self.shows_today += 1
        if not PERMANENT:
            self.schedule_next()

        frames, delays = load_frames(self.gif_path, random.uniform(*SCALE))
        w, h = frames[0].size
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        x = random.randint(0, max(0, sw - w))
        y = random.randint(0, max(0, sh - h))

        win = tk.Toplevel(self.root)
        win.overrideredirect(True)
        win.attributes("-topmost", True)
        win.geometry(f"{w}x{h}+{x}+{y}")
        win.config(bg=KEY)
        try:
            win.attributes("-transparentcolor", KEY)  # Windows
        except tk.TclError:
            pass

        photos = [ImageTk.PhotoImage(f) for f in frames]
        label = tk.Label(win, bg=KEY, bd=0)
        label.pack()
        state = {"i": 0, "alive": True}

        def close(_e=None):
            if state["alive"]:
                state["alive"] = False
                win.destroy()
                if PERMANENT:
                    self.root.destroy()

        def tick():
            if not state["alive"]:
                return
            label.config(image=photos[state["i"]])
            d = delays[state["i"]]
            state["i"] = (state["i"] + 1) % len(photos)
            win.after(d, tick)

        label.bind("<Button-3>", close)  # right-click dismisses
        if not PERMANENT:
            win.after(int(random.uniform(*SHOW_SECONDS) * 1000), close)
        tick()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    gif = sys.argv[1] if len(sys.argv) > 1 else resource_path("popup.gif")
    if not os.path.exists(gif):
        sys.exit(f"GIF not found: {gif}")
    App(gif).run()
