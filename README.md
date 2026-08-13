# Grind University — Telegram-бот

Бот для продажи курса «Grind University»: разделы «Описание», «Отзывы», «Оплата»
и админ-панель прямо в боте (без отдельного сайта).

## Возможности

- 📖 **Описание** — текст курса, редактируется из админки.
- ⭐ **Отзывы** — текстовые и фото-отзывы (скриншоты), с пролистыванием ◀️▶️.
- 💳 **Оплата** — текст + кнопка со ссылкой на оплату (по умолчанию Tribute:
  `https://t.me/tribute/app?startapp=s13bX`).
- ⚙️ **Админ-панель** (`/admin`, доступна только твоему Telegram ID):
  - изменить текст описания;
  - изменить ссылку на оплату;
  - изменить текст и подпись кнопки оплаты;
  - добавлять/удалять отзывы (текст или фото).

Все данные хранятся в `content.json` рядом с ботом — редактировать руками не нужно,
всё меняется через диалог с ботом в Telegram.

## Установка

1. Создай бота через [@BotFather](https://t.me/BotFather) и получи токен.
2. Узнай свой Telegram ID через [@userinfobot](https://t.me/userinfobot).
3. Скопируй `.env.example` в `.env` и заполни:

   ```
   BOT_TOKEN=твой_токен_от_botfather
   ADMIN_IDS=твой_telegram_id
   ```

   Можно указать несколько админов через запятую: `ADMIN_IDS=111,222`.

4. Установи зависимости:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

5. Запусти бота:

   ```bash
   python bot.py
   ```

6. В Telegram напиши боту `/start` — увидишь главное меню. Как админ, напиши `/admin`
   (или нажми кнопку «⚙️ Админ-панель» в главном меню) — откроется панель управления.

## Деплой (чтобы бот работал постоянно)

Проще всего — арендовать дешёвый VPS (например, Timeweb, Selectel, Beget, Hetzner)
и запустить бота там через `systemd` или `screen`/`tmux`, либо в Docker. Бот работает
через long polling, отдельный домен/HTTPS не нужен.

Пример автозапуска через systemd (`/etc/systemd/system/grind-bot.service`):

```ini
[Unit]
Description=Grind University Telegram Bot
After=network.target

[Service]
WorkingDirectory=/path/to/grind-university-bot
ExecStart=/path/to/grind-university-bot/.venv/bin/python bot.py
Restart=always
User=youruser

[Install]
WantedBy=multi-user.target
```

Затем:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now grind-bot
```

## Структура проекта

```
grind-university-bot/
├── bot.py            # точка входа
├── config.py         # чтение токена и списка админов из .env
├── storage.py         # чтение/запись content.json
├── content.json       # текущее содержимое (описание, оплата, отзывы)
├── keyboards.py        # инлайн-клавиатуры
├── handlers/
│   ├── user.py         # меню, описание, отзывы, оплата
│   └── admin.py         # админ-панель (FSM-диалоги редактирования)
├── requirements.txt
└── .env.example
```
