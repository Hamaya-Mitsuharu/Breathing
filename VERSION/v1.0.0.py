import tkinter as tk
from tkinter import ttk
import threading
import time


class BreathingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Breathing App")
        self.root.geometry("300x160")
        self.root.resizable(False, False)

        # =======================
        # ★ 調整可能パラメータ ★
        # =======================

        self.fade_duration = 4000     # フェードイン＋アウトの総時間(ms)
        self.fade_steps = 40          # フェード分割数（滑らかさ）
        self.interval_between = 1000  # 次の呼吸までの待機時間(ms)

        # =======================

        self.running = False
        self.fade_window = None

        self.create_ui()

    # ================= UI =================

    def create_ui(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="深呼吸アプリ", font=("Segoe UI", 14)).pack(pady=(0, 15))

        btn_frame = ttk.Frame(frame)
        btn_frame.pack()

        ttk.Button(btn_frame, text="開始", command=self.start).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="停止", command=self.stop).pack(side="left", padx=10)

    # ================= 制御 =================

    def start(self):
        if self.running:
            return
        self.running = True
        self.loop_breathing()

    def stop(self):
        self.running = False
        if self.fade_window:
            self.fade_window.destroy()
            self.fade_window = None

    # ================= 呼吸ループ =================

    def loop_breathing(self):
        if not self.running:
            return

        self.create_fade_popup()

        # 次の呼吸を予約
        total_cycle = self.fade_duration + self.interval_between
        self.root.after(total_cycle, self.loop_breathing)

    # ================= フェード処理 =================

    def create_fade_popup(self):
        if self.fade_window:
            self.fade_window.destroy()

        win = tk.Toplevel(self.root)
        self.fade_window = win

        win.overrideredirect(True)
        win.attributes("-topmost", True)
        win.configure(bg="#d8f5d0")
        win.attributes("-alpha", 0.0)

        size = 400
        screen_w = win.winfo_screenwidth()
        screen_h = win.winfo_screenheight()

        x = screen_w // 2 - size // 2
        y = screen_h // 2 - size // 2

        frame = tk.Frame(win, bg="#d8f5d0", width=size, height=size)
        frame.pack()

        win.geometry(f"{size}x{size}+{x}+{y}")

        steps = self.fade_steps
        interval = self.fade_duration // steps

        def fade(step=0):
            if not self.running:
                win.destroy()
                return

            # 前半：フェードイン（吸う）
            if step <= steps // 2:
                alpha = step / (steps // 2)
            # 後半：フェードアウト（吐く）
            else:
                alpha = (steps - step) / (steps // 2)

            win.attributes("-alpha", max(0, min(1, alpha)))

            if step < steps:
                win.after(interval, fade, step + 1)
            else:
                win.destroy()

        fade()


if __name__ == "__main__":
    root = tk.Tk()
    app = BreathingApp(root)
    root.mainloop()