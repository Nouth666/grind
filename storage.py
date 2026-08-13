import json
import os
import threading
from datetime import datetime, timedelta

CONTENT_PATH = os.path.join(os.path.dirname(__file__), "content.json")
USERS_PATH = os.path.join(os.path.dirname(__file__), "users.json")

_lock = threading.Lock()
_users_lock = threading.Lock()

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


def _read_users() -> dict:
    if not os.path.exists(USERS_PATH):
        return {}
    with open(USERS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_users(users: dict) -> None:
    with open(USERS_PATH, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def track_user(user_id: int, username: str | None, first_name: str | None, action: str) -> None:
    """Запоминает пользователя (для рассылки) и считает его действия (для статистики)."""
    with _users_lock:
        users = _read_users()
        now = datetime.utcnow().isoformat()
        entry = users.get(str(user_id))
        if entry is None:
            entry = {
                "username": username,
                "first_name": first_name,
                "first_seen": now,
                "last_seen": now,
                "actions": {},
            }
        entry["username"] = username
        entry["first_name"] = first_name
        entry["last_seen"] = now
        entry["actions"][action] = entry["actions"].get(action, 0) + 1
        users[str(user_id)] = entry
        _write_users(users)


def get_all_user_ids() -> list[int]:
    with _users_lock:
        users = _read_users()
    return [int(uid) for uid in users.keys()]


def get_stats() -> dict:
    with _users_lock:
        users = _read_users()

    now = datetime.utcnow()
    new_today = 0
    new_7d = 0
    active_7d = 0
    actions_totals = {"start": 0, "description": 0, "reviews": 0, "payment": 0}

    for entry in users.values():
        first_seen = datetime.fromisoformat(entry["first_seen"])
        last_seen = datetime.fromisoformat(entry["last_seen"])
        if now - first_seen <= timedelta(days=1):
            new_today += 1
        if now - first_seen <= timedelta(days=7):
            new_7d += 1
        if now - last_seen <= timedelta(days=7):
            active_7d += 1
        for key in actions_totals:
            actions_totals[key] += entry.get("actions", {}).get(key, 0)

    return {
        "total_users": len(users),
        "new_today": new_today,
        "new_7d": new_7d,
        "active_7d": active_7d,
        "actions": actions_totals,
    }
