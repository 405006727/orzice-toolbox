import tkinter as tk
from tkinter import ttk

MORSE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
    "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
    "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
    ".": ".-.-.-", ",": "--..--", "?": "..--..", "'": ".----.", "!": "-.-.--",
    "/": "-..-.", "(": "-.--.", ")": "-.--.-", "&": ".-...", ":": "---...",
    ";": "-.-.-.", "=": "-...-", "+": ".-.-.", "-": "-....-", "_": "..--.-",
    "\"": ".-..-.", "@": ".--.-.",
}
REV = {v: k for k, v in MORSE.items()}


def encode(text):
    return " ".join(MORSE.get(ch, "?") for ch in text.upper())


def decode(code):
    return "".join(REV.get(tok, "�") for tok in code.replace("/", " ").split())


def build(parent, feature, host):
    frame = ttk.Frame(parent, padding=16)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="文本 → 摩斯", font=("", 11, "bold")).pack(anchor="w")
    src = tk.Text(frame, height=4, wrap="word")
    src.pack(fill="x", pady=(4, 8))

    ttk.Label(frame, text="摩斯 → 文本（单词间用 / 分隔）", font=("", 11, "bold")).pack(anchor="w")
    morse_out = tk.Text(frame, height=4, wrap="word")
    morse_out.pack(fill="x", pady=(4, 8))

    def do_encode():
        morse_out.delete("1.0", "end")
        morse_out.insert("1.0", encode(src.get("1.0", "end").strip()))

    def do_decode():
        src.delete("1.0", "end")
        src.insert("1.0", decode(morse_out.get("1.0", "end").strip()))

    bar = ttk.Frame(frame)
    bar.pack(fill="x", pady=4)
    ttk.Button(bar, text="编码为摩斯", command=do_encode).pack(side="left", padx=(0, 8))
    ttk.Button(bar, text="解码摩斯", command=do_decode).pack(side="left")

    ttk.Label(frame, text="对照码表", font=("", 11, "bold")).pack(anchor="w", pady=(12, 4))
    cols = ("char", "code")
    table = ttk.Treeview(frame, columns=cols, show="headings", height=10)
    table.heading("char", text="字符")
    table.heading("code", text="摩斯")
    table.column("char", width=100)
    table.column("code", width=160)
    for ch, code in MORSE.items():
        if len(ch) == 1 and ch.isalnum():
            table.insert("", "end", values=(ch, code))
    table.pack(fill="both", expand=True)
    return frame
