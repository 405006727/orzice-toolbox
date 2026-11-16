import json
import sys
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox

from . import launcher
from .tools import doors, morse, unit_value

ROOT = Path(__file__).resolve().parent.parent


def _resource(rel: str) -> Path:
    base = Path(getattr(sys, "_MEIPASS", ROOT))
    return base / rel


DATA_FILE = _resource("data/features.json")

LOCAL_BUILDERS = {
    "doors": doors.build,
    "morse": morse.build,
    "item_jz": unit_value.build,
}

ACCENT = "#1f6feb"
BG_SIDEBAR = "#f1f4f8"


class OrziceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        self.host = self.data["site"]["host"].rstrip("/")
        self.title(f"{self.data['site']['name']} · Windows 工具箱")
        self.geometry("1120x760")
        self.minsize(960, 620)
        self.selected = None
        self._build_layout()
        self._build_sidebar("")
        self.show_home()

    def _build_layout(self):
        self.paned = ttk.Panedwindow(self, orient="horizontal")
        self.paned.pack(fill="both", expand=True)

        self.sidebar = tk.Frame(self.paned, width=280, bg=BG_SIDEBAR)
        self.paned.add(self.sidebar, weight=0)

        right = ttk.Frame(self.paned)
        self.paned.add(right, weight=1)

        self.header = ttk.Frame(right, padding=(18, 14, 18, 6))
        self.header.pack(fill="x")
        self.title_var = tk.StringVar(value=self.data["site"]["name"])
        self.desc_var = tk.StringVar(value=self.data["site"]["description"])
        ttk.Label(self.header, textvariable=self.title_var, font=("", 15, "bold")).pack(anchor="w")
        ttk.Label(self.header, textvariable=self.desc_var, foreground="#555", wraplength=640, justify="left").pack(anchor="w", pady=(4, 0))

        self.body = ttk.Frame(right, padding=(18, 8, 18, 8))
        self.body.pack(fill="both", expand=True)

        self.status = ttk.Label(self, text=self.data["site"]["notice"], foreground="#777", padding=(12, 4))
        self.status.pack(fill="x", side="bottom")

        search_wrap = tk.Frame(self.sidebar, bg=BG_SIDEBAR, padx=12, pady=6)
        search_wrap.pack(fill="x")
        ttk.Label(search_wrap, text="功能搜索", background=BG_SIDEBAR).pack(anchor="w")
        self.search_var = tk.StringVar()
        entry = ttk.Entry(search_wrap, textvariable=self.search_var)
        entry.pack(fill="x", pady=(4, 0))
        entry.bind("<KeyRelease>", lambda _e: self._build_sidebar(self.search_var.get().strip().lower()))

        self.side_canvas = tk.Canvas(self.sidebar, bg=BG_SIDEBAR, highlightthickness=0)
        self.side_scroll = ttk.Scrollbar(self.sidebar, orient="vertical", command=self.side_canvas.yview)
        self.side_inner = tk.Frame(self.side_canvas, bg=BG_SIDEBAR)
        self.side_inner.bind("<Configure>", lambda e: self.side_canvas.configure(scrollregion=self.side_canvas.bbox("all")))
        self.side_canvas.create_window((0, 0), window=self.side_inner, anchor="nw")
        self.side_canvas.configure(yscrollcommand=self.side_scroll.set)
        self.side_canvas.pack(side="left", fill="both", expand=True, padx=(12, 0))
        self.side_scroll.pack(side="right", fill="y")

    def _flat_features(self):
        items = []
        for cat in self.data["categories"]:
            for f in cat["features"]:
                items.append((cat["name"], f))
        for f in self.data.get("local_tools", []):
            items.append(("本地工具", {**f, "kind": "local", "url": ""}))
        return items

    def _build_sidebar(self, keyword):
        for w in self.side_inner.winfo_children():
            w.destroy()

        by_cat = {}
        for cat_name, f in self._flat_features():
            if keyword and keyword not in f["name"].lower() and keyword not in f["id"].lower():
                continue
            by_cat.setdefault(cat_name, []).append(f)

        row = 0
        for cat_name, features in by_cat.items():
            ttk.Label(self.side_inner, text=cat_name, background=BG_SIDEBAR, font=("", 10, "bold")).grid(
                row=row, column=0, sticky="w", padx=4, pady=(10, 2)
            )
            row += 1
            for f in features:
                btn = tk.Button(
                    self.side_inner,
                    text=f["name"],
                    anchor="w",
                    relief="flat",
                    bg="#ffffff",
                    activebackground="#e8f1ff",
                    font=("", 10),
                    padx=14,
                    pady=5,
                    command=lambda feat=f: self._open_feature(feat),
                )
                btn.grid(row=row, column=0, sticky="ew", padx=10, pady=2)
                self.side_inner.columnconfigure(0, weight=1)
                row += 1

    def _clear_body(self):
        for w in self.body.winfo_children():
            w.destroy()

    def _open_feature(self, feature):
        self.selected = feature
        self.title_var.set(feature["name"])
        self.desc_var.set(feature.get("desc", ""))
        self._clear_body()

        if feature["id"] in LOCAL_BUILDERS:
            LOCAL_BUILDERS[feature["id"]](self.body, feature, self.host)
        else:
            self._render_web_card(feature)

    def _render_web_card(self, feature):
        url = self.host + feature["url"]
        card = ttk.LabelFrame(self.body, text="在线功能", padding=16)
        card.pack(fill="x")

        ttk.Label(card, text="数据取自原站实时交易行 / 攻略内容，客户端不缓存行情数据。", foreground="#555").pack(anchor="w")
        ttk.Label(card, text=f"地址：{url}", foreground=ACCENT, wraplength=620).pack(anchor="w", pady=(8, 12))

        bar = ttk.Frame(card)
        bar.pack(anchor="w")
        ttk.Button(bar, text="在浏览器打开", command=lambda: launcher.open_url(url)).pack(side="left", padx=(0, 8))

        def copy_link():
            self.body.clipboard_clear()
            self.body.clipboard_append(url)
            messagebox.showinfo("已复制", "链接已复制到剪贴板。")

        ttk.Button(bar, text="复制链接", command=copy_link).pack(side="left")

    def show_home(self):
        self._clear_body()
        self.title_var.set(self.data["site"]["name"])
        self.desc_var.set(self.data["site"]["description"])
        home = ttk.LabelFrame(self.body, text="站点概览", padding=16)
        home.pack(fill="both", expand=True)
        total = sum(len(c["features"]) for c in self.data["categories"])
        ttk.Label(home, text=f"共 {len(self.data['categories'])} 个分类、{total} 项在线功能，另附本地小工具。", font=("", 11)).pack(anchor="w")
        ttk.Label(home, text="在左侧选择分类与功能项；标注「本地」的工具在客户端内直接运行，其余功能直达原站对应页面。", foreground="#555", wraplength=620).pack(anchor="w", pady=(8, 0))
        ttk.Button(home, text="打开原站首页", command=lambda: launcher.open_url(self.host)).pack(anchor="w", pady=(14, 0))


def main():
    app = OrziceApp()
    app.mainloop()


if __name__ == "__main__":
    main()
