import json
import re
import ssl
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "features.json"

DOOR_MAPS = ["零号大坝", "长弓溪谷", "巴克什", "航天基地", "潮汐监狱", "AZ3"]
DOOR_FALLBACK = {
    "零号大坝": "2515",
    "长弓溪谷": "4857",
    "巴克什": "8009",
    "航天基地": "0257",
    "潮汐监狱": "0466",
    "AZ3": "2910",
}


def load_site():
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return data["site"]


def site_host():
    return load_site()["host"].rstrip("/")


def fetch_doors(timeout=8):
    host = site_host()
    req = urllib.request.Request(
        host + "/",
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    )
    ctx = ssl.create_default_context()
    html = urllib.request.urlopen(req, timeout=timeout, context=ctx).read().decode("utf-8", "ignore")
    doors = {}
    pattern = re.compile(r"(零号大坝|长弓溪谷|巴克什|航天基地|潮汐监狱|AZ3)[^\d]{0,160}?(\d{4})", re.S)
    for m in pattern.finditer(html):
        doors[m.group(1)] = m.group(2)
    date_match = re.search(r'hp-pwd-date">([0-9]{4}-[0-9]{2}-[0-9]{2})', html)
    if not date_match:
        date_match = re.search(r"更新日期[^\d]{0,60}?([0-9]{4}-[0-9]{2}-[0-9]{2})", html)
    update = date_match.group(1) if date_match else ""
    doors = {**DOOR_FALLBACK, **doors}
    return [{"map": k, "password": doors[k]} for k in DOOR_MAPS], update
