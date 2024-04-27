import random

from telebot import types, TeleBot, custom_filters
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage

from database import get_random_pair, Word, create_session, add_new_word, delete_word


print('Bot is running...')

state_storage = StateMemoryStorage()
token_bot = ''
bot = TeleBot(token_bot, state_storage=state_storage)

known_users = []
userStep = {}
buttons = []


def show_hint(*lines):
    return '\n'.join(lines)


def show_target(data):
    return f"{data['translate_word']} -> {data['target_word']}"


class Command:
    ADD_WORD = 'Добавить слово ✚'
    DELETE_WORD = 'Удалить слово —'
    NEXT = 'Дальше ⏭'


class MyStates(StatesGroup):
    target_word = State()
    translate_word = State()
    another_words = State()


def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        known_users.append(uid)
        userStep[uid] = 0
    print("New user detected, who hasn't used \"/start\" yet")
    return 0


@bot.message_handler(commands=['cards', 'start'])
def create_cards(message):
    cid = message.chat.id
    session = create_session()
    if cid not in known_users:
        known_users.append(cid)
        userStep[cid] = 0
        bot.send_message(cid, "Hello! Let's study English!")
    markup = types.ReplyKeyboardMarkup(row_width=2)
    global buttons
    buttons = []

    pair = get_random_pair()
    target_word = pair[1]
    translate = pair[0]
    target_word_btn = types.KeyboardButton(target_word)
    buttons.append(target_word_btn)

    other_words = [word.translate for word in session.query(Word).filter(Word.translate != translate).all()]
    other_words = random.sample(other_words, 3)
    other_words_btns = [types.KeyboardButton(word) for word in other_words]
    buttons.extend(other_words_btns)

    random.shuffle(buttons)

    next_btn = types.KeyboardButton(Command.NEXT)
    add_word_btn = types.KeyboardButton(Command.ADD_WORD)
    delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)
    buttons.extend([next_btn, add_word_btn, delete_word_btn])

    markup.add(*buttons)

    greeting = f"Выберите перевод:\n🇷🇺 {translate}"
    bot.send_message(message.chat.id, greeting, reply_markup=markup)
    bot.set_state(message.from_user.id, MyStates.target_word, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['target_word'] = target_word
        data['translate_word'] = translate
        data['other_words'] = other_words


@bot.message_handler(func=lambda message: message.text == Command.NEXT)
def next_cards(message):
    create_cards(message)


@bot.message_handler(func=lambda message: message.text == Command.DELETE_WORD)
def delete_word_handler(message):
    cid = message.chat.id
    userStep[cid] = 2
    bot.send_message(cid, 'Введите слово для удаления:')
    bot.register_next_step_handler(message, delete_word_from_db)


def delete_word_from_db(message):
    word_to_delete = message.text
    session = create_session()
    word = session.query(Word).filter_by(word=word_to_delete).first()
    if word:
        delete_word(word_to_delete)
        bot.send_message(message.chat.id, f'Слово "{word_to_delete}" удалено.')
    else:
        bot.send_message(message.chat.id, f'Ошибка! Слово "{word_to_delete}" отсутствует в базе данных.')
    create_cards(message)


@bot.message_handler(func=lambda message: message.text == Command.ADD_WORD)
def add_word(message):
    cid = message.chat.id
    userStep[cid] = 1
    bot.send_message(message.chat.id, 'Введите слово:')
    bot.register_next_step_handler(message, add_word_translate)


def add_word_translate(message):
    cid = message.chat.id
    target_word = message.text
    bot.send_message(cid, 'Введите перевод:')
    bot.register_next_step_handler(message, add_word_to_db, target_word)


def add_word_to_db(message, target_word):
    cid = message.chat.id
    translate_word = message.text

    session = create_session()
    word = session.query(Word).filter_by(word=target_word).first()

    if word:
        bot.send_message(cid, f'Ошибка! Слово "{target_word}" уже есть в базе данных.')
    else:
        add_new_word(target_word, translate_word)
        markup = types.ReplyKeyboardMarkup(row_width=2)
        next_btn = types.KeyboardButton(Command.NEXT)
        markup.add(next_btn)
        bot.send_message(cid, 'Слово добавлено!', reply_markup=markup)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def message_reply(message):
    text = message.text
    markup = types.ReplyKeyboardMarkup(row_width=2)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        target_word = data['target_word']
        if text == target_word:
            hint = show_target(data)
            hint_text = ["Это правильный ответ! 👍", hint]
            next_btn = types.KeyboardButton(Command.NEXT)
            add_word_btn = types.KeyboardButton(Command.ADD_WORD)
            delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)
            buttons.extend([next_btn, add_word_btn, delete_word_btn])
            hint = show_hint(*hint_text)
        else:
            for btn in buttons:
                if btn.text == text:
                    btn.text = text + '❌'
                    break
            hint = show_hint("Ошибка!",
                             f"Попробуйте ещё раз 🇷🇺{data['translate_word']}")
    markup.add(*buttons)
    bot.send_message(message.chat.id, hint, reply_markup=markup)


bot.add_custom_filter(custom_filters.StateFilter(bot))

bot.infinity_polling(skip_pending=True)
