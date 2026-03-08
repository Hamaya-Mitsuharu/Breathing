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
        self.fade_duration = 3000
        self.fade_steps = 40
        self.post_fade_wait = 500
        self.interval_between = 500

        # --- カラー ---
        self.base_color = (190, 235, 180)

        # --- 画面端トリガー設定 ---
        self.edge_size = 20
        self.edge_cooldown = False

        # =======================

        self.root.title("Breathing App")
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        self.root.resizable(False, False)

        self.running = False

        self.create_ui()

        # 画面端監視開始
        self.monitor_edges()

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

    def toggle_breathing(self):
        if self.running:
            self.stop()
        else:
            self.start()

    # ================= 画面端トリガー =================

    def monitor_edges(self):
        x, y = self.root.winfo_pointerxy()

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        # 左上
        if x <= self.edge_size and y <= self.edge_size:
            if not self.edge_cooldown:
                self.edge_cooldown = True
                self.trigger_top_left()

        # 左下
        elif x <= self.edge_size and y >= screen_h - self.edge_size:
            if not self.edge_cooldown:
                self.edge_cooldown = True
                self.trigger_bottom_left()

        else:
            self.edge_cooldown = False

        self.root.after(50, self.monitor_edges)

    def trigger_top_left(self):
        # 最前面化
        self.root.deiconify()
        self.root.attributes("-topmost", True)
        self.root.lift()

        # 呼吸切替
        self.toggle_breathing()

    def trigger_bottom_left(self):
        self.root.iconify()

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