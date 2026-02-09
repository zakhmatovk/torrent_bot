import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Вставьте ваш токен, полученный от @BotFather в Telegram
TOKEN = os.environ['TORRENT_BOT_TOKEN']
WHITE_LIST = set(int(it) for it in os.environ['TORRENT_BOT_WHITE_LIST'].split(','))
TORRENT_DIR = os.environ['TORRENT_DIR']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    if update.message.chat_id not in WHITE_LIST:
        await update.message.reply_text(f'Привет! Твоего chat_id: {update.message.chat_id} нет в белом списке.')
        return
    await update.message.reply_text('Привет! Отправьте мне торрент-файл, и я сохраню его.')

async def receive_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Проверяем, что полученный файл является документом
    if not update.message:
        return
    if update.message.chat_id not in WHITE_LIST:
        await update.message.reply_text(f'Привет! Твоего chat_id: {update.message.chat_id} нет в белом списке.')
        return

    if update.message.document:
        file = update.message.document
        if file.file_name and file.file_name.endswith('.torrent'):
            new_file = await context.bot.get_file(file.file_id)
            os.makedirs(TORRENT_DIR, exist_ok=True)
            file_path = f'{TORRENT_DIR}/{file.file_name}'
            await new_file.download_to_drive(custom_path=file_path)
            await update.message.reply_text('Торрент-файл сохранён.')
        else:
            await update.message.reply_text('Пожалуйста, отправьте торрент-файл.')

def main():
    # Создаем приложение бота
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.Document.ALL, receive_file))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
