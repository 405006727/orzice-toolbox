import tkinter as tk
from tkinter import ttk, messagebox

from .. import site


def build(parent, feature, host):
    frame = ttk.Frame(parent, padding=16)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="今日密码门", font=("", 13, "bold")).pack(anchor="w")
    status_var = tk.StringVar(value="正在获取今日密码…")
    ttk.Label(frame, textvariable=status_var, foreground="#555").pack(anchor="w", pady=(4, 12))

    cards = ttk.Frame(frame)
    cards.pack(fill="x")

    card_widgets = []

    def render(doors, update):
        for w in card_widgets:
            w.destroy()
        card_widgets.clear()
        for i, item in enumerate(doors):
            box = ttk.LabelFrame(cards, text=item["map"], padding=10)
            box.grid(row=i // 3, column=i % 3, padx=8, pady=8, sticky="nsew")
            card_widgets.append(box)
            pwd = item["password"]
            ttk.Label(box, text=pwd, font=("Consolas", 18, "bold")).pack(anchor="w")

            def copy_pwd(value=pwd):
                frame.clipboard_clear()
                frame.clipboard_append(value)

            ttk.Button(box, text="复制密码", command=copy_pwd).pack(anchor="w", pady=(6, 0))
        for col in range(3):
            cards.columnconfigure(col, weight=1)
        status_var.set(f"更新日期：{update or '未知'}　数据取自原站首页，每日 0 点后更新。")

    def refresh():
        try:
            doors, update = site.fetch_doors()
            render(doors, update)
        except Exception as exc:
            messagebox.showerror("获取失败", f"无法连接原站：{exc}")

    ttk.Button(frame, text="刷新密码", command=refresh).pack(anchor="w", pady=(0, 12))
    refresh()
    return frame
