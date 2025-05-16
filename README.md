


 🧠 Focus Timer with Ambient Music & Distraction Blocking

A customizable Pomodoro timer that helps you stay focused with:
- Ambient background music 🎵
- Fullscreen blocking UI during focus mode ⛔
- Task Manager hiding and key blocking (Alt, Ctrl+Esc, etc.) 🔒
- Tkinter-based GUI with Start/Reset options

 🚀 Features

- Pomodoro cycle with focus and break time settings
- Random ambient music playback from multiple online sources
- Fullscreen block screen to reduce distractions
- Key blocking (Alt, Alt+Tab, Win, Esc, Ctrl+Esc, Alt+F4)
- Auto-hides Task Manager during focus time
- Converts to .exe easily using PyInstaller

 🛠 Installation

1. Clone the repository or download the .py file.
2. Install dependencies:

bash
pip install -r requirements.txt


3. Run the script:

bash
python pomodoro_timer.py


 🔒 Admin Privileges

* This app **must be run as administrator** to block system keys and hide Task Manager.

 🧾 Requirements

* Python 3.7+
* Internet connection (for streaming ambient music)
* Windows OS (uses win32gui, win32con for Task Manager hiding)

 📦 Convert to EXE (Optional)

Install PyInstaller and run:

bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed pomodoro_timer.py


Find the .exe in the build folder.



 📄 License

MIT License



---

 ✅ requirements.txt

txt
pygame
requests
keyboard
psutil
pywin32


---

