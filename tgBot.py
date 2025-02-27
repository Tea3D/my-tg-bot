import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.enums import ChatType

TOKEN = "7569085967:AAHMvPdfjOC-tVdKmKb8cIb7i6M0YHJO5-g"
FORBIDDEN_WORDS = {"@Timed3D_Tea3D", "@ILLKUS"}
USER_ID = 5570292124  # Замените на ID пользователя, которого нужно логировать
GROUP_ID = -1002385563310  # Замените на ID группы, в которой должен работать бот

bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

@dp.message()
async def log_messages(message: Message):
    if message.chat.type not in {ChatType.SUPERGROUP, ChatType.GROUP}:
        return

    if message.chat.id != GROUP_ID:
        return

    print(f"Сообщение от {message.from_user.id}: {message.text}")

    if message.from_user.id == USER_ID:
        with open("messages.log", "a", encoding="utf-8") as log_file:
            log_file.write(f"{message.from_user.id}: {message.text}\n")

    # Проверка на запрещенные слова
    if any(word in message.text for word in FORBIDDEN_WORDS):
        try:
            await bot.delete_message(message.chat.id, message.message_id)
            print(f"Удалено сообщение: {message.text}")
        except Exception as e:
            logging.warning(f"Не удалось удалить сообщение: {e}")
            print(f"Ошибка удаления: {e}")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
