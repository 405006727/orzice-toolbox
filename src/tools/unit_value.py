import tkinter as tk
from tkinter import ttk, messagebox


def build(parent, feature, host):
    frame = ttk.Frame(parent, padding=16)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="物品单格价值计算器", font=("", 13, "bold")).pack(anchor="w")
    ttk.Label(frame, text="输入物品交易行总价与背包占格数，计算每一格的平均价值。", foreground="#555").pack(anchor="w", pady=(4, 12))

    form = ttk.Frame(frame)
    form.pack(fill="x")

    ttk.Label(form, text="物品总价（科恩币）").grid(row=0, column=0, sticky="w", pady=6)
    price_var = tk.StringVar()
    ttk.Entry(form, textvariable=price_var, width=22).grid(row=0, column=1, padx=12, pady=6)

    ttk.Label(form, text="背包占格数").grid(row=1, column=0, sticky="w", pady=6)
    slots_var = tk.StringVar()
    ttk.Entry(form, textvariable=slots_var, width=22).grid(row=1, column=1, padx=12, pady=6)

    result_var = tk.StringVar(value="单格价值：—")
    ttk.Label(frame, textvariable=result_var, font=("", 12, "bold")).pack(anchor="w", pady=(16, 4))
    hint_var = tk.StringVar()
    ttk.Label(frame, textvariable=hint_var, foreground="#555").pack(anchor="w")

    def calc():
        try:
            price = float(price_var.get().replace(",", "").strip())
            slots = float(slots_var.get().strip())
            if slots <= 0:
                raise ValueError
            unit = price / slots
            result_var.set(f"单格价值：{unit:,.0f} 币 / 格")
            if unit >= 20000:
                hint_var.set("单格价值很高，属于高性价比搬运物。")
            elif unit >= 8000:
                hint_var.set("单格价值中等，可根据行情选择搬运。")
            else:
                hint_var.set("单格价值偏低，搬运收益一般。")
        except ValueError:
            messagebox.showwarning("输入有误", "请填写有效的总价与大于 0 的占格数。")

    ttk.Button(frame, text="计算单格价值", command=calc).pack(anchor="w", pady=(12, 0))
    return frame
