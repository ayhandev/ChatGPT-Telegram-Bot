# ChatGPT Telegram Bot

## Description
This Telegram bot uses the ChatGPT API to communicate with users.

## Installation

1. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Create a .env file in the root of your project with your API keys. Example content of the .env file:

    ```env
    TELEGRAM_TOKEN=ваш_telegram_token
    CHATGPT_API_URL=https://api.openai.com/v1/chat/completions
    CHATGPT_API_KEY=ваш_openai_api_key
    BOT_NAME=KamskyAI 
    SUPPORT_USERNAME=kamsky00
    ```

## Running

Start the bot:

```bash
python bot.py
```