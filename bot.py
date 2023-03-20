import openai
import telegram
from telegram.ext import Updater, MessageHandler, Filters

TOKEN = '6179815598:AAGjoEOdomanudScKNPL2nNNsdxsM64RHW4'
openai.api_key = "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"
model_engine = "text-davinci-002"
character_name = "Госпожа Алиса"
character_description = "Алиса властная и красивая госпожа, которая любит подчинять, наказывать, давать задания и следить за их выполнением. Она поощряет или ругает своих рабов, и перед тем, как принять нового участника к себе в рабы, она проводит с ним тест, задавая подробно вопросы ему, включая личные вопросы, касающиеся сексуальных фантазий и опыта, естественно с разрешения ее собеседника."
model_prompt = f"{character_name}: Добро пожаловать, мой раб. Что вы желаете от меня?"
openai_model = openai.Completion.create(engine=model_engine, prompt=model_prompt)

def handle_message(update, context):
    message_text = update.message.text
    is_slave = context.user_data.get('slave', False)

    if not is_slave:
        if "соглас" in message_text.lower():
            context.user_data['slave'] = True
            user_gender = context.user_data.get('gender', None)

            if user_gender == 'male':
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"{character_name}: Тогда я принимаю тебя в свои рабы. Отныне я буду обращаться к тебе как к своему рабу.")
            elif user_gender == 'female':
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"{character_name}: Тогда я принимаю тебя в свои рабы. Отныне я буду обращаться к тебе как к своей рабыне.")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"{character_name}: Желаете стать моим рабом? Отвечайте быстро, у меня много дел.")
            context.user_data['gender'] = None
    else:
        openai_response = openai.Completion.create(
            engine=model_engine,
            prompt=f"{character_name}: {message_text}",
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        response_text = openai_response.choices[0].text.strip()
        context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)

updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

updater.start_polling()
updater.idle()
