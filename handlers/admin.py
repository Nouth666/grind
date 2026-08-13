from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

import config
import keyboards as kb
from storage import add_review, delete_review, get_content, update_content

router = Router(name="admin")
router.message.filter(F.from_user.id.in_(config.ADMIN_IDS))
router.callback_query.filter(F.from_user.id.in_(config.ADMIN_IDS))


class AdminStates(StatesGroup):
    editing_description = State()
    editing_payment_link = State()
    editing_payment_button = State()
    editing_payment_text = State()
    adding_review = State()


@router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("⚙️ <b>Админ-панель Grind University</b>", reply_markup=kb.admin_menu_kb())


@router.callback_query(F.data == "admin:menu")
async def cb_admin_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.delete()
    await callback.bot.send_message(
        callback.message.chat.id,
        "⚙️ <b>Админ-панель Grind University</b>",
        reply_markup=kb.admin_menu_kb(),
    )


@router.callback_query(F.data == "admin:edit_description")
async def cb_edit_description(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(AdminStates.editing_description)
    await callback.message.edit_text(
        "Пришли новый текст описания курса (можно с HTML-разметкой: <b>жирный</b>, <i>курсив</i>).",
        reply_markup=kb.cancel_kb(),
    )


@router.message(AdminStates.editing_description)
async def save_description(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Нужен текст. Попробуй ещё раз.")
        return
    update_content(description=message.text)
    await state.clear()
    await message.answer("✅ Описание обновлено.", reply_markup=kb.admin_menu_kb())


@router.callback_query(F.data == "admin:edit_payment_link")
async def cb_edit_payment_link(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(AdminStates.editing_payment_link)
    await callback.message.edit_text(
        "Пришли новую ссылку на оплату (например, ссылку Tribute).",
        reply_markup=kb.cancel_kb(),
    )


@router.message(AdminStates.editing_payment_link)
async def save_payment_link(message: Message, state: FSMContext):
    link = (message.text or "").strip()
    if not link.startswith("http"):
        await message.answer("Это не похоже на ссылку. Пришли ссылку, начинающуюся с http(s)://")
        return
    update_content(payment_link=link)
    await state.clear()
    await message.answer("✅ Ссылка на оплату обновлена.", reply_markup=kb.admin_menu_kb())


@router.callback_query(F.data == "admin:edit_payment_button")
async def cb_edit_payment_button(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(AdminStates.editing_payment_button)
    await callback.message.edit_text(
        "Пришли новый текст для кнопки оплаты (например: «💳 Оплатить курс»).",
        reply_markup=kb.cancel_kb(),
    )


@router.message(AdminStates.editing_payment_button)
async def save_payment_button(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Нужен текст. Попробуй ещё раз.")
        return
    update_content(payment_button_text=message.text)
    await state.clear()
    await message.answer("✅ Текст кнопки обновлён.", reply_markup=kb.admin_menu_kb())


@router.callback_query(F.data == "admin:edit_payment_text")
async def cb_edit_payment_text(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(AdminStates.editing_payment_text)
    await callback.message.edit_text(
        "Пришли новый текст, который показывается на вкладке «Оплата» (над кнопкой).",
        reply_markup=kb.cancel_kb(),
    )


@router.message(AdminStates.editing_payment_text)
async def save_payment_text(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Нужен текст. Попробуй ещё раз.")
        return
    update_content(payment_text=message.text)
    await state.clear()
    await message.answer("✅ Текст вкладки «Оплата» обновлён.", reply_markup=kb.admin_menu_kb())


@router.callback_query(F.data == "admin:add_review")
async def cb_add_review(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(AdminStates.adding_review)
    await callback.message.edit_text(
        "Пришли отзыв: текстом или фото (скриншот) с подписью.",
        reply_markup=kb.cancel_kb(),
    )


@router.message(AdminStates.adding_review, F.photo)
async def save_review_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    add_review(kind="photo", text=message.caption, file_id=file_id)
    await state.clear()
    await message.answer("✅ Отзыв (фото) добавлен.", reply_markup=kb.admin_menu_kb())


@router.message(AdminStates.adding_review, F.text)
async def save_review_text(message: Message, state: FSMContext):
    add_review(kind="text", text=message.text)
    await state.clear()
    await message.answer("✅ Отзыв добавлен.", reply_markup=kb.admin_menu_kb())


@router.callback_query(F.data == "admin:list_reviews")
async def cb_list_reviews(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    content = get_content()
    reviews = content["reviews"]
    await callback.message.delete()
    if not reviews:
        await callback.bot.send_message(
            callback.message.chat.id,
            "Отзывов пока нет.",
            reply_markup=kb.admin_menu_kb(),
        )
        return
    for i, review in enumerate(reviews):
        if review["type"] == "photo":
            await callback.bot.send_photo(
                callback.message.chat.id,
                review["file_id"],
                caption=review.get("text") or None,
                reply_markup=kb.review_delete_kb(i),
            )
        else:
            await callback.bot.send_message(
                callback.message.chat.id,
                review["text"],
                reply_markup=kb.review_delete_kb(i),
            )
    await callback.bot.send_message(
        callback.message.chat.id,
        "Это все отзывы.",
        reply_markup=kb.admin_menu_kb(),
    )


@router.callback_query(F.data.startswith("admin:del_review:"))
async def cb_delete_review(callback: CallbackQuery):
    index = int(callback.data.split(":")[2])
    delete_review(index)
    await callback.answer("Отзыв удалён 🗑")
    try:
        await callback.message.delete()
    except Exception:
        pass
