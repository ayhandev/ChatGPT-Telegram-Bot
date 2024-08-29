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
    TELEGRAM_TOKEN=telegram token
    CHATGPT_API_URL=https://api.openai.com/v1/chat/completions
    CHATGPT_API_KEY=OpenAI token
    BOT_NAME=KamskyAI 
    SUPPORT_USERNAME=Your Telegram nickname 
    ```

## Running

Start the bot:

```bash
python bot.py
```
