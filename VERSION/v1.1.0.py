import tkinter as tk
from tkinter import ttk


class BreathingApp:
    def __init__(self, root):
        self.root = root

        # =======================
        # ★ 調整可能パラメータ ★
        # =======================

        # --- ウィンドウサイズ ---
        self.window_width = 360
        self.window_height = 240

        # --- フェード設定 ---
        self.fade_duration = 3000      # フェードイン＋アウト合計(ms)
        self.fade_steps = 40           # 分割数（滑らかさ）
        self.post_fade_wait = 500      # ★ フェードイン後の保持時間(ms)
        self.interval_between = 500    # 呼吸終了後の待機(ms)

        # --- カラー候補 ---
        self.base_color = (190, 235, 180)  # 緑①（使用中）

        # 他候補（必要なら差し替え）
        # self.base_color = (160, 220, 150)  # 緑②
        # self.base_color = (120, 200, 110)  # 緑③
        # self.base_color = (100, 170, 90)   # 緑④

        # =======================

        self.root.title("Breathing App")
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        self.root.resizable(False, False)

        self.running = False

        self.create_ui()

    # ================= UI =================

    def create_ui(self):
        main = ttk.Frame(self.root)
        main.pack(fill="both", expand=True)

        top_frame = ttk.Frame(main)
        top_frame.pack(fill="x", pady=15)

        button_container = ttk.Frame(top_frame)
        button_container.pack(anchor="center")

        ttk.Button(button_container, text="開始", command=self.start).pack(side="left", padx=10)
        ttk.Button(button_container, text="停止", command=self.stop).pack(side="left", padx=10)

        self.bottom_frame = tk.Frame(main, bg="#ffffff")
        self.bottom_frame.pack(fill="both", expand=True)

    # ================= 制御 =================

    def start(self):
        if self.running:
            return
        self.running = True
        self.loop_breathing()

    def stop(self):
        self.running = False
        self.set_color(0)

    # ================= 呼吸ループ =================

    def loop_breathing(self):
        if not self.running:
            return
        self.fade_in()

    # ================= フェード処理 =================

    def fade_in(self):
        half_steps = self.fade_steps // 2
        interval = self.fade_duration // self.fade_steps

        def step_in(step=0):
            if not self.running:
                self.set_color(0)
                return

            ratio = step / half_steps
            self.set_color(ratio)

            if step < half_steps:
                self.root.after(interval, step_in, step + 1)
            else:
                # フェードイン完了 → 保持
                self.root.after(self.post_fade_wait, self.fade_out)

        step_in()

    def fade_out(self):
        half_steps = self.fade_steps // 2
        interval = self.fade_duration // self.fade_steps

        def step_out(step=0):
            if not self.running:
                self.set_color(0)
                return

            ratio = 1 - (step / half_steps)
            self.set_color(ratio)

            if step < half_steps:
                self.root.after(interval, step_out, step + 1)
            else:
                # 呼吸終了 → 次の呼吸まで待機
                self.root.after(self.interval_between, self.loop_breathing)

        step_out()

    # ================= 色制御 =================

    def set_color(self, ratio):
        r_base, g_base, b_base = self.base_color

        r = int(255 - (255 - r_base) * ratio)
        g = int(255 - (255 - g_base) * ratio)
        b = int(255 - (255 - b_base) * ratio)

        color = f"#{r:02x}{g:02x}{b:02x}"
        self.bottom_frame.configure(bg=color)


if __name__ == "__main__":
    root = tk.Tk()
    app = BreathingApp(root)
    root.mainloop()