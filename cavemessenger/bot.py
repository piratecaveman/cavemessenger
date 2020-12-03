import random
import botogram
import pathlib
import os

from cavemessenger.transforms import Transformer
API_KEY = os.environ['API_KEY']


bot = botogram.create(API_KEY)
transformer = Transformer()


def read(name: str):
    name = pathlib.Path(__file__).parent / 'templates' / name
    with open(str(name), 'r') as file:
        contents = file.readlines()
    return contents


def get_names(message: botogram.Message) -> dict:
    names = {
        'sender_username': None,
        'sender_name': None,
        'linked_username': None,
        'linked_name': None
    }

    if message.sender:
        if message.sender.username:
            names['sender_username'] = f'@{message.sender.username}'
        if message.sender.name:
            names['sender_name'] = message.sender.name

    if message.reply_to_message:
        if message.reply_to_message.sender:
            if message.reply_to_message.sender.username:
                names['linked_username'] = f'@{message.reply_to_message.sender.username}'
            if message.reply_to_message.sender.name:
                names['linked_name'] = message.reply_to_message.sender.name

    return names


@bot.command('hello')
def hello(chat: botogram.Chat, message: botogram.Message):
    """Greetings in 21 languages"""
    greetings = read('greetings.txt')
    names = get_names(message)

    name = names['sender_username'] if names['sender_username'] else names['sender_name']
    if not name:
        name = 'Human'

    linked_name = names['linked_username'] if names['linked_username'] else names['linked_name']
    if not linked_name:
        linked_name = 'Another Human'

    number = random.randint(0, len(greetings) - 1)

    if message.reply_to_message:
        text = f'{greetings[number]} and {linked_name}'.replace('<name>', name)
    else:
        text = greetings[number].replace('<name>', name)
    chat.send(text)


@bot.command('insult')
def insult(chat: botogram.Chat, message: botogram.Message, args: list):
    """Don't be too harsh"""
    names = get_names(message)
    insults = read('insults.txt')
    number = random.randint(0, len(insults) - 1)
    insult = insults[number]

    name = names['sender_username'] if names['sender_username'] else names['sender_name']
    if name is None:
        name = 'Human'

    linked_name = names['linked_username'] if names['linked_username'] else names['linked_name']
    if linked_name is None:
        linked_name = 'Human'

    if args:
        args: str = args[0]
        if not args.startswith('@'):
            chat.send(f'You are too dumb to use a command properly {name}')
        else:
            if args == '@cavemessengerbot':
                chat.send(f'Only a dimwit like you would try to insult a bot {name}', reply_to=message.id)
            else:
                text = insult.replace('<name>', args)
                chat.send(f'{text}', reply_to=message.id)

    elif message.reply_to_message:
        if linked_name == '@cavemessengerbot':
            chat.send(f'Only a dimwit like you would try to insult a bot {name}', reply_to=message.id)
        else:
            text = insult.replace('<name>', linked_name)
            chat.send(text, reply_to=message.id)
    else:
        chat.send(f'You are too dumb to use a command properly {name}', reply_to=message.id)


@bot.command('germanize')
def germanize(chat: botogram.Chat, message: botogram.Message, args: list):
    """Germanize text"""

    refusals = read('refuse.txt')
    number = random.randint(0, len(refusals) - 1)
    refuse = refusals[number]

    if args:
        if not all(isinstance(x, str) for x in args):
            chat.send(f'You trult are too dumb to use a command properly', reply_to=message.id)
        else:
            args = ' '.join(args)
            german_text = transformer.germanize(args)
            chat.send(german_text, reply_to=message.id)

    elif message.reply_to_message:
        if message.reply_to_message.text:
            if not isinstance(message.reply_to_message.text, str):
                chat.send(refuse, reply_to=message.id)
            else:
                german_text = transformer.germanize(message.reply_to_message.text)
                chat.send(german_text, message.id)
        else:
            chat.send(refuse, reply_to=message.id)
    else:
        chat.send(f'You truly are too dumb to use a command properly', reply_to=message.id)


@bot.command('source')
def source(chat: botogram.Chat, message: botogram.Message):
    """Have a look at the source code"""
    url = 'https://github.com/piratecaveman/cavemessenger'
    text = (f"You can have a look at my source code here if you'd like:"
            f"{url}")
    chat.send(text, reply_to=message.id)
z

if __name__ == '__main__':
    bot.run()
