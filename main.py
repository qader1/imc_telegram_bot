from telegram.ext import Updater, CommandHandler
from datetime import date, timedelta, datetime
from APIs import *
from schedule import *
from reddit_api import *

# IMPORTANT: two updaters running -the class the receives bot updates- will probably not work
###########
# reddit and calendar functions won't work because of Oauth2.
# basically reddit API and google calendar API,
# require authorization from user to access their account
# in reddit there is no way around it. I didn't try with google's
###########
# I didn't upload my credentials but I uploaded the token.
# I made comments in parts of code that I thought need clarifying


def weather(update, context):
    chat_id = update.effective_chat.id
    arg = context.args[0]
    if arg == 'today':
        today = date.today().isoformat()
        w = get_weather(today)
    elif arg == 'tomorrow':
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        w = get_weather(tomorrow)
    else:
        w = get_weather(arg)
    if type(w) == str:
        context.bot.send_message(chat_id, w)
    else:
        for i in range(len(w)):
            context.bot.send_message(chat_id, w[i])
    save(update)


def q(update, context):
    user_name = update.message['chat']['first_name']
    quote = get_quote()
    text = f'"{quote[0]}"\n\n{quote[1]}'
    if user_name is not None:
        text = f'for you {user_name}!\n"{quote[0]}"\n\n{quote[1]}'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    save(update)


def advice(update, context):
    chat_id = update.effective_chat.id
    user_name = update.message['chat']['first_name']
    text = f'here\'s your advice!\n\n"{get_advice()}"'
    if user_name is not None:
        text = f'here\'s your advice {user_name}!\n\n"{get_advice()}"'
    context.bot.send_message(chat_id=chat_id, text=text)
    save(update)


def dog(update, context):
    url = get_dog()
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=url)
    save(update)


def hi(update, context):
    chat_id = update.effective_chat.id
    user_name = update.message['chat']['first_name']
    context.bot.send_message(chat_id=chat_id, text=f'welcome {user_name}')
    context.bot.send_message(chat_id=chat_id, text=f'I\'m a bot\nblip blop I\'m a robot 🤖')
    context.bot.send_message(chat_id=chat_id, text=f'press "/" to see the list of my current commands (more could come)')
    save(update)


def reddit(update, context):
    chat_id = update.effective_chat.id
    args = context.args
    result = get_reddit(*args)
    if type(result) == str:
        context.bot.send_photo(chat_id=chat_id, photo=result)
    else:
        context.bot.send_message(chat_id=chat_id,
                                 text=f'{result[0]}\n{result[1]}')
    save(update)


def schedule(update, context):
    chat_id = update.effective_chat.id
    arg = context.args[0]
    result = get_schedule(arg)
    if type(result) == str:
        context.bot.send_message(chat_id, result)
    else:
        for i in range(len(result)):
            string = result[i][0] + '\n' + result[i][1]
            context.bot.send_message(chat_id, string)
    save(update)


def save(update):
    chat_id = update.effective_chat.id
    user_name = update.message['chat']['first_name']
    text = update['message']['text']
    now = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    with open('history.csv', 'a+') as f:
        f.write(f'{now},{chat_id},{user_name},{text}\n')


def main():

    """the updater identifies the bot with the bot token
    the bot probably won't run if two updaters are running
    on two different machines

    updater class: receives the bot updates
    dispatcher class: used to handle bot events
    command functions: each function is passed two arguments by the dispatcher, context and update
                       context and update have all the information about the user or group, message id
                       and arguments passed after the command in the bot
    """

    bot = '1182377175:AAFOx_MF2ILQZ4eMcTql9ytD1mShJaZT1Ac'
    updater = Updater(bot, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('dog', dog))
    dp.add_handler(CommandHandler('start', hi))
    dp.add_handler(CommandHandler('advice', advice))
    dp.add_handler(CommandHandler('weather', weather))
    dp.add_handler(CommandHandler('quote', q))
    dp.add_handler(CommandHandler('schedule', schedule))
    dp.add_handler(CommandHandler('reddit', reddit))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

