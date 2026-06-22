import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import time


# ---------------- FUNCTIONS ---------------- #

def generate_music():
    global generate_btn, progress, status, time_label

    start = time.time()

    try:
        status.config(text="Generating Music...")
        generate_btn.config(state="disabled")

        progress.start(10)
        window.update()

        subprocess.run(
            [
                "python",
                "generate.py",
                "--notes", str(notes_var.get()),
                "--temperature", str(temp_var.get()),
                "--instrument", instrument_var.get()
            ],
            check=True
        )

        progress.stop()

        end = time.time()

        status.config(text="Music Generated Successfully!")
        time_label.config(text=f"Time: {round(end-start,2)} sec")

        generate_btn.config(state="normal")

        if os.path.exists("generated_music.mid"):
            os.startfile("generated_music.mid")
            messagebox.showinfo("Success", "Music Generated Successfully!")

        else:
            messagebox.showwarning("Warning", "MIDI file not found!")

    except subprocess.CalledProcessError:
        progress.stop()
        generate_btn.config(state="normal")
        status.config(text="Generation Failed!")
        messagebox.showerror("Error", "Error while running generate.py")

    except Exception as e:
        progress.stop()
        generate_btn.config(state="normal")
        status.config(text="Error!")
        messagebox.showerror("Error", str(e))


def play_music():
    if os.path.exists("generated_music.mid"):
        os.startfile("generated_music.mid")
    else:
        messagebox.showwarning("Warning", "Generate music first!")


def open_folder():
    os.startfile(os.getcwd())


# ---------------- WINDOW ---------------- #

window = tk.Tk()
window.title("AI Music Generator")
window.geometry("700x650")
window.configure(bg="#1E1E2F")
window.state('zoomed')
window.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TProgressbar",
    thickness=18,
    troughcolor="#2B2B40",
    background="#00E676"
)

# ---------------- TITLE ---------------- #

tk.Label(
    window,
    text="🎼 AI Music Generator 🎵",
    font=("Arial", 26, "bold"),
    bg="#1E1E2F",
    fg="#00E5FF"
).pack(pady=20)

tk.Label(
    window,
    text="Generate AI-Based MIDI Music",
    font=("Arial", 12),
    bg="#1E1E2F",
    fg="white"
).pack()

# ---------------- STATUS ---------------- #

status = tk.Label(
    window,
    text="Ready",
    bg="#1E1E2F",
    fg="#00E676",
    font=("Arial", 11, "bold")
)
status.pack(pady=10)

progress = ttk.Progressbar(
    window,
    orient="horizontal",
    length=450,
    mode="indeterminate"
)
progress.pack(pady=10)

# ---------------- FRAME ---------------- #

frame = tk.Frame(window, bg="#2B2B40", bd=2, relief="ridge")
frame.pack(padx=20, pady=20, fill="x")

# ---------------- NOTES ---------------- #

tk.Label(
    frame,
    text="🎼 Number of Notes",
    bg="#2B2B40",
    fg="white"
).grid(row=0, column=0, padx=20, pady=20)

notes_var = tk.IntVar(value=500)

ttk.Combobox(
    frame,
    textvariable=notes_var,
    values=list(range(100, 1100, 100)),
    state="readonly",
    width=18
).grid(row=0, column=1)

# ---------------- TEMPERATURE ---------------- #

tk.Label(
    frame,
    text="🌡 Temperature",
    bg="#2B2B40",
    fg="white"
).grid(row=1, column=0, padx=20, pady=20)

temp_var = tk.DoubleVar(value=1.0)

ttk.Combobox(
    frame,
    textvariable=temp_var,
    values=[0.5, 0.7, 0.9, 1.0, 1.1, 1.3, 1.5],
    state="readonly",
    width=18
).grid(row=1, column=1)

# ---------------- INSTRUMENT ---------------- #

tk.Label(
    frame,
    text="🎹 Instrument",
    bg="#2B2B40",
    fg="white"
).grid(row=2, column=0, padx=20, pady=20)

instrument_var = tk.StringVar(value="Piano")

ttk.Combobox(
    frame,
    textvariable=instrument_var,
    values=["Piano", "Guitar", "Violin", "Flute", "Trumpet"],
    state="readonly",
    width=18
).grid(row=2, column=1)

# ---------------- BUTTONS ---------------- #

generate_btn = tk.Button(
    window,
    text="🚀 Generate Music",
    command=generate_music,
    bg="#2962FF",
    fg="white",
    font=("Arial", 14, "bold"),
    width=22,
    height=2
)
generate_btn.pack(pady=10)

tk.Button(
    window,
    text="▶ Play Music",
    command=play_music,
    bg="#00C853",
    fg="white",
    width=22
).pack(pady=5)

tk.Button(
    window,
    text="📂 Open Folder",
    command=open_folder,
    bg="#FF9800",
    fg="white",
    width=22
).pack(pady=5)

tk.Button(
    window,
    text="❌ Exit",
    command=window.destroy,
    bg="#D50000",
    fg="white",
    width=22
).pack(pady=5)

# ---------------- TIME LABEL ---------------- #

time_label = tk.Label(
    window,
    text="",
    bg="#1E1E2F",
    fg="#FFD54F",
    font=("Arial", 11, "bold")
)
time_label.pack(pady=10)

window.mainloop()