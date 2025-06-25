from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import pandas as pd
import os

# 📄 Укажи путь к PDF-файлу, который бот будет отправлять
PDF_FILE_PATH = 'promo.pdf'

# 📋 Список подписчиков
subscribers = []

# 📍 Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📩 Подписаться", callback_data='subscribe')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! 👋 Подпишись и получи полезный PDF-файл!",
        reply_markup=reply_markup
    )

# 📍 Обработка кнопки подписки
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'subscribe':
        user = query.from_user

        # Сохраняем пользователя
        subscribers.append({
            "ID": user.id,
            "Username": user.username,
            "Имя": user.first_name
        })

        # Отправка PDF-файла
        if os.path.exists(PDF_FILE_PATH):
            await query.message.reply_document(open(PDF_FILE_PATH, 'rb'), caption="📄 Вот ваш файл. Спасибо за подписку!")
        else:
            await query.message.reply_text("Файл PDF не найден. Пожалуйста, свяжитесь с админом.")

        # Сохраняем в Excel
        df = pd.DataFrame(subscribers)
        df.to_excel("subscribers.xlsx", index=False)

# 🚀 Запуск бота
if __name__ == '__main__':
    # 🔐 ТВОЙ ТОКЕН ВСТАВЛЕН СЮДА
    TOKEN = "7626564661:AAEcT-B1A00cx3BFhvmRrEhIoV3r7scr1rY"

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    print("✅ Бот запущен...")
    app.run_polling()
