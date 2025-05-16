import tkinter as tk
from tkinter import messagebox
import pygame
import requests
import io
import random
import keyboard
import threading
import time
import psutil
import win32gui
import win32con

ambient_urls = [
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
    "https://files.freemusicarchive.org/storage-freemusicarchive-org/music/ccCommunity/Kai_Engel/Century/Century_-_05_-_Ambient_Story.mp3",
    "https://files.freemusicarchive.org/storage-freemusicarchive-org/music/ccCommunity/Scott_Holmes/Corporate_Themes/Scott_Holmes_-_07_-_Ambient_Motivation.mp3",
    "https://www.bensound.com/bensound-music/bensound-slowmotion.mp3",
    "https://www.bensound.com/bensound-music/bensound-sunny.mp3",
    "https://archive.org/download/ambient-soundscape-01/Ambient_Soundscape_01.mp3",
    "https://cdn.pixabay.com/download/audio/2022/03/15/audio_5b57f3d30f.mp3?filename=calm-instrumental-ambient-background-music-11232.mp3"
]


class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Focus Timer")
        self.root.geometry("350x400")
        self.root.configure(bg="#e3f2fd")

        pygame.mixer.init()

        tk.Label(root, text="Pomodoro Timer", font=("Helvetica", 20, "bold"), bg="#e3f2fd").pack(pady=10)

        form = tk.Frame(root, bg="#e3f2fd")
        form.pack(pady=10)

        tk.Label(form, text="Focus Time (min):", bg="#e3f2fd").grid(row=0, column=0, sticky='e')
        self.focus_entry = tk.Entry(form, width=5)
        self.focus_entry.insert(0, "25")
        self.focus_entry.grid(row=0, column=1, padx=10)

        tk.Label(form, text="Break Time (min):", bg="#e3f2fd").grid(row=1, column=0, sticky='e')
        self.break_entry = tk.Entry(form, width=5)
        self.break_entry.insert(0, "5")
        self.break_entry.grid(row=1, column=1, padx=10)

        self.status_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#e3f2fd")
        self.status_label.pack()

        self.timer_label = tk.Label(root, text="00:00", font=("Helvetica", 48), bg="#e3f2fd")
        self.timer_label.pack(pady=10)

        self.start_button = tk.Button(root, text="Start Focus", command=self.confirm_focus, bg="#2196f3", fg="white")
        self.start_button.pack(pady=10)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer, state="disabled")
        self.reset_button.pack()

        self.running = False
        self.is_focus = True
        self.time_left = 0
        self.confirm_countdown = 10
        self.blocker = None

    def confirm_focus(self):
        answer = messagebox.askyesno("Start Focus", "Start focus session now?")
        if answer:
            self.status_label.config(text="Starting in 10 seconds. Get ready...")
            self.start_button.config(state="disabled")
            self.countdown_confirm()

    def countdown_confirm(self):
        if self.confirm_countdown > 0:
            self.timer_label.config(text=f"00:{self.confirm_countdown:02d}")
            self.confirm_countdown -= 1
            self.root.after(1000, self.countdown_confirm)
        else:
            self.confirm_countdown = 10
            self.start_timer()

    def start_timer(self):
        try:
            focus_min = int(self.focus_entry.get())
            break_min = int(self.break_entry.get())
            self.focus_time = focus_min * 60
            self.break_time = break_min * 60
            self.time_left = self.focus_time if self.is_focus else self.break_time
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers.")
            self.start_button.config(state="normal")
            return

        self.running = True
        self.reset_button.config(state="normal")
        self.status_label.config(text="Focus Time!" if self.is_focus else "Break Time!")
        self.play_random_ambient_music()
        self.block_keys()
        self.block_screen()
        self.hide_task_manager()
        self.countdown()

    def reset_timer(self):
        self.running = False
        self.time_left = 0
        self.timer_label.config(text="00:00")
        self.status_label.config(text="")
        self.start_button.config(state="normal")
        self.reset_button.config(state="disabled")
        pygame.mixer.music.stop()
        self.unblock_keys()
        self.unblock_screen()

    def countdown(self):
        if self.time_left > 0 and self.running:
            self.timer_label.config(text=self.format_time(self.time_left))
            self.time_left -= 1
            self.root.after(1000, self.countdown)
        elif self.running:
            pygame.mixer.music.stop()
            self.running = False
            self.is_focus = not self.is_focus
            self.reset_button.config(state="disabled")
            self.start_button.config(state="normal")
            self.unblock_keys()
            self.unblock_screen()
            self.status_label.config(text="")
            messagebox.showinfo("Pomodoro", "Break Time!" if not self.is_focus else "Focus Time!")
            self.timer_label.config(text=self.format_time(self.focus_time if self.is_focus else self.break_time))

    def format_time(self, secs):
        mins, secs = divmod(secs, 60)
        return f"{mins:02d}:{secs:02d}"

    def play_random_ambient_music(self):
        try:
            url = random.choice(ambient_urls)
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                music_data = io.BytesIO()
                for chunk in response.iter_content(chunk_size=4096):
                    if chunk:
                        music_data.write(chunk)
                music_data.seek(0)
                pygame.mixer.music.load(music_data)
                pygame.mixer.music.play(-1)
        except Exception as e:
            print("Error playing music:", e)

    def block_screen(self):
        if self.is_focus:
            self.blocker = tk.Toplevel(self.root)
            self.blocker.attributes("-fullscreen", True)
            self.blocker.configure(bg="black")
            tk.Label(self.blocker, text="Stay Focused!", font=("Arial", 32), fg="white", bg="black").pack(expand=True)
            self.blocker.attributes("-topmost", True)
            self.blocker.protocol("WM_DELETE_WINDOW", lambda: None)

    def unblock_screen(self):
        if self.blocker and self.blocker.winfo_exists():
            self.blocker.destroy()

    def block_keys(self):
        keys = ['alt', 'alt+tab', 'tab', 'win', 'esc', 'ctrl+esc', 'ctrl+alt+del', 'alt+f4']
        for key in keys:
            try:
                keyboard.block_key(key)
            except:
                pass

    def unblock_keys(self):
        keyboard.unhook_all()

    def hide_task_manager(self):
        def monitor():
            while self.running and self.is_focus:
                try:
                    for proc in psutil.process_iter(['name']):
                        if proc.info['name'] and proc.info['name'].lower() == 'taskmgr.exe':
                            hwnd = win32gui.FindWindow(None, "Task Manager")
                            if hwnd:
                                win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
                    time.sleep(2)
                except:
                    pass
        threading.Thread(target=monitor, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
