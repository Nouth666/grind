from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config


def main_menu_kb(user_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="📖 Описание курса", callback_data="menu:description")
    kb.button(text="⭐ Отзывы", callback_data="menu:reviews")
    kb.button(text="💳 Оплата", callback_data="menu:payment")
    kb.adjust(1)
    if user_id in config.ADMIN_IDS:
        kb.button(text="⚙️ Админ-панель", callback_data="admin:menu")
        kb.adjust(1)
    return kb.as_markup()


def back_kb(target: str = "menu:main") -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ Назад", callback_data=target)
    return kb.as_markup()


def payment_kb(url: str, button_text: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=button_text, url=url)
    kb.button(text="⬅️ Назад", callback_data="menu:main")
    kb.adjust(1)
    return kb.as_markup()


def reviews_nav_kb(index: int, total: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if total > 1:
        kb.button(text="◀️", callback_data=f"reviews:{(index - 1) % total}")
        kb.button(text=f"{index + 1}/{total}", callback_data="noop")
        kb.button(text="▶️", callback_data=f"reviews:{(index + 1) % total}")
    kb.button(text="⬅️ В меню", callback_data="menu:main")
    kb.adjust(3, 1) if total > 1 else kb.adjust(1)
    return kb.as_markup()


def admin_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="✏️ Изменить описание", callback_data="admin:edit_description")
    kb.button(text="💳 Изменить ссылку оплаты", callback_data="admin:edit_payment_link")
    kb.button(text="🔘 Изменить текст кнопки оплаты", callback_data="admin:edit_payment_button")
    kb.button(text="📝 Изменить текст под оплатой", callback_data="admin:edit_payment_text")
    kb.button(text="➕ Добавить отзыв", callback_data="admin:add_review")
    kb.button(text="🗂 Список отзывов / удалить", callback_data="admin:list_reviews")
    kb.button(text="📢 Рассылка", callback_data="admin:broadcast")
    kb.button(text="📊 Статистика", callback_data="admin:stats")
    kb.button(text="⬅️ В главное меню", callback_data="menu:main")
    kb.adjust(1)
    return kb.as_markup()


def confirm_broadcast_kb(recipients: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=f"✅ Отправить всем ({recipients})", callback_data="admin:broadcast_confirm")
    kb.button(text="❌ Отмена", callback_data="admin:menu")
    kb.adjust(1)
    return kb.as_markup()


def cancel_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="❌ Отмена", callback_data="admin:menu")
    return kb.as_markup()


def review_delete_kb(index: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=f"🗑 Удалить отзыв #{index + 1}", callback_data=f"admin:del_review:{index}")
    return kb.as_markup()
