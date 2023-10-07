import telebot
import pprint
import webbrowser
from telebot import types
import sqlite3

bot = telebot.TeleBot('6466557038:AAG5DcQxvA_xmU561vVRQMdY66O57_TnWY0')


@bot.message_handler(commands=['start'])
def start(message):
    """
        :param message:
        {'content_type': 'text', 'id': 6, 'message_id': 6, 'from_user': {'id': 457820490, 'is_bot': False,
        'first_name': 'Oleg', 'username': 'geloverasok', 'last_name': 'Kosarev', 'language_code': 'en',
        'can_join_groups': None, 'can_read_all_group_messages': None, 'supports_inline_queries': None,
        'is_premium': None, 'added_to_attachment_menu': None}, 'date': 1696679562,
        'chat': {
            'id': 457820490, 'type': 'private', 'title': None, 'username': 'geloverasok', 'first_name': 'Oleg',
            'last_name': 'Kosarev', 'is_forum': None, 'photo': None, 'bio': None, 'join_to_send_messages': None,
            'join_by_request': None, 'has_private_forwards': None, 'has_restricted_voice_and_video_messages': None,
            'description': None, 'invite_link': None, 'pinned_message': None, 'permissions': None,
            'slow_mode_delay': None, 'message_auto_delete_time': None, 'has_protected_content': None,
            'sticker_set_name': None, 'can_set_sticker_set': None, 'linked_chat_id': None, 'location': None,
            'active_usernames': None, 'emoji_status_custom_emoji_id': None, 'has_hidden_members': None,
            'has_aggressive_anti_spam_enabled': None, 'emoji_status_expiration_date': None}, 'sender_chat': None,
            'forward_from': None, 'forward_from_chat': None, 'forward_from_message_id': None, 'forward_signature': None,
            'forward_sender_name': None, 'forward_date': None, 'is_automatic_forward': None, 'reply_to_message': None,
            'via_bot': None, 'edit_date': None, 'has_protected_content': None, 'media_group_id': None,
            'author_signature': None, 'text': '/start',
            'entities': [<telebot.types.MessageEntity object at 0x0000011A5976A2B0>], 'caption_entities': None,
            'audio': None, 'document': None, 'photo': None, 'sticker': None, 'video': None, 'video_note': None,
            'voice': None, 'caption': None, 'contact': None, 'location': None, 'venue': None, 'animation': None,
            'dice': None, 'new_chat_member': None, 'new_chat_members': None, 'left_chat_member': None,
            'new_chat_title': None, 'new_chat_photo': None, 'delete_chat_photo': None, 'group_chat_created': None,
            'supergroup_chat_created': None, 'channel_chat_created': None, 'migrate_to_chat_id': None,
            'migrate_from_chat_id': None, 'pinned_message': None, 'invoice': None, 'successful_payment': None,
            'connected_website': None, 'reply_markup': None, 'message_thread_id': None, 'is_topic_message': None,
            'forum_topic_created': None, 'forum_topic_closed': None, 'forum_topic_reopened': None,
            'has_media_spoiler': None, 'forum_topic_edited': None, 'general_forum_topic_hidden': None,
            'general_forum_topic_unhidden': None, 'write_access_allowed': None, 'user_shared': None,
            'chat_shared': None, 'story': None, 'json': {'message_id': 6, 'from': {'id': 457820490,
            'is_bot': False, 'first_name': 'Oleg', 'last_name': 'Kosarev', 'username': 'geloverasok',
            'language_code': 'en'}, 'chat': {'id': 457820490, 'first_name': 'Oleg', 'last_name': 'Kosarev',
            'username': 'geloverasok', 'type': 'private'}, 'date': 1696679562, 'text': '/start',
            'entities': [{'offset': 0, 'length': 6, 'type': 'bot_command'}]
            }
        }
        """

    conn = sqlite3.connect('admix_db.sql')
    cur = conn.cursor()

    cur.execute(
        'CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    markup = types.ReplyKeyboardMarkup()
    btn_1 = types.KeyboardButton('Go to website')
    markup.row(btn_1)
    btn_2 = types.KeyboardButton('One')
    btn_3 = types.KeyboardButton('Two')
    markup.add(btn_2, btn_3)
    # file_start = open('./photo.jpeg', 'rb')                              # если хотим при старте отправлять картинку
    # bot.send_photo(message.chat.id, file_start, reply_markup=markup)
    bot.send_message(message.chat.id,
                     f"Hello!!! \n Enter login:",
                     reply_markup=markup)  # отправляем в ответ
    bot.register_next_step_handler(message, user_name)
    bot.register_next_step_handler(message, on_click)


def user_name(message):
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Enter password')
    bot.register_next_step_handler(message, user_pass, name)


def user_pass(message, user_name):
    password = message.text.strip()

    conn = sqlite3.connect('admix_db.sql')
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (user_name, password))
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('All Users', callback_data='users'))
    bot.send_message(message.chat.id, 'Authorised', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('admix_db.sql')
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    info = ''
    for el in users:
        info += f"Login: {el[1]} ====> Password: {el[2]}\n"
    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)


def on_click(message):
    if message.text == 'Go to website':
        bot.send_message(message.chat.id, 'Open site')
    elif message.text == 'One':
        bot.send_message(message.chat.id, 'One')
    elif message.text == 'Two':
        bot.send_message(message.chat.id, 'Two')


@bot.message_handler(commands=['help'])
def open_help(message):
    bot.send_message(message.chat.id, '<b>Help information</b>',
                     parse_mode='html')  # parse_mode='html' - дает возможность редактировать текст тегами


@bot.message_handler()
def view_info(message):
    if message.text.lower() == 'no':
        bot.send_message(message.chat.id, '<b>NO</b>',
                         parse_mode='html')
    elif message.text.lower() == 'yes':
        bot.reply_to(message, f"YES {message.from_user.id}")


@bot.message_handler(commands=['site', 'website'])
def go_to_site(message):
    webbrowser.open('https://www.it-admix.by')


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn_1 = types.InlineKeyboardButton('Go to website', url='https://it-admix.by')
    markup.row(btn_1)
    btn_2 = types.InlineKeyboardButton('Delete', callback_data='delete')
    btn_3 = types.InlineKeyboardButton('Edit', callback_data='edit')
    markup.add(btn_2, btn_3)
    bot.reply_to(message, 'PHOTO', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text(callback.message.chat.id, callback.message.message_id - 1)


bot.polling(none_stop=True)  # не дает закрываться программе
# bot.infinity_polling(none_stop=True) #тоже самое, что и bot.polling(none_stop=True), не дает закрываться программе
