from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

import keyboards as kb
from storage import get_content, track_user

router = Router(name="user")


async def render_main_menu(chat_id: int, user_id: int, bot, edit: Message | None = None):
    text = "👋 Добро пожаловать в <b>Grind University</b>!\n\nВыбери раздел:"
    if edit is not None:
        try:
            await edit.delete()
        except Exception:
            pass
    await bot.send_message(chat_id, text, reply_markup=kb.main_menu_kb(user_id))


@router.message(CommandStart())
async def cmd_start(message: Message):
    track_user(message.from_user.id, message.from_user.username, message.from_user.first_name, "start")
    await render_main_menu(message.chat.id, message.from_user.id, message.bot)


@router.callback_query(F.data == "menu:main")
async def cb_main_menu(callback: CallbackQuery):
    await callback.answer()
    await render_main_menu(callback.message.chat.id, callback.from_user.id, callback.bot, edit=callback.message)


@router.callback_query(F.data == "menu:description")
async def cb_description(callback: CallbackQuery):
    await callback.answer()
    track_user(callback.from_user.id, callback.from_user.username, callback.from_user.first_name, "description")
    content = get_content()
    await callback.message.delete()
    await callback.bot.send_message(
        callback.message.chat.id,
        content["description"],
        reply_markup=kb.back_kb(),
    )


@router.callback_query(F.data == "menu:payment")
async def cb_payment(callback: CallbackQuery):
    await callback.answer()
    track_user(callback.from_user.id, callback.from_user.username, callback.from_user.first_name, "payment")
    content = get_content()
    await callback.message.delete()
    await callback.bot.send_message(
        callback.message.chat.id,
        content["payment_text"],
        reply_markup=kb.payment_kb(content["payment_link"], content["payment_button_text"]),
    )


async def send_review(chat_id: int, bot, index: int, reviews: list):
    review = reviews[index]
    markup = kb.reviews_nav_kb(index, len(reviews))
    if review["type"] == "photo":
        await bot.send_photo(chat_id, review["file_id"], caption=review.get("text") or None, reply_markup=markup)
    else:
        await bot.send_message(chat_id, review["text"], reply_markup=markup)


@router.callback_query(F.data == "menu:reviews")
async def cb_reviews(callback: CallbackQuery):
    await callback.answer()
    track_user(callback.from_user.id, callback.from_user.username, callback.from_user.first_name, "reviews")
    content = get_content()
    reviews = content["reviews"]
    await callback.message.delete()
    if not reviews:
        await callback.bot.send_message(
            callback.message.chat.id,
            "Пока нет отзывов 🙂",
            reply_markup=kb.back_kb(),
        )
        return
    await send_review(callback.message.chat.id, callback.bot, 0, reviews)


@router.callback_query(F.data.startswith("reviews:"))
async def cb_reviews_nav(callback: CallbackQuery):
    await callback.answer()
    index = int(callback.data.split(":")[1])
    content = get_content()
    reviews = content["reviews"]
    if not reviews:
        return
    index = index % len(reviews)
    await callback.message.delete()
    await send_review(callback.message.chat.id, callback.bot, index, reviews)


@router.callback_query(F.data == "noop")
async def cb_noop(callback: CallbackQuery):
    await callback.answer()


@router.message(Command("admin"))
async def cmd_admin_no_access(message: Message):
    # Обрабатывается admin-роутером для админов; если дошло сюда — доступа нет.
    await message.answer("⛔ У тебя нет доступа к админ-панели.")
