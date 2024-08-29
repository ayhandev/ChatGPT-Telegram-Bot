import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv
import httpx
import asyncio


load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHATGPT_API_URL = 'https://api.openai.com/v1/chat/completions'
CHATGPT_API_KEY = os.getenv('CHATGPT_API_KEY')
BOT_NAME = os.getenv('BOT_NAME')
SUPPORT_USERNAME = os.getenv('SUPPORT_USERNAME')


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


async def send_to_chatgpt(message: str) -> str:
    headers = {
        'Authorization': f'Bearer {CHATGPT_API_KEY}',
        'Content-Type': 'application/json',
    }
    data = {
        'model': 'gpt-3.5-turbo',  
        'messages': [{'role': 'user', 'content': message}],
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(CHATGPT_API_URL, headers=headers, json=data)
            response.raise_for_status()  
            chatgpt_response = response.json()
            return chatgpt_response['choices'][0]['message']['content']
        except httpx.HTTPStatusError as e:
            if response.status_code == 429:
                logger.error("Ошибка 429: Превышена квота API. Попробуйте позже.")
                return "В данный момент бот перегружен. Попробуйте позже."
            elif response.status_code == 404:
                logger.error("Ошибка 404: Неправильный URL или ресурс не найден.")
                return "Произошла ошибка при обработке вашего запроса: ресурс не найден."
            else:
                logger.error(f"Ошибка при запросе к боту: {e}")
                return "Произошла ошибка при обработке вашего запроса."
        except httpx.RequestError as e:
            logger.error(f"Ошибка при запросе к боту: {e}")
            return "Произошла ошибка при обработке вашего запроса."



async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f'Привет! Я бот {BOT_NAME}. Напиши мне что-нибудь.')


async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f'Для получения помощи обратитесь к техподдержке: @{SUPPORT_USERNAME}')


async def show_progress_bar(update: Update, context: CallbackContext, message_id: int, progress: int, old_text: str) -> None:
    bars = '🟩' * progress + '⬜' * (5 - progress)
    new_text = f'{bars} ({progress * 20}%)'
    if new_text != old_text:
        try:
            await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=message_id, text=new_text)
        except Exception as e:
            logger.error(f"Ошибка при обновлении сообщения: {e}")


async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text.lower()
    message = await update.message.reply_text('🟩⬜⬜⬜⬜ (20%)')
    message_id = message.message_id

    if user_message == 'кто ты?' or user_message == 'кто ты':
        response = 'Я проект независимых энтузиастов'
        await show_progress_bar(update, context, message_id, 5, '🟩⬜⬜⬜⬜ (20%)')
        await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=message_id, text=response)
    else:
        await show_progress_bar(update, context, message_id, 1, '🟩⬜⬜⬜⬜ (20%)')
        await asyncio.sleep(2) 
        await show_progress_bar(update, context, message_id, 3, '🟩⬜⬜⬜⬜ (20%)')
        await asyncio.sleep(2)  
        await show_progress_bar(update, context, message_id, 5, '🟩⬜⬜⬜⬜ (20%)')


        response = await send_to_chatgpt(user_message)
        

        try:
            await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=message_id, text=response)
        except Exception as e:
            logger.error(f"Ошибка при обновлении сообщения: {e}")


def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


    application.run_polling()

if __name__ == '__main__':
    main()
