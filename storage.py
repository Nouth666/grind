import json
import os
import threading

CONTENT_PATH = os.path.join(os.path.dirname(__file__), "content.json")

_lock = threading.Lock()

_DEFAULT_CONTENT = {
    "description": "🎓 <b>Grind University</b>\n\nОписание курса пока не заполнено.",
    "payment_link": "https://t.me/tribute/app?startapp=s13bX",
    "payment_button_text": "💳 Оплатить курс",
    "payment_text": "Чтобы получить доступ к курсу <b>Grind University</b>, нажми на кнопку ниже 👇",
    "reviews": [],
}


def _read() -> dict:
    if not os.path.exists(CONTENT_PATH):
        return dict(_DEFAULT_CONTENT)
    with open(CONTENT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    for key, value in _DEFAULT_CONTENT.items():
        data.setdefault(key, value)
    return data


def _write(data: dict) -> None:
    with open(CONTENT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_content() -> dict:
    with _lock:
        return _read()


def update_content(**fields) -> dict:
    with _lock:
        data = _read()
        data.update(fields)
        _write(data)
        return data


def add_review(kind: str, text: str | None = None, file_id: str | None = None) -> dict:
    with _lock:
        data = _read()
        data["reviews"].append({"type": kind, "text": text, "file_id": file_id})
        _write(data)
        return data


def delete_review(index: int) -> dict:
    with _lock:
        data = _read()
        if 0 <= index < len(data["reviews"]):
            data["reviews"].pop(index)
            _write(data)
        return data
